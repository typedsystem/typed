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
    FACTORY,
    OPERATION,
    DEPENDENT,
    LAZY
)

class Callable(metaclass=CALLABLE):
    """
    The type of callables.

    : typeof(Callable)    is  CALLABLE
    : isterm(f, Callable) iff issub(typeof(f), Callable)
    : nullof(Callable)    is  nill

    """
    def __init__(self, func):
        from typed.mods.check import check
        check.isinstance(func, callable)

        self.__func__    = func
        self.__wrapped__ = func

    def __call__(self, *a, **kw):
        return self.__func__(*a, **kw)

    @property
    def args(self):
        from typed.helper.func import _args
        return _args(self)

    @property
    def kwargs(self):
        from typed.helper.func import _kwargs
        return _kwargs(self)

    @property
    def posargs(self):
        from typed.helper.func import _pos_args
        return _pos_args(self)

    @property
    def unwrap(self):
        from typed.helper.func import _unwrap
        return _unwrap(self)

    @property
    def __name__(self):
        return getattr(self.unwrap(), "__name__")

    @property
    def __display__(self):
        return self.__name__

    from typed.mods.init import TYPESYSTEM

    __typesystems__ = [TYPESYSTEM]
    __type__       = CALLABLE
    __display__    = "Callable"
    __name__       = "Callable"
    __builtin__    = callable

class Lambda(metaclass=LAMBDA):


Lambda  = LAMBDA('Lambda', (Callable,), {"__display__": "Lambda", "__flags__": {**Callable.__flags__, "is_lambda": True}})
Class         = CLASS('Class', (Callable,), {"__display__": "Class", "__flags__": {**Callable.__flags__, "is_class": True}})
Method        = METHOD('Method', (Callable,), {"__display__": "Method", "__flags__": {**Callable.__flags__, "is_method": True}})

class Func(Callable, metaclass=FUNC):
    """
    The type of functions.
    """
    __flags__ = {**Callable.__flags__, "is_func": True}

class DomFunc(Func, metaclass=DOM_FUNC):
    __flags__ = {**Func.__flags__, "is_dom": True}

class CodFunc(Func, metaclass=COD_FUNC):
    __flags__ = {**Func.__flags__, "is_cod": True}

