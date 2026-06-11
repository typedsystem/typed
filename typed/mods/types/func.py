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
    LAZY_TYPED,
    PARTIAL
)
from typed.mods.nill import nill

class Callable(metaclass=CALLABLE):
    """
    The type of callables.

    : typeof(Callable)    is  CALLABLE
    : isterm(f, Callable) iff callable(f)
    : nullof(Callable)    is  nill
    """

    def __call__(self, *a, **kw):
        return self.__func__(*a, **kw)

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
        return self.signature.dom

    @property
    def cod(self):
        return self.signature.cod

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
        from typed.helper.func import _compose_functions
        return _compose_functions(self, other)

    def __rshift__(self, other):
        """
        (self >> other)(*args, **kwargs) == other(self(*args, **kwargs)).
        """
        from typed.helper.func import _compose_functions
        return _compose_functions(other, self)

class DomHinted(DomFunc, metaclass=DOM_HINTED):
    __null__ = nill.dom.hinted

class CodHinted(CodFunc, metaclass=COD_HINTED):
    __null__ = nill.cod.hinted

class Hinted(CompFunc, DomHinted, CodHinted, metaclass=HINTED):
    __null__ = nill.hinted

class DomTyped(DomHinted, metaclass=DOM_TYPED):
    __null__ = nill.dom.typed

    def __call__(self, *args, check: bool=True, **kwargs):
        from typed.mods.func import signature
        from typed.mods.check import check as _check

        sig_data = signature(self.__func__)
        b = sig_data.bind(*args, **kwargs)

        if check:
            _check.bind.dom(self.__func__, list(b.arguments.keys()), list(b.arguments.values()), sig_data.dom)

        return self.__func__(*b.args, **b.kwargs)

class CodTyped(CodHinted, metaclass=COD_TYPED):
    __null__ = nill.cod.typed

    def __call__(self, *args, check: bool=True, **kwargs):
        from typed.mods.func import signature
        from typed.mods.check import check as _check

        sig_data = signature(self.__func__)
        b = sig_data.bind(*args, **kwargs)

        r = self.__func__(*b.args, **b.kwargs)

        if check:
            _check.bind.cod(self.__func__, r, sig_data.cod)

        return r

class Typed(Hinted, DomTyped, CodTyped, metaclass=TYPED):
    __null__ = nill.cod.typed

    def __call__(self, *args, check: bool=True, **kwargs):
        from typed.mods.func import signature
        from typed.mods.check import check as _check

        sig_data = signature(self.__func__)
        b = sig_data.bind(*args, **kwargs)

        r = self.__func__(*b.args, **b.kwargs)

        if check:
            _check.issafe(self.__func__, list(b.arguments.keys()), list(b.arguments.values()), sig_data.dom, r, sig_data.cod)

        return r

class Condition(Typed, metaclass=CONDITION):
    __null__ = nill.condition

class Family(Typed, metaclass=FAMILY):
    __null__ = nill.family

class Constructor(Family, metaclass=CONSTRUCTOR):
    __null__ = nill.constructor

class LazyTyped(Hinted, metaclass=LAZY_TYPED):
    def materialize(self):
        if self._wrapped is None:
            self._wrapped = Typed(self.__func__)
        return self._wrapped

    def __call__(self, *a, check: bool=True, **kw):
        return self.materialize()(*a, check=check, **kw)

    def __getattr__(self, name):
        if name in ('__flags__', '__func__', '__wrapped__', '_wrapped', 'is_lazy'):
            return super().__getattribute__(name)
        return getattr(self.materialize(), name)

class Partial(Func, metaclass=PARTIAL):
    def __call__(self, *new_args, **new_kwargs):
        from typed.mods.general import _
        from typed.mods.typesystem import nameof
        from typed.mods.func import signature
        from typed.mods.err import TypeErr

        effective_new_pos = [a for a in new_args if a is not _]
        effective_new_kw  = [v for v in new_kwargs.values() if v is not _]
        num_effective_new = len(effective_new_pos) + len(effective_new_kw)

        expected_remaining = len(self.dom)

        if num_effective_new > expected_remaining:
            if len(new_args) == 1 and not new_kwargs:
                input_val = new_args[0]
            else:
                input_val = tuple(new_args) if not new_kwargs else (tuple(new_args), new_kwargs)

            if len(self.dom) == 1:
                expected_type = self.dom[0]
            else:
                expected_type = self.dom

            from typed.mods.meta.atomic import TYPE
            actual_type = TYPE(input_val)

            raise TypeErr(
                message=f"Domain mismatch in partial application '{nameof(self)}'",
                received=actual_type,
                expected=expected_type,
            )

        arg_list = list(self.bound_args)
        kwarg_dict = dict(self.bound_kwargs)

        new_args_iter = iter(new_args)
        for i, arg in enumerate(arg_list):
            if arg is _:
                try:
                    arg_list[i] = next(new_args_iter)
                except StopIteration:
                    break

        for extra in new_args_iter:
            arg_list.append(extra)

        try:
            sig = signature(self.__func__)
            param_names = [a.name for a in sig.args]
        except Exception:
            sig = None
            param_names = []

        for kwarg_name, kwarg_value in new_kwargs.items():
            if kwarg_name in kwarg_dict and kwarg_dict[kwarg_name] is not _:
                raise TypeErr(
                    message=f"Argument '{kwarg_name}' is already bound in this partial and cannot be provided again."
                )

            if kwarg_name in param_names:
                param_index = param_names.index(kwarg_name)
                if param_index < len(arg_list) and arg_list[param_index] is not _:
                    raise TypeErr(
                        message=f"Argument '{kwarg_name}' is already bound in this partial and cannot be provided again."
                    )

        if param_names:
            for kwarg_name, kwarg_value in new_kwargs.items():
                if kwarg_name in param_names:
                    param_index = param_names.index(kwarg_name)
                    if param_index < len(arg_list) and arg_list[param_index] is _:
                        arg_list[param_index] = kwarg_value

        if _ in arg_list:
            new_partial = object.__new__(self.__class__)
            return PARTIAL(self.__func__, arg_list, kwarg_dict)

        cleaned_args = [arg for arg in arg_list if arg is not _]

        final_kwargs = kwarg_dict.copy()
        final_kwargs.update(new_kwargs)

        if sig is not None:
            for i in range(min(len(cleaned_args), len(param_names))):
                param_name = param_names[i]
                if param_name in final_kwargs:
                    del final_kwargs[param_name]

        return self.__func__(*cleaned_args, **final_kwargs)

    def __repr__(self):
        return (
            f"<Partial: {getattr(self.__func__, '__name__', 'func')} "
            f"with bound args {self.bound_args} and kwargs {self.bound_kwargs}>"
        )

    def __lshift__(self, other):
        return CompFunc.__lshift__(self, other)

    def __rlshift__(self, other):
        return CompFunc.__lshift__(other, self)

    def __rshift__(self, other):
        return CompFunc.__rshift__(self, other)

    def __rrshift__(self, other):
        return CompFunc.__rshift__(other, self)
