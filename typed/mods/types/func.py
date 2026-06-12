from typed.mods.meta.func import (
    CALLABLE,
    LAMBDA,
    CLASS,
    METHOD,
    FUNC,
    DOM_FUNC,
    COD_FUNC,
    COMP_FUNC,
    DOM_HINTED,
    COD_HINTED,
    HINTED,
    DOM_TYPED,
    COD_TYPED,
    TYPED,
    CONDITION,
    FAMILY,
    CONSTRUCTOR,
    LAZY_FUNC,
    LAZY_HINTED,
    LAZY_TYPED,
    LAZY_CONDITION,
    LAZY_FAMILY,
    LAZY_CONSTRUCTOR,
)
from typed.mods.nill import nill

class Callable(metaclass=CALLABLE):
    """
    The type of callables.

    : typeof(Callable)    is  CALLABLE
    : isterm(f, Callable) iff callable(f)
    : nullof(Callable)    is  nill
    """

    def __call__(self, *args, **kwargs):

        if Ellipsis in args or any(v is Ellipsis for v in kwargs.values()):
            return self.reduce(*args, **kwargs)
        return self.__func__(*args, **kwargs)

    def reduce(self, *args, **kwargs):
        from typed.mods.func import reduce as _reduce
        reduced = _reduce(self.__func__, *args, **kwargs)

        inst = type(self)(reduced)

        try:
            from typed.mods.typesystem import nameof
            base_name = nameof(self)
            from typed.helper.func import _repr_arg

            pos = ", ".join(_repr_arg(a) for a in args)
            kw  = ", ".join(f"{k}={_repr_arg(v)}" for k, v in kwargs.items())
            inside = ", ".join(p for p in (pos, kw) if p)
            if inside:
                inst.__display__ = f"{base_name}({inside})"
            else:
                inst.__display__ = base_name
        except Exception:
            inst.__display__ = reduced.__name__

        return inst

    @property
    def signature(self):
        from typed.mods.func import signature
        return signature(self)

    @property
    def args(self):
        return self.signature.args

    @property
    def kwargs(self):
        from typed.mods.err import NotDefined
        return tuple(a for a in self.args if a.default is not NotDefined)

    @property
    def posargs(self):
        from typed.mods.err import NotDefined
        return tuple(a for a in self.args if a.default is NotDefined)

    @property
    def dom(self):
        return getattr(self, "_lazy_dom", self.signature.dom)

    @property
    def cod(self):
        return getattr(self, "_lazy_cod", self.signature.cod)

    @property
    def unwrap(self):
        from typed.mods.func import unwrap
        return unwrap(self)

    @property
    def __name__(self):
        from typed.mods.err import NotDefined
        return getattr(self.unwrap, "__name__", NotDefined)

    @property
    def __display__(self):
        return self.__name__

    __null__    = nill.func
    __builtin__ = callable

class Lambda(Callable, metaclass=LAMBDA):
    """
    """
class Class(Callable, metaclass=CLASS):
    """
    """
    __null__ = nill.cls

class Method(Callable, metaclass=METHOD):
    """
    """
    __null__ = nill.cls().nill

class Func(Callable, metaclass=FUNC):
    """
    The type of functions.
    """
    __null__ = nill.func

class DomFunc(Func, metaclass=DOM_FUNC):
    """
    """
    __null__ = nill.dom.func

class CodFunc(Func, metaclass=COD_FUNC):
    """
    """
    __null__ = nill.cod.func

class CompFunc(DomFunc, CodFunc, metaclass=COMP_FUNC):
    """
    """
    __null__ = nill.comp

    def __rlshift__(self, other):
        """
        Support 'other << self' when 'other' does not
        implement __lshift__ but is in DomFunc/CodFunc.
        """
        return CompFunc.__lshift__(other, self)

    def __rrshift__(self, other):
        """
        Support 'other >> self' when 'other' does not
        implement __rshift__ but is in DomFunc/CodFunc.
        """
        return CompFunc.__rshift__(other, self)

    def __lshift__(self, other):
        """
        (self << other)(*args, **kwargs) == self(other(*args, **kwargs)).
        """
        from typed.mods.func import compose
        return compose(self, other)

    def __rshift__(self, other):
        """
        (self >> other)(*args, **kwargs) == other(self(*args, **kwargs)).
        """
        from typed.mods.func import compose
        return compose(other, self)

