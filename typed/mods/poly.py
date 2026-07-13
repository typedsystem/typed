from typing import Any, Callable

class Poly:
    def __new__(self, attr: str, *args, cod=None, typesystem=None, callable: bool=False) -> Callable[..., Any]:
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if (args or cod is not None) or callable is True:
            import builtins

            def __poly__(*call_args: Any, **kwargs: Any) -> Any:
                from typed.mods.err import NotDefined

                if not call_args and not kwargs:
                    raise TypeError(f"Polymorphism '{attr}' requires at least one argument to dispatch.")

                if call_args:
                    entity = call_args[1]
                    user_args = list(call_args[2:])
                else:
                    entity = next((v for v in kwargs.values() if isinstance(v, type)), None)
                    if entity is None:
                        raise TypeError(
                            f"Polymorphism '{attr}' requires at least one type/class to dispatch. "
                            f"Ensure you are passing classes as values (e.g., A=X, not X='A'). Received kwargs: {kwargs}"
                        )
                    user_args = []

                final_args = list(user_args)

                if args:
                    from typed.mods.check import require

                    for i, arg in enumerate(args):
                        if i < len(user_args):
                            val = user_args[i]
                        else:
                            if hasattr(arg, 'default') and arg.default is not NotDefined:
                                val = arg.default
                                final_args.append(val)
                            else:
                                break

                        if hasattr(arg, 'hint') and arg.hint not in (None, NotDefined):
                            require.isterm(val, arg.hint)

                entity_type = typesystem.typeof(entity)
                method = getattr(entity_type, attr, None)
                if method is None:
                    method = getattr(entity, attr, None)

                if method is None:
                    type_name = getattr(entity_type, '__name__', type(entity).__name__)
                    raise AttributeError(f"type '{type_name}' has no attribute '{attr}'")

                if not builtins.callable(method):
                    type_name = getattr(entity_type, '__name__', type(entity).__name__)
                    raise TypeError(f"'{attr}' is not callable on type '{type_name}'")

                res = method(entity, *final_args, **kwargs)

                if cod is not None:
                    from typed.mods.check import require
                    require.isterm(res, cod)

                return res

            __poly__.__name__ = attr
            return __poly__

        def __poly__(*call_args: Any, **kwargs: Any) -> Any:
            f"""
            The '{attr}' parametric polymorphism.
            """
            if not call_args and not kwargs:
                raise TypeError(f"Polymorphism '{attr}' requires at least one argument to dispatch.")

            if call_args:
                entity = call_args[1]
            else:
                entity = next((v for v in kwargs.values() if isinstance(v, type)), None)
                if entity is None:
                    raise TypeError(
                        f"Polymorphism '{attr}' requires at least one type/class to dispatch. "
                        f"Ensure you are passing classes as values (e.g., A=X, not X='A'). Received kwargs: {kwargs}"
                    )

            from typed.mods.err import NotDefined
            return getattr(entity, attr, NotDefined)

        __poly__.__name__ = attr
        return __poly__

prod    = Poly("__prod__",    callable=True)
coprod  = Poly("__coprod__",  callable=True)
include = Poly("__include__", callable=True)
join    = Poly("__join__",    callable=True)
split   = Poly("__split__",   callable=True)
sizeof  = Poly("__size__",    callable=True)
nullof  = Poly("__null__")
displayof  = Poly("__display__")
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
