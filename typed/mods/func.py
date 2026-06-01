from functools import lru_cache as cache
from inspect import Signature

@cache
def Dom(typesystem=TYPESYSTEM):
    class DOM(TYPE):
        def __instancecheck__(cls, instance):
            t = typeof(instance, typesystem)
            if not issub(t, Tuple):
                return False

            types = getattr(t, "__types__", NotDefined)
            if types is NotDefined or types is None:
                return False
            return all(y in typesystem for y in types)

    return DOM("Dom", (TYPE,), {"__display__": "Dom", "__typesystems__": [typesystem]})

@cache
def Cod(typesystem=TYPESYSTEM):
    class COD(TYPE):
        def __instancecheck__(cls, instance):
            return instance in typesystem

    return COD("Cod", (TYPE,), {"__display__": "Cod", "__typesystems__": [typesystem]})

@cache
def signature(func) -> Signature:
    from inspect import signature as _signature
    return _signature(func)

@cache
def hints(func):
    from typing import get_type_hints
    return get_type_hints(func)

__wrap_attrs__ = ["wrapped", "__wrapped__", "_wrapped", "func", "__func__", "_funsc"]

def unwrap(func: callable, attrs: list[str]=__wrap_attrs__) -> callable:
    from typed.mods.check import check

    check.isinstance(func, callable)

    seen = set()
    for attr in attrs:
        id_ = id(func)
        if id_ in seen: break
        seen.add(id_)
        _func = getattr(func, attr, None)
        if isinstance(_func, callable):
            func = _func

    return func