class DomHinted(DomFunc, metaclass=DOM_HINTED):
    __null__ = nill.dom.hinted

class CodHinted(CodFunc, metaclass=COD_HINTED):
    __null__ = nill.cod.hinted

class Hinted(CompFunc, DomHinted, CodHinted, metaclass=HINTED):
    __null__ = nill.hinted

class DomTyped(DomHinted, metaclass=DOM_TYPED):
    __null__ = nill.dom.typed

    def __call__(self, *args, check: bool=True, **kwargs):
        if Ellipsis in args or any(v is Ellipsis for v in kwargs.values()):
            return self.reduce(*args, **kwargs)

        effective_check = check and getattr(self, '_check', True)

        if effective_check:
            from typed.mods.check import check as _check
            from typed.mods.func import signature
            sig = signature(self.__func__)
            _check.bind.dom(self.__func__, sig, args, kwargs)

        return self.__func__(*args, **kwargs)

class CodTyped(CodHinted, metaclass=COD_TYPED):
    __null__ = nill.cod.typed

    def __call__(self, *args, check: bool=True, **kwargs):
        if Ellipsis in args or any(v is Ellipsis for v in kwargs.values()):
            return self.reduce(*args, **kwargs)

        r = self.__func__(*args, **kwargs)

        effective_check = check and getattr(self, '_check', True)

        if effective_check:
            from typed.mods.check import check as _check
            from typed.mods.func import signature
            sig = signature(self.__func__)
            _check.bind.cod(self.__func__, sig, r)

        return r

class Typed(Hinted, DomTyped, CodTyped, metaclass=TYPED):
    __null__ = nill.cod.typed

    def __call__(self, *args, check: bool=True, **kwargs):
        if Ellipsis in args or any(v is Ellipsis for v in kwargs.values()):
            return self.reduce(*args, **kwargs)

        effective_check = check and getattr(self, '_check', True)

        if effective_check:
            from typed.mods.check import check as _check
            from typed.mods.func import signature
            sig = signature(self.__func__)
            _check.bind.dom(self.__func__, sig, args, kwargs)

        r = self.__func__(*args, **kwargs)

        if effective_check:
            if 'sig' not in locals():
                from typed.mods.func import signature
                sig = signature(self.__func__)

            from typed.mods.check import check as _check
            _check.bind.cod(self.__func__, sig, r)

        return r

class Condition(Typed, metaclass=CONDITION):
    __null__ = nill.condition

class Family(Typed, metaclass=FAMILY):
    __null__ = nill.family

class Constructor(Family, metaclass=CONSTRUCTOR):
    __null__ = nill.constructor


class LazyFunc(Callable, metaclass=LAZY_FUNC):
    def materialize(self):
        if self._wrapped is None:
            target_type = getattr(self, '_target_type', None)
            if target_type is None:
                target_type = Func

            self._wrapped = target_type(
                self.__func__, 
                check=self._check, 
                defaults=self._defaults, 
                envs=self._envs
            )
        return self._wrapped

    def __call__(self, *args, check: bool=True, **kwargs):
        if Ellipsis in args or any(v is Ellipsis for v in kwargs.values()):
            return self.reduce(*args, **kwargs)

        return self.materialize()(*args, check=check, **kwargs)

    def __getattr__(self, name):
        if name in ('__flags__', '__func__', '__wrapped__', '_wrapped', 'is_lazy', '_target_type', '_check', '_defaults', '_envs', '_lazy_dom', '_lazy_cod'):
            return super().__getattribute__(name)
        return getattr(self.materialize(), name)

class LazyHinted(LazyFunc, Hinted, metaclass=LAZY_HINTED):
    __null__ = nill.hinted

class LazyTyped(LazyFunc, Typed, metaclass=LAZY_TYPED):
    __null__ = nill.cod.typed

class LazyCondition(LazyFunc, Condition, metaclass=LAZY_CONDITION):
    __null__ = nill.condition

class LazyFamily(LazyFunc, Family, metaclass=LAZY_FAMILY):
    __null__ = nill.family

class LazyConstructor(LazyFunc, Constructor, metaclass=LAZY_CONSTRUCTOR):
    __null__ = nill.constructor
