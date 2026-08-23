class Poly:
    def __new__(
        self, 
        attr: str, 
        *args, 
        cod=None, 
        typesystem=None, 
        callable: bool=False, 
        homogeneous: bool=False
    ):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if (args or cod is not None) or callable is True:
            import builtins

            def __poly__(*call_args, **kwargs):
                from typed.mods.err import NotDefined

                if not call_args and not kwargs:
                    raise TypeError(f"Polymorphism '{attr}' requires at least one argument to dispatch.")

                if call_args:
                    entity = call_args[0]
                    user_args = list(call_args[1:])
                else:
                    entity = next((v for v in kwargs.values() if isinstance(v, type)), None)
                    if entity is None:
                        raise TypeError(
                            f"Polymorphism '{attr}' requires at least one type/class to dispatch. "
                            f"Ensure you are passing classes as values (e.g., A=X, not X='A'). Received kwargs: {kwargs}"
                        )
                    user_args = []

                if homogeneous:
                    from typed.mods.typesystem import typeof, issub
                    entity_type = typeof(
                        entity=entity, 
                        typesystem=typesystem
                    )
                    for a in user_args:
                        arg_type = typeof(
                            entity=a, 
                            typesystem=typesystem
                        )
                        if not issub(arg_type, entity_type, typesystem=typesystem):
                            raise TypeError(
                                f"Polymorphism '{attr}' requires homogeneous term types. "
                                f"Expected subtype of {getattr(entity_type, '__display__', entity_type)}, "
                                f"got {getattr(arg_type, '__display__', arg_type)}."
                            )

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
                            require.isterm(
                                term=val, 
                                types=(arg.hint,)
                            )

                entity_type = typesystem.typeof(entity)
                method = getattr(
                    entity_type,
                    attr,
                    None
                )

                if method is None:
                    method = getattr(
                        entity,
                        attr,
                        None
                    )

                if method is None:
                    type_name = getattr(
                        entity_type,
                        '__name__',
                        type(entity).__name__
                    )
                    raise AttributeError(f"type '{type_name}' has no attribute '{attr}'")

                if not builtins.callable(method):
                    type_name = getattr(
                        entity_type,
                        '__name__',
                        type(entity).__name__
                    )
                    raise TypeError(f"'{attr}' is not callable on type '{type_name}'")

                res = method(
                    entity,
                    *final_args,
                    **kwargs
                )
                if cod is not None:
                    from typed.mods.check import require
                    require.isterm(
                        term=res, 
                        types=(cod,)
                    )

                return res

            __poly__.__name__ = attr
            return __poly__

        def __poly__(*call_args, **kwargs):
            if not call_args and not kwargs:
                raise TypeError(f"Polymorphism '{attr}' requires at least one argument to dispatch.")
            if call_args:
                entity = call_args[0]
            else:
                entity = next((v for v in kwargs.values() if isinstance(v, type)), None)
                if entity is None:
                    raise TypeError(
                        f"Polymorphism '{attr}' requires at least one type/class to dispatch. "
                        f"Ensure you are passing classes as values (e.g., A=X, not X='A'). Received kwargs: {kwargs}"
                    )
            from typed.mods.err import NotDefined
            return getattr(
                entity,
                attr,
                NotDefined
            )
        __poly__.__name__ = attr
        return __poly__

prod    = Poly("__prod__",    callable=True)
coprod  = Poly("__coprod__",  callable=True)
join    = Poly("__join__",    callable=True, homogeneous=True)
split   = Poly("__split__",   callable=True, homogeneous=True)
sizeof  = Poly("__size__",    callable=True)
include = Poly("__include__", callable=True)
remove  = Poly("__remove__", callable=True)

def flatten(*args, **kwargs):
    try:
        return Poly(
        attr="__flatten__",
        callable=True,
        homogeneous=True
    )
    except AttributeError as e:
        if "__flatten__" not in str(e):
            raise

    if not args:
        raise TypeError("Polymorphism '__flatten__' requires at least one argument to dispatch.")

    entity = args[0]
    depth = args[1] if len(args) > 1 else kwargs.pop("depth", 0)

    if depth < 0:
        return entity

    try:
        if isinstance(entity, dict):
            iterator = iter(entity.values())
        else:
            iterator = iter(entity)
    except TypeError:
        from typed.mods.err import Err
        raise Err(
            message=f"Cannot flatten non-iterable term: {entity}"
        )

    try:
        first = next(iterator)
    except StopIteration:
        from typed.mods.err import Err, NotDefined
        null_val = nullof(entity)
        if null_val is NotDefined:
            raise Err(
                message="Cannot flatten empty term without a defined null value"
            )
        return null_val

    try:
        reduced = join(
            first,
            *list(iterator)
        )
    except (TypeError, AttributeError):
        return entity

    if depth == 0:
        return flatten(
            reduced,
            depth=0,
            **kwargs
        )

    if depth <= 1:
        return reduced

    return flatten(
        reduced,
        depth=depth - 1,
        **kwargs
    )

def unflatten(*args, **kwargs):
    try:
        return Poly(
        attr="__unflatten__",
        callable=True,
        homogeneous=True
    )

    except AttributeError as e:
        if "__unflatten__" not in str(e):
            raise

    if not args:
        raise TypeError("Polymorphism '__unflatten__' requires at least one argument to dispatch.")

    entity = args[0]
    depth = args[1] if len(args) > 1 else kwargs.pop("depth", 1)

    if depth < 0:
        return entity

    try:
        expanded = split(
            entity,
            **kwargs
        )
    except (TypeError, AttributeError):
        return entity

    if depth == 0:
        if expanded == entity or expanded == [entity]:
            return expanded
        if isinstance(expanded, dict):
            return type(expanded)({
                k: unflatten(
                    v,
                    depth=0,
                    **kwargs
                )
                for k, v in expanded.items()
            })
        return type(expanded)(
            unflatten(
                e,
                depth=0,
                **kwargs
            )
            for e in expanded
        )

    if depth <= 1:
        return expanded

    if isinstance(expanded, dict):
        return type(expanded)({
            k: unflatten(
                v,
                depth=depth - 1,
                **kwargs
            )
            for k, v in expanded.items()
        })

    return type(expanded)(
        unflatten(
            e,
            depth=depth - 1,
            **kwargs
        )
        for e in expanded
    )

from typed.mods.types.atomic import Str

serialize = Poly("__serialize__", cod=Str, callable=True)
parse = Poly("__parse__", Str, callable=True)

nullof  = Poly("__null__")
displayof  = Poly("__display__")
builtinof = Poly("__builtin__")

def termsof(entity: object) -> set:
    """
    The 'terms' polymorphism.
    """
    from typed.mods.err import NotDefined
    __terms__ = getattr(entity, "__terms__", NotDefined)
    if __terms__ is not NotDefined:
        return set(__terms__)
    return NotDefined

class poly:
    join = join
    split = split
    flatten = flatten
    unflatten = unflatten
    prod = prod
    coprod = coprod
    include = include
    remove = remove
