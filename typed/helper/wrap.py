from functools import lru_cache as cache

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
