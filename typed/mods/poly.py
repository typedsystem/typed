class Poly:
    def __new__(self, attr: str, *args, cod=None, typesystem=None, callable: bool=False):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if (args or cod is not None) or callable is True:
            import builtins

            def __poly__(obj, *call_args):
                from typed.mods.err import NotDefined

                final_args = list(call_args)

                if args:
                    from typed.mods.check import check

                    for i, arg in enumerate(args):
                        if i < len(call_args):
                            val = call_args[i]
                        else:
                            if hasattr(arg, 'default') and arg.default is not NotDefined:
                                val = arg.default
                                final_args.append(val)
                            else:
                                break

                        if hasattr(arg, 'hint') and arg.hint not in (None, NotDefined):
                            check.isterm(val, arg.hint)

                obj_type = typesystem.typeof(obj)
                if not hasattr(obj_type, attr):
                    raise AttributeError(f"type '{obj_type.__name__}' has no attribute '{attr}'")

                method = getattr(obj_type, attr)
                if not builtins.callable(method):
                    raise TypeError(f"'{attr}' is not callable on type '{obj_type.__name__}'")

                res = method(obj, *final_args)

                if cod is not None:
                    from typed.mods.check import check
                    check.isterm(res, cod)

                return res

            __poly__.__name__ = attr
            return __poly__

        def __poly__(obj: object) -> object:
            f"""
            The '{attr}' parametric polymorphism.
            """
            from typed.mods.err import NotDefined
            return getattr(obj, attr, NotDefined)

        __poly__.__name__ = attr
        return __poly__

prod    = Poly("__prod__",   callable=True)
coprod  = Poly("__coprod__", callable=True)
null    = Poly("__null__")
display = Poly("__display__")
builtin = Poly("__display__")

def get(obj: object, what: str="", default: object=None, typesystem=None) -> object:
    if default is None:
        from typed.mods.err import NotDefined
        default = NotDefined

    from typed.mods.resolve import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    if not what:
        return obj

    keys = what.split('.')
    value = obj

    for key in keys:
        typ = typesystem.typeof(value)

        if hasattr(typ, "__get__"):
            try:
                value = getattr(typ, "__get__")(value, key)
            except Exception:
                return default

        elif hasattr(typ, "__getitem__"):
            try:
                value = getattr(typ, "__getitem__")(value, key)
            except Exception:
                try:
                    value = getattr(typ, "__getitem__")(value, int(key))
                except Exception:
                    return default

        else:
            try:
                value = getattr(value, key)
            except AttributeError:
                return default

    return value

def terms(type: object) -> set:
    """
    The 'terms' polymorphism.
    """
    from typed.mods.err import NotDefined
    __terms__ = getattr(type, "__terms__", NotDefined)
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
