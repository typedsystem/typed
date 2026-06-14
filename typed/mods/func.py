from functools import lru_cache as cache
from typed.mods.types.atomic import Dom, Cod

class Arg:
    def __init__(self, name: str, hint: object, default: object):
        self.name = name
        self.hint = hint
        self.default = default

class Signature:
    def __init__(self, func: callable, dom: Dom, cod: Cod, args: tuple[Arg, ...]):
        self.func = func
        self.dom = dom
        self.cod = cod
        self.args = args

    def bind(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def reduce(self, *reduce_args, **reduce_kwargs):
        fixed_values = {}

        for i, arg_val in enumerate(reduce_args):
            if arg_val is not Ellipsis:
                if i < len(self.args):
                    fixed_values[self.args[i].name] = arg_val

        for k, v in reduce_kwargs.items():
            if v is not Ellipsis:
                fixed_values[k] = v

        new_args = []
        new_dom = []
        for i, arg in enumerate(self.args):
            if arg.name not in fixed_values:
                new_args.append(arg)
                if i < len(self.dom):
                    new_dom.append(self.dom[i])

        new_sig = Signature(
            func=self.func,
            dom=tuple(new_dom),
            cod=self.cod,
            args=tuple(new_args)
        )
        return new_sig, fixed_values

def compose(f, g):
    def composed(*args, **kwargs):
        return f(g(*args, **kwargs))

    if hasattr(g, 'dom'):
        composed.dom = g.dom
    if hasattr(f, 'cod'):
        composed.cod = f.cod

    composed.__name__ = f"({getattr(f, '__name__', str(f))} << {getattr(g, '__name__', str(g))})"
    return composed

@cache
def hints(func):
    from typing import get_type_hints
    try:
        return get_type_hints(func)
    except Exception:
        return {}

@cache
def args(func: callable) -> tuple[Arg, ...]:
    from inspect import signature as _signature, Parameter
    from typed.mods.err import NotDefined

    actual_func = unwrap(func)
    try:
        sig = _signature(actual_func)
    except Exception:
        return ()

    hints_dict = hints(actual_func)

    arg_objs = []
    for name, param in sig.parameters.items():
        if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY):
            hint = hints_dict.get(name, NotDefined)
            default = NotDefined if param.default is Parameter.empty else param.default
            arg_objs.append(Arg(name=name, hint=hint, default=default))

    return tuple(arg_objs)

@cache
def signature(func: callable) -> Signature:
    from typed.mods.meta.atomic import TYPE
    from typed.mods.err import NotDefined

    target = unwrap(func)

    target_args = args(func)
    hints_dict = hints(target)

    hint_dom = tuple(a.hint for a in target_args if a.hint is not None and a.hint is not NotDefined)
    hint_cod = hints_dict.get('return', None)

    if not isinstance(hint_cod, TYPE):
        hint_cod = None

    orig_dom, orig_cod = (), None

    if hasattr(func, "_dom"):
        orig_dom = func._dom
        orig_cod = getattr(func, "_cod", None)
    elif hasattr(func, "__dict__") and "dom" in func.__dict__:
        orig_dom = func.__dict__["dom"]
        orig_cod = func.__dict__.get("cod", None)
    elif hasattr(target, "__dict__") and "dom" in target.__dict__:
        orig_dom = target.__dict__["dom"]
        orig_cod = target.__dict__.get("cod", None)
    else:
        orig_dom = hint_dom
        orig_cod = hint_cod

    from typed.mods.check import check
    check.hint.dom(func, orig_dom, hint_dom)

    if hint_cod is not None:
        check.hint.cod(func, orig_cod, hint_cod)

    return Signature(
        func=target,
        dom=orig_dom,
        cod=orig_cod,
        args=target_args
    )

def reduce(func, *reduce_args, **reduce_kwargs):
    sig = signature(func)
    new_sig, fixed_values = sig.reduce(*reduce_args, **reduce_kwargs)

    def reduced(*args, **kwargs):
        call_kwargs = dict(fixed_values)
        for i, arg_val in enumerate(args):
            if i < len(new_sig.args):
                call_kwargs[new_sig.args[i].name] = arg_val
        call_kwargs.update(kwargs)

        final_args = []
        final_kwargs = dict(call_kwargs)
        for arg in sig.args:
            if arg.name in final_kwargs:
                final_args.append(final_kwargs.pop(arg.name))

        return func(*final_args, **final_kwargs)

    reduced.__name__ = getattr(func, "__name__", "reduced")
    reduced._dom = new_sig.dom
    reduced._cod = new_sig.cod

    hints_dict = getattr(func, "__annotations__", {}).copy()
    for k in fixed_values:
        if k in hints_dict:
            del hints_dict[k]
    reduced.__annotations__ = hints_dict

    return reduced

