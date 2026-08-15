def get(entity: object, prop: str="", default: object=None, typesystem=None) -> object:
    if default is None:
        from typed.mods.err import NotDefined
        default = NotDefined

    from typed.mods.resolve import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    if not prop:
        return entity

    keys = prop.split('.')
    value = entity

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

def set(entity: object, prop: str, value: object, typesystem=None) -> object:
    from typed.mods.resolve import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    if not prop:
        return entity

    keys = prop.split('.')

    parent_path = '.'.join(keys[:-1])
    target = get(entity, parent_path)

    last_key = keys[-1]
    typ = typesystem.typeof(target)

    if hasattr(typ, "__setitem__"):
        try:
            getattr(typ, "__setitem__")(target, last_key, value)
        except Exception:
            getattr(typ, "__setitem__")(target, int(last_key), value)
    else:
        setattr(target, last_key, value)

    return entity

def has(entity: object, prop: str, value: object=None, typesystem=None) -> object:
    from typed.mods.resolve import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    if not prop:
        return True

    keys = prop.split('.')

    parent_path = '.'.join(keys[:-1])
    target = get(entity, parent_path)

    last_key = keys[-1]
    typ = typesystem.typeof(target)

    if value is not None:
        if hasattr(typ, "__getitem__"):
            try:
                value_ = getattr(typ, "__getitem__")(target, last_key, None)
                return value == value_
            except Exception:
                value_ = getattr(typ, "__getitem__")(target, int(last_key), None)
                return value == value_
    else:
        return hasattr(target, last_key)


class prop:
    def typeof(entity: object, level: int=-1, typesystem=None) -> object:
        from typed.mods.typesystem import typeof as _typeof
        return _typeof(
            entity=entity,
            level=level,
            typesystem=typesystem
        )

    def kindof(entity: object, typesystem=None) -> object:
        from typed.mods.typesystem import kindof as _kindof
        return _kindof(
            entity=entity,
            typesystem=typesystem
        )

    def nameof(*entities: tuple[object], typesystem=None) -> object:
        from typed.mods.typesystem import nameof as _nameof
        return _nameof(
            *entities,
            typesystem=typesystem
        )

    def sizeof(entity: object) -> object:
        from typed.mods.poly import sizeof as _sizeof
        return _sizeof(entity=entity)

    def termsof(entity: object) -> object:
        from typed.mods.poly import termsof as _termsof
        return _termsof(entity=entity)

    def nullof(entity: object) -> object:
        from typed.mods.poly import nullof as _nullof
        return _nullof(entity=entity)

    def get(entity: object, prop: str="", default: object=None, typesystem=None) -> object:
        return get(
            entity=entity,
            prop=prop,
            default=default,
            typesystem=typesystem
        )

    has = has

    class set:
        def __new__(cls, entity, prop, value):
            return globals()["set"](
                entity=entity,
                prop=prop,
                value=value
            )

        @staticmethod
        def nameof(entity, name):
            setattr(entity, "__name__", name)
            setattr(entity, "__display__", name)
            return entity

        @staticmethod
        def typeof(entity, type):
            setattr(entity, "__type__", type)
            return entity

        @staticmethod
        def kindof(entity, kind):
            setattr(entity, "__kind__", kind)
            return entity

        @staticmethod
        def nullof(entity, value):
            setattr(entity, "__null__", value)
            return entity
