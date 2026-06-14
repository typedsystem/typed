class Poly:
    def __new__(self, attr: str, *args, cod=None, typesystem=None, callable: bool=False):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if (args or cod is not None) or callable is True:
            import builtins

            def __poly__(entity, *call_args):
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

                entity_type = typesystem.typeof(entity)
                if not hasattr(entity_type, attr):
                    raise AttributeError(f"type '{entity_type.__name__}' has no attribute '{attr}'")

                method = getattr(entity_type, attr)
                if not builtins.callable(method):
                    raise TypeError(f"'{attr}' is not callable on type '{entity_type.__name__}'")

                res = method(entity, *final_args)

                if cod is not None:
                    from typed.mods.check import check
                    check.isterm(res, cod)

                return res

            __poly__.__name__ = attr
            return __poly__

        def __poly__(entity: object) -> object:
            f"""
            The '{attr}' parametric polymorphism.
            """
            from typed.mods.err import NotDefined
            return getattr(entity, attr, NotDefined)

        __poly__.__name__ = attr
        return __poly__

prod    = Poly("__prod__",    callable=True)
coprod  = Poly("__coprod__",  callable=True)
include = Poly("__include__", callable=True)
join    = Poly("__join__",    callable=True)
split   = Poly("__split__",   callable=True)
nullof  = Poly("__null__")
sizeof  = Poly("__size__")
builtin = Poly("__builtin__")

def termsof(entity: object) -> set:
    """
    The 'terms' polymorphism.
    """
    from typed.mods.err import NotDefined
    __terms__ = getattr(entity, "__terms__", NotDefined)
    if __terms__ is not NotDefined:
        return set(__terms__)
    return NotDefined
