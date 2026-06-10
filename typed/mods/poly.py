from typed.mods.err import NotDefined

def get(obj: object, what: str="", default: object=NotDefined) -> object:
    keys = entry.split('.')
    value = obj
    for key in keys:
        if isinstance(value, Dict):
            if key not in value:
                return std
            value = value[key]
        elif isinstance(value, List):
            try:
                index = int(key)
            except ValueError:
                return std
            if index < 1 or index >= len(value):
                return std
            value = value[index]
        else:
            return std
    from typed.mods.typesystem import typeof
    if not what:
        return obj

    if len(what) == 1:
        what = what[0]

    getattr_ = getattr(typeof(obj), "")
    if 



def null(obj: object) -> object:
    """
    The 'null' parametric polymorphism.
    """
    from typed.mods.err import NotDefined
    return getattr(obj, "__null__", NotDefined)

def display(obj: object) -> str:
    """
    The 'display' parametric polymorphism.
    """
    from typed.mods.err import NotDefined
    return getattr(obj, "__display__", NotDefined)

def builtin(type: type) -> type:
    """
    The 'builtin' parametric polymorphism.
    """
    from typed.mods.err import NotDefined
    return getattr(type, "__builtin__", NotDefined)

def terms(t: type) -> set:
    """
    The 'terms' polymorphism.
    """
    from typed.mods.err import NotDefined
    __terms__ = getattr(t, "__terms__", NotDefined)
    if __terms__ is not NotDefined:
        return set(__terms__)
    return NotDefined

def append(container, *args, **kwargs):
    if any(
        _is_placeholder_like(x)
        for x in (container, *args, *kwargs.values())
    ):
        def func(*call_args, **call_kwargs):
            obj = _resolve_placeholder_value(container, call_args, call_kwargs)
            if obj is None:
                return None

            resolved_args = [
                _resolve_placeholder_value(a, call_args, call_kwargs)
                for a in args
            ]
            resolved_kwargs = {
                k: _resolve_placeholder_value(v, call_args, call_kwargs)
                for k, v in kwargs.items()
            }
            return _append(obj, *resolved_args, **resolved_kwargs)
        return func
    return _append(container, *args, **kwargs)

def join(*args):
    if any(_is_placeholder_like(a) for a in args):
        def func(*call_args, **call_kwargs):
            resolved = [
                _resolve_placeholder_value(a, call_args, call_kwargs)
                for a in args
            ]
            return _join(*resolved)
        return func
    return _join(*args)

def split(container, *args, **kwargs):
    if any(
        _is_placeholder_like(x)
        for x in (container, *args, *kwargs.values())
    ):
        def func(*call_args, **call_kwargs):
            obj = _resolve_placeholder_value(container, call_args, call_kwargs)
            if obj is None:
                return None

            resolved_args = [
                _resolve_placeholder_value(a, call_args, call_kwargs)
                for a in args
            ]
            resolved_kwargs = {
                k: _resolve_placeholder_value(v, call_args, call_kwargs)
                for k, v in kwargs.items()
            }
            return _split(obj, *resolved_args, **resolved_kwargs)
        return func

    return _split(container, *args, **kwargs)

def poly(attr: str):
    def polymorphic_function(obj, *args, **kwargs):
        obj_type = type(obj)
        if not hasattr(obj_type, attr):
            raise AttributeError(f"type '{obj_type.__name__}' has no attribute '{attr}'")
        method = getattr(obj_type, attr)
        if not callable(method):
            raise TypeError(f"'{attr}' is not callable on type '{obj_type.__name__}'")
        return method(obj, *args, **kwargs)
    return polymorphic_function

convert = poly("__convert__")
