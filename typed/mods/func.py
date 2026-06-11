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
        from inspect import signature as _signature
        sig = _signature(self.func)
        b = sig.bind(*args, **kwargs)
        b.apply_defaults()
        return b

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
    from typed.mods.general import _

    target = unwrap(func)

    target_args = args(func)
    hints_dict = hints(target)

    hint_dom = tuple(a.hint for a in target_args if a.hint is not None and a.hint is not NotDefined)
    has_return_hint = 'return' in hints_dict
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

    if has_return_hint:
        check.hint.cod(func, orig_cod, hint_cod)

    dom, cod = (), None

    if hasattr(func, "bound_args"):
        param_names = [a.name for a in target_args]
        if not param_names:
            remaining = [
                t for arg, t in zip(func.bound_args, orig_dom)
                if arg is _
            ]
            dom = tuple(remaining)
        else:
            remaining_types = []
            for idx, (name, typ) in enumerate(zip(param_names, orig_dom)):
                pos_bound = idx < len(func.bound_args) and func.bound_args[idx] is not _
                kw_bound = name in getattr(func, "bound_kwargs", {})
                if not pos_bound and not kw_bound:
                    remaining_types.append(typ)
            dom = tuple(remaining_types)
        cod = orig_cod
    else:
        dom = orig_dom
        cod = orig_cod

    return Signature(
        func=target,
        dom=dom,
        cod=cod,
        args=target_args
    )

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