class CompFunc(DomFunc, CodFunc, metaclass=COMP_FUNC):
    __flags__ = {**DomFunc.__flags__, **CodFunc.__flags__, "is_comp": True}

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
        (f << g)(*args, **kwargs) == f(g(*args, **kwargs)).
        """
        from inspect import signature
        from typing import get_type_hints
        if not _is_composable(other, self):
            dom_f, cod_f = _get_dom_cod(self)
            dom_g, cod_g = _get_dom_cod(other)
            dom0_f = dom_f[0] if dom_f else None
            raise TypeError(
                "Wrong type in function composition 'f << g':\n"
                f" ==> codomain '{_name(cod_g)}' of '{_name(other)}' "
                f"does not match domain '{_name(dom0_f)}' of '{_name(self)}'"
            )

        dom_f, cod_f = _get_dom_cod(self)
        dom_g, cod_g = _get_dom_cod(other)

        if not dom_f:
            raise TypeError(
                "Wrong type in function composition 'f << g':\n"
                f" ==> '{_name(self)}' has empty domain"
            )

        if len(dom_f) > 1:
            cod_types = getattr(cod_g, "__types__", None)
            if cod_types is None or tuple(cod_types) != tuple(dom_f):
                raise TypeError(
                    "Wrong type in function composition 'f << g':\n"
                    f" ==> '{_name(self)}' expects {len(dom_f)} arguments but "
                    f"'{_name(other)}' returns '{_name(cod_g)}'; cannot feed the result "
                    f"of '{_name(other)}' into '{_name(self)}'"
                )

        orig_f = _unwrap(self)
        orig_g = _unwrap(other)

        try:
            sig_g = signature(orig_g)
            ann_g = get_type_hints(orig_g)
        except Exception:
            sig_g = None
            ann_g = {}

        composite_anns = dict(ann_g)
        composite_anns["return"] = cod_f

        outer = self
        inner = other

        def composed_orig(*args, **kwargs):
            return outer(inner(*args, **kwargs))

        composed_orig.__name__ = (
            f"{getattr(outer, '__name__', 'f')}∘{getattr(inner, '__name__', 'g')}"
        )
        composed_orig.__annotations__ = composite_anns
        if sig_g:
            composed_orig.__signature__ = sig_g

        from typed.mods.types.func import Lazy
        if getattr(self, "is_lazy", False) and getattr(other, "is_lazy", False):
            return Lazy(composed_orig)

        return composed_orig

    def __rshift__(self, other):
        """
        (f >> g)(*args, **kwargs) == g(f(*args, **kwargs)).
        """
        from inspect import signature
        from typing import get_type_hints
        if not _is_composable(self, other):
            dom_f, cod_f = _get_dom_cod(self)
            dom_g, cod_g = _get_dom_cod(other)
            dom0_g = dom_g[0] if dom_g else None
            raise TypeError(
                "Wrong type in function composition 'f >> g':\n"
                f" ==> codomain '{_name(cod_f)}' of '{_name(self)}' "
                f"does not match domain '{_name(dom0_g)}' of '{_name(other)}'"
            )

        dom_f, cod_f = _get_dom_cod(self)
        dom_g, cod_g = _get_dom_cod(other)

        if not dom_g:
            raise TypeError(
                "Wrong type in function composition 'f >> g':\n"
                f" ==> '{_name(other)}' has empty domain"
            )

        if len(dom_g) > 1:
            cod_types = getattr(cod_f, "__types__", None)
            if cod_types is None or tuple(cod_types) != tuple(dom_g):
                raise TypeError(
                    "Wrong type in function composition 'f >> g':\n"
                    f" ==> '{_name(other)}' expects {len(dom_g)} arguments but "
                    f"'{_name(self)}' returns '{_name(cod_f)}'; cannot feed the result "
                    f"of '{_name(self)}' into '{_name(other)}'"
                )

        orig_f = _unwrap(self)
        orig_g = _unwrap(other)

        try:
            sig_f = signature(orig_f)
            ann_f = get_type_hints(orig_f)
        except Exception:
            sig_f = None
            ann_f = {}

        composite_anns = dict(ann_f)
        composite_anns["return"] = cod_g

        inner = self
        outer = other

        def composed_orig(*args, **kwargs):
            return outer(inner(*args, **kwargs))

        composed_orig.__name__ = (
            f"{getattr(outer, '__name__', 'g')}∘{getattr(inner, '__name__', 'f')}"
        )
        composed_orig.__annotations__ = composite_anns
        if sig_f:
            composed_orig.__signature__ = sig_f

        from typed.mods.types.func import Lazy
        if getattr(self, "is_lazy", False) and getattr(other, "is_lazy", False):
            return Lazy(composed_orig)

        return composed_orig


class DomHinted(DomFunc, metaclass=DOM_HINTED):
    __flags__ = {**DomFunc.__flags__, "is_dom_hinted": True}

    def __init__(self, func):
        _is_domain_hinted(func)
        self.__func__ = func
        self._hinted_domain = _hinted_domain(self.__func__)

    @property
    def domain(self):
        return self._hinted_domain

    @property
    def dom(self):
        return self.domain

class CodHinted(CodFunc, metaclass=COD_HINTED):
    __flags__ = {**CodFunc.__flags__, "is_cod_hinted": True}

    def __init__(self, func):
        _is_codomain_hinted(func)
        self.__func__ = func
        self._hinted_codomain = _hinted_codomain(self.__func__)

    @property
    def codomain(self):
        return self._hinted_codomain

    @property
    def cod(self):
        return self.codomain

class Hinted(CompFunc, DomHinted, CodHinted, metaclass=HINTED):
    __flags__ = {**CompFunc.__flags__, **DomHinted.__flags__, **CodHinted.__flags__, "is_hinted": True}

    def __init__(self, func):
        _is_domain_hinted(func)
        _is_codomain_hinted(func)
        DomHinted.__init__(self, func)
        CodHinted.__init__(self, func)

    @property
    def domain(self):
        return self._hinted_domain
    @property
    def dom(self):
        return self.domain
    @property
    def codomain(self):
        return self._hinted_codomain
    @property
    def cod(self):
        return self.codomain

class DomTyped(DomHinted, metaclass=DOM_TYPED):
    __flags__ = {**DomHinted.__flags__, "is_dom_typed": True}

    def __call__(self, *args, **kwargs):
        from inspect import signature
        from typed.mods.check import check
        sig = signature(self.__func__)
        b = sig.bind(*args, **kwargs); b.apply_defaults()
        check.dom(self.__func__, list(b.arguments.keys()), list(b.arguments.values()), self.domain)
        return self.__func__(*b.args, **b.kwargs)

class CodTyped(CodHinted, metaclass=COD_TYPED):
    __flags__ = {**CodHinted.__flags__, "is_cod_typed": True}

    def __call__(self, *args, **kwargs):
        from inspect import signature
        from typed.mods.check import check
        sig = signature(self.__func__)
        b = sig.bind(*args, **kwargs); b.apply_defaults()
        r = self.__func__(*b.args, **b.kwargs)
        check.cod(self.__func__, r, self.codomain)
        return r

class Typed(Hinted, DomTyped, CodTyped, metaclass=TYPED):
    __flags__ = {**Hinted.__flags__, **DomTyped.__flags__, **CodTyped.__flags__, "is_typed": True}

    def __call__(self, *args, **kwargs):
        from inspect import signature
        from typed.mods.check import check
        sig = signature(self.__func__)
        b = sig.bind(*args, **kwargs)
        b.apply_defaults()
        return check.issafe(self.__func__, b, self.domain, self.codomain)

class Condition(Typed, metaclass=CONDITION):
    __flags__ = {**Typed.__flags__, "is_condition": True}

class Factory(Typed, metaclass=FACTORY):
    __flags__ = {**Typed.__flags__, "is_factory": True}

class Operation(Factory, metaclass=OPERATION):
    __flags__ = {**Factory.__flags__, "is_operation": True}

class Dependent(Factory, metaclass=DEPENDENT):
    __flags__ = {**Factory.__flags__, "is_dependent": True}

class Lazy(Hinted, metaclass=LAZY):
    __flags__ = {**Hinted.__flags__, "is_lazy": True}

    def __init__(self, f):
        self.__func__ = f
        self.__wrapped__ = f

        self._wrapped = None

        self._lazy_domain = tuple(_hinted_domain(self.__func__))
        self._lazy_codomain = _hinted_codomain(self.__func__)

    @property
    def domain(self):
        return self._lazy_domain

    @property
    def dom(self):
        return self.domain

    @property
    def codomain(self):
        return self._lazy_codomain

    @property
    def cod(self):
        return self.codomain

    def materialize(self):
        if self._wrapped is None:
            self._wrapped = Typed(self.__func__)
        return self._wrapped

    def __call__(self, *a, **kw):
        return self.materialize()(*a, **kw)

    def __getattr__(self, name):
        if name in ('__flags__', '__func__', '__wrapped__', '_wrapped', 'is_lazy', '_lazy_domain', '_lazy_codomain'):
            return super().__getattribute__(name)
        return getattr(self.materialize(), name)

class Partial(Func, metaclass=PARTIAL):
    def __init__(self, func, bound_args, bound_kwargs):
        self.original_func = func
        self.func = func
        self.__wrapped__ = func

        self.bound_args = list(bound_args)
        self.bound_kwargs = dict(bound_kwargs)
        self.is_partial = True
        self.is_lazy = getattr(func, "is_lazy", False)

        try:
            from typed.mods.general import _
            base = _unwrap(func)

            def _fmt_arg(a):
                if a is _:
                    return "_"
                return repr(a)

            pos = ", ".join(_fmt_arg(a) for a in bound_args)
            kw  = ", ".join(
                f"{k}={_fmt_arg(v)}" for k, v in bound_kwargs.items()
            )
            inside = ", ".join(p for p in (pos, kw) if p)
            self.__display__ = f"{_name(base)}({inside})"
        except Exception:
            self.__display__ = _name(func)

        if hasattr(func, '__name__'):
            self.__name__ = f"{func.__name__}_partial"
        else:
            self.__name__ = "partial"

        if hasattr(func, 'domain'):
            self._original_domain = func.domain
        if hasattr(func, 'codomain'):
            self._original_codomain = func.codomain

    def __call__(self, *new_args, **new_kwargs):
        from typed.mods.general import _
        from typed.mods.types.base import TYPE

        effective_new_pos = [a for a in new_args if a is not _]
        effective_new_kw  = [v for v in new_kwargs.values() if v is not _]
        num_effective_new = len(effective_new_pos) + len(effective_new_kw)

        expected_remaining = len(self.domain)

        if num_effective_new > expected_remaining:
            if len(new_args) == 1 and not new_kwargs:
                input_val = new_args[0]
            else:
                input_val = tuple(new_args) if not new_kwargs else (tuple(new_args), new_kwargs)

            if len(self.domain) == 1:
                expected_type = self.domain[0]
            else:
                expected_type = self.domain

            actual_type = TYPE(input_val)

            raise TypeError(
                f"Domain mismatch in partial application '{_name(self)}':\n"
                f" ==> input has value '{input_val}'\n"
                f"     [expected_type] '{_name(expected_type)}'\n"
                f"     [received_type] '{_name(actual_type)}'"
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

        target = getattr(self.func, "func", self.func)
        try:
            sig = signature(target)
            param_names = list(sig.parameters.keys())
        except Exception:
            sig = None
            param_names = []

        for kwarg_name, kwarg_value in new_kwargs.items():
            if kwarg_name in kwarg_dict and kwarg_dict[kwarg_name] is not _:
                raise TypeError(
                    f"Argument '{kwarg_name}' is already bound in this partial "
                    f"and cannot be provided again."
                )

            if kwarg_name in param_names:
                param_index = param_names.index(kwarg_name)
                if param_index < len(arg_list) and arg_list[param_index] is not _:
                    raise TypeError(
                        f"Argument '{kwarg_name}' is already bound in this partial "
                        f"and cannot be provided again."
                    )

        if param_names:
            for kwarg_name, kwarg_value in new_kwargs.items():
                if kwarg_name in param_names:
                    param_index = param_names.index(kwarg_name)
                    if param_index < len(arg_list) and arg_list[param_index] is _:
                        arg_list[param_index] = kwarg_value

        if _ in arg_list:
            new_partial = object.__new__(self.__class__)
            new_partial.__init__(self.func, arg_list, kwarg_dict)
            return new_partial

        cleaned_args = [arg for arg in arg_list if arg is not _]

        final_kwargs = kwarg_dict.copy()
        final_kwargs.update(new_kwargs)

        if sig is not None:
            for i in range(min(len(cleaned_args), len(param_names))):
                param_name = param_names[i]
                if param_name in final_kwargs:
                    del final_kwargs[param_name]

        return self.func(*cleaned_args, **final_kwargs)

    def __repr__(self):
        return (
            f"<Partial: {getattr(self.func, '__name__', 'func')} "
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

    @property
    def domain(self):
        from typed.mods.general import _
        if not hasattr(self, '_original_domain'):
            return ()

        target = getattr(self.func, "func", self.func)

        try:
            sig = signature(target)
            param_names = list(sig.parameters.keys())
        except Exception:
            remaining = [
                t for arg, t in zip(self.bound_args, self._original_domain)
                if arg is _
            ]
            return tuple(remaining)

        remaining_types = []

        for idx, (name, typ) in enumerate(zip(param_names, self._original_domain)):
            pos_bound = idx < len(self.bound_args) and self.bound_args[idx] is not _
            kw_bound = name in self.bound_kwargs

            if not pos_bound and not kw_bound:
                remaining_types.append(typ)

        return tuple(remaining_types)

    @property
    def codomain(self):
        if hasattr(self, '_original_codomain'):
            return self._original_codomain
        return None

    @property
    def dom(self):
        return self.domain

    @property
    def cod(self):
        return self.codomain