__wrap_attrs__ = ["__func__", "__wrapped__", "func", "original_func"]

def unwrap(func: callable, attrs: list[str]=None) -> callable:
    if attrs is None:
        attrs = __wrap_attrs__

    from typed.mods.check import check
    check.iscallable(func)

    current = func
    seen = set()

    while True:
        id_ = id(current)
        if id_ in seen:
            break
        seen.add(id_)

        found = False
        for attr in attrs:
            _func = getattr(current, attr, None)
            if callable(_func):
                current = _func
                found = True
                break

        if not found:
            break

    return current

def func(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Func, LazyFunc
        if lz:
            return LazyFunc(fn, check=check, defaults=defaults, envs=envs)
        return Func(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def hinted(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Hinted, LazyHinted
        if lz:
            return LazyHinted(fn, check=check, defaults=defaults, envs=envs)
        return Hinted(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def typed(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Typed, LazyTyped
        if lz:
            return LazyTyped(fn, check=check, defaults=defaults, envs=envs)
        return Typed(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def condition(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Condition, LazyCondition
        if lz:
            return LazyCondition(fn, check=check, defaults=defaults, envs=envs)
        return Condition(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def family(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Family, LazyFamily
        if lz:
            return LazyFamily(fn, check=check, defaults=defaults, envs=envs)
        return Family(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)

def constructor(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Constructor, LazyConstructor
        if lz:
            return LazyConstructor(fn, check=check, defaults=defaults, envs=envs)
        return Constructor(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)

def prod(f, g):
    def prod_func(args_tuple):
        x, y = args_tuple
        return (f(x), g(y))

    prod_func.__name__ = f"({getattr(f, '__name__', str(f))} x {getattr(g, '__name__', str(g))})"

    from typed.mods.types.constructor import Prod
    from typed.mods.meta.func import Hinted, Typed

    try:
        sig_f = signature(f)
        sig_g = signature(g)

        f_dom = sig_f.dom[0] if sig_f.dom else None
        g_dom = sig_g.dom[0] if sig_g.dom else None

        if f_dom and g_dom and sig_f.cod and sig_g.cod:
            dom_type = Prod(f_dom, g_dom)
            cod_type = Prod(sig_f.cod, sig_g.cod)

            prod_func._dom = (dom_type,)
            prod_func._cod = cod_type

            is_f_typed = getattr(type(f), "__flags__", None) and type(f).__flags__.is_typed
            is_g_typed = getattr(type(g), "__flags__", None) and type(g).__flags__.is_typed
            is_f_hinted = getattr(type(f), "__flags__", None) and type(f).__flags__.is_hinted
            is_g_hinted = getattr(type(g), "__flags__", None) and type(g).__flags__.is_hinted

            if is_f_typed and is_g_typed:
                return Typed(dom_type, cod=cod_type)(prod_func)
            elif is_f_hinted and is_g_hinted:
                return Hinted(dom_type, cod=cod_type)(prod_func)
    except Exception:
        pass

    return prod_func

def coprod(f, g):
    def coprod_func(args_tuple):
        i, val = args_tuple
        if i == 0:
            return (0, f(val))
        elif i == 1:
            return (1, g(val))
        raise ValueError(f"Invalid coproduct index: {i}")

    coprod_func.__name__ = f"({getattr(f, '__name__', str(f))} + {getattr(g, '__name__', str(g))})"

    from typed.mods.types.constructor import Coprod
    from typed.mods.meta.func import Hinted, Typed
    try:
        sig_f = signature(f)
        sig_g = signature(g)

        f_dom = sig_f.dom[0] if sig_f.dom else None
        g_dom = sig_g.dom[0] if sig_g.dom else None

        if f_dom and g_dom and sig_f.cod and sig_g.cod:
            dom_type = Coprod(f_dom, g_dom)
            cod_type = Coprod(sig_f.cod, sig_g.cod)

            coprod_func._dom = (dom_type,)
            coprod_func._cod = cod_type

            is_f_typed = getattr(type(f), "__flags__", None) and type(f).__flags__.is_typed
            is_g_typed = getattr(type(g), "__flags__", None) and type(g).__flags__.is_typed
            is_f_hinted = getattr(type(f), "__flags__", None) and type(f).__flags__.is_hinted
            is_g_hinted = getattr(type(g), "__flags__", None) and type(g).__flags__.is_hinted

            if is_f_typed and is_g_typed:
                return Typed(dom_type, cod=cod_type)(coprod_func)
            elif is_f_hinted and is_g_hinted:
                return Hinted(dom_type, cod=cod_type)(coprod_func)
    except Exception:
        pass

    return coprod_func
