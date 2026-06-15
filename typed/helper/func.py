from functools import lru_cache as cache

def _reduce_args(sig_args, *args, **kwargs):
    from typed.mods.err import NotDefined
    arguments = {}
    for i, arg in enumerate(sig_args):
        if i < len(args):
            arguments[arg.name] = args[i]
        elif arg.name in kwargs:
            arguments[arg.name] = kwargs[arg.name]
        elif arg.default is not NotDefined:
            arguments[arg.name] = arg.default
    return arguments

def _repr_arg(x):
    if x is Ellipsis: return "..."
    return repr(x)

@cache
def _unwrap_cache(func: callable, attrs: tuple) -> callable:
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
