from typed.mods.meta.base import TYPE, UNIVERSE_1

class TUPLE(TYPE):
    """
    The metatype of the dependent type of tuples.

    kindof(TUPLE)    is  meta
    typeof(TUPLE)    is  UNIVERSE(1)
    isterm(T, TUPLE) iff issub(typeof(T), TUPLE)
    nullof(TUPLE)    is  NotDefined
    builtin(TUPLE)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if  not isinstance(trm, tuple) and not issub(typeof(typeof(trm)), TUPLE):
            return False

        types = getattr(typ, '__types__', None)
        if types is not None:
            for x in trm:
                if not any(isterm(x, t) for t in types):
                    return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        if type(other) is type(typ):
            typ_types = getattr(typ, '__types__', None)
            other_types = getattr(other, '__types__', None)
            if typ_types is None and other_types is not None:
                return False
            if other_types is None:
                return True
            for t1 in typ_types:
                if not any(issub(t1, t2) for t2 in other_types):
                    return False
            return True
        return False

    def __call__(typ, *types, typesystem=None):
        from typed.mods.typesystem import names
        from typed.mods.init import TYPESYSTEM
        if typesystem is None:
            typesystem = TYPESYSTEM

        types = set(types)
        if typesystem.is_restrictive:
            from typed.mods.check import check
            check.typesystem(*types, typesystem=typesystem)

        name = f"Tuple({names(*types)})" if types else "Tuple"

        return TUPLE(name, (typ,), {
            "is_type": True,
            "__typesystems__": [typesystem],
            "__display__": name,
            "__types__": types,
        })

    from typed.mods.err import NotDefined
    from typed.mods.init import TYPESYSTEM

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __display__ = "TUPLE"
    __null__ = NotDefined
    __builtin__ = NotDefined


class LIST(TYPE):
    """
    The metatype of lists.

    kindof(LIST)    is meta
    typeof(LIST)    is UNIVERSE(1)
    isterm(T, LIST) iff isinstance(T, list) and elements match types, or issub(typeof(typeof(T)), LIST)
    nullof(LIST)    is NotDefined
    builtin(LIST)   is NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, list) and not issub(typeof(typeof(trm)), LIST):
            return False

        types = getattr(typ, '__types__', None)
        if types is not None:
            for x in trm:
                if not any(isterm(x, t) for t in types):
                    return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        if type(other) is type(typ):
            typ_types = getattr(typ, '__types__', None)
            other_types = getattr(other, '__types__', None)
            if typ_types is None and other_types is not None:
                return False
            if other_types is None:
                return True
            for t1 in typ_types:
                if not any(issub(t1, t2) for t2 in other_types):
                    return False
            return True
        return False

    def __call__(typ, *types, typesystem=None):
        from typed.mods.typesystem import names
        if typesystem is None:
            from typed.mods.init import TYPESYSTEM
            typesystem = TYPESYSTEM

        types = set(types)
        if typesystem.is_restrictive:
            for t in types:
                if t not in typesystem.__types__:
                    raise TypeError(f"Type {t} not in typesystem.__types__")

        name = f"List({names(*types)})" if types else "List"

        return LIST(name, (typ,), {
            "is_type": True,
            "__typesystems__": [typesystem],
            "__display__": name,
            "__types__": types,
        })

    from typed.mods.init import TYPESYSTEM
    from typed.mods.err import NotDefined

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __display__ = "LIST"
    __null__ = NotDefined
    __builtin__ = NotDefined


class SET(TYPE):
    """
    The metatype of sets.

    kindof(SET)    is meta
    typeof(SET)    is UNIVERSE(1)
    isterm(T, SET) iff isinstance(T, set) and elements match types, or issub(typeof(typeof(T)), SET)
    nullof(SET)    is NotDefined
    builtin(SET)   is NotDefined
    """
    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, set) and not issub(typeof(typeof(trm)), SET):
            return False

        types = getattr(typ, '__types__', None)
        if types is not None:
            for x in trm:
                if not any(isterm(x, t) for t in types):
                    return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        if type(other) is type(typ):
            typ_types = getattr(typ, '__types__', None)
            other_types = getattr(other, '__types__', None)
            if typ_types is None and other_types is not None:
                return False
            if other_types is None:
                return True
            for t1 in typ_types:
                if not any(issub(t1, t2) for t2 in other_types):
                    return False
            return True
        return False

    def __call__(typ, *types, typesystem=None):
        from typed.mods.typesystem import names
        if typesystem is None:
            typesystem = TYPESYSTEM

        types = set(types)
        if typesystem.is_restrictive:
            for t in types:
                if t not in typesystem.__types__:
                    raise TypeError(f"Type {t} not in typesystem.__types__")

        name = f"Set({names(*types)})" if types else "Set()"

        return type.__new__(typ.__class__, name, (typ,), {
            "__display__": name,
            "__types__": types,
            "__typesystems__": [typesystem],
            "is_type": True
        })

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "SET"
    __null__ = NotDefined
    __builtin__ = NotDefined


class DICT(TYPE):
    """
    The metatype of dictionaries.

    kindof(DICT)    is meta
    typeof(DICT)    is UNIVERSE(1)
    isterm(T, DICT) iff isinstance(T, dict) and its keys/values match types, or issub(typeof(typeof(T)), DICT)
    nullof(DICT)    is NotDefined
    builtin(DICT)   is NotDefined
    """
    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, dict) and not issub(typeof(typeof(trm)), DICT):
            return False

        types = getattr(typ, "__types__", None)
        key_type = getattr(typ, "__key_type__", None)

        if types is not None:
            for v in trm.values():
                if not any(isterm(v, t) for t in types):
                    return False

        if key_type is not None:
            for k in trm.keys():
                if not isterm(k, key_type):
                    return False

        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        if type(other) is type(typ):
            typ_types = getattr(typ, '__types__', None)
            other_types = getattr(other, '__types__', None)
            typ_key = getattr(typ, '__key_type__', None)
            other_key = getattr(other, '__key_type__', None)

            if typ_types is None and other_types is not None:
                return False
            if typ_key is None and other_key is not None:
                return False

            if typ_types is not None and other_types is not None:
                for t1 in typ_types:
                    if not any(issub(t1, t2) for t2 in other_types):
                        return False

            if typ_key is not None and other_key is not None:
                if not issub(typ_key, other_key):
                    return False

            return True
        return False

    def __call__(typ, *types, key=None, typesystem=None):
        from typed.mods.typesystem import names, nameof
        if typesystem is None:
            typesystem = TYPESYSTEM

        types = set(types)
        if typesystem.is_restrictive:
            for t in types:
                if t not in typesystem.__types__:
                    raise TypeError(f"Type {t} not in typesystem.__types__")
            if key is not None and key not in typesystem.__types__:
                raise TypeError(f"Type {key} not in typesystem.__types__")

        if key is not None:
            name = f"Dict({names(*types)}, key={nameof(key)})" if types else f"Dict(key={nameof(key)})"
        else:
            name = f"Dict({names(*types)})" if types else "Dict"

        return TYPE(typ.__class__, name, (typ,), {
            "__display__": name,
            "__types__": types,
            "__key_type__": key,
            "__typesystems__": [typesystem],
            "is_type": True
        })

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "DICT"
    __null__ = NotDefined
    __builtin__ = NotDefined


class EXTENSIONAL(TYPE):
    def __isterm__(typ, trm):
        quantifier = getattr(typ, "__quantifier__", None)
        types = tuple(getattr(typ, "__types__", (typ,)))
        from typed.mods.core import isterm
        return isterm(trm, *types, quantifier=quantifier)

    def __issub__(typ, other):
        quantifier = getattr(typ, "__quantifier__", None)
        types = (t for t in getattr(typ, "__types__", (typ,)))
        others = (o for o in getattr(other, "__types__", (other,)))
        from typed.mods.core import issub
        if getattr(other, "is_extensional", False):
            return quantifier(issub(o, *types, quantifier=quantifier) for o in others)
        return issub(other, *types, quantifier=quantifier)

    def __call__(met, *types, base=None, quantifier=None, typesystem=None):
        if not isinstance(base, type):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=EXTENSIONAL.__call__,
                arg=base,
                expected=type,
                received=type(base)
            )
        from typed.mods.core import Quantifier
        if not isinstance(quantifier, Quantifier):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=EXTENSIONAL.__call__,
                arg=quantifier,
                expected=Quantifier,
                received=type(quantifier)
            )

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(quantifier)

        types = set(types)

        for t in types:
            if not isinstance(t, type):
                raise TypeErr(
                    term=EXTENSIONAL.__call__,
                    arg=t,
                    expected=type,
                    received=type(t)
                )
            typesystem.check(t)

        if not types:
            return base

        if len(types) == 1:
            return tuple(types)[0]

        from typed.mods.err import NotDefined
        from typed.mods.core import names

        name = f"Union({names(*types)})"

        return TYPE.__call__(name, tuple(types), {
            'is_type': True,
            'is_parametric': True,
            'is_extensional': True,
            '__display__': name,
            '__types__': types,
            '__null__': NotDefined
        })


class UNION(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.core import isterm, some
        return any(isterm(trm, t) for t in getattr(typ, "__types__", set()))

    def __issub__(typ, other):
        from typed.mods.core import issub, some
        types = getattr(typ, "__types__", set())
        others = getattr(other, "__types__", set())

        if getattr(other, "is_union", False):
            if others:
                return any(issub(o, *types) for o in others)
            return True
        return issub(other, *types)

    def __call__(met, *types, typesystem=None):
        types = set(types)

        if not types:
            from typed.mods.types.base import Empty
            return Empty

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(*tuple(types))

        if len(types) == 1:
            return types[0]

        from typed.mods.err import NotDefined
        from typed.mods.core import names

        name = f"Union({names(*types)})"

        return TYPE.__call__(name, tuple(types), {
            'is_type': True,
            'is_union': True,
            'is_parametric': True,
            '__display__': name,
            '__types__': types,
            '__null__': NotDefined
        })

class INTER(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.core import isterm
        return all(isterm(trm, t) for t in getattr(typ, "__types__", set()))

    def __issub__(typ, other):
        from typed.mods.core import issub
        types = getattr(typ, "__types__", set())
        others = getattr(other, "__types__", set())

        if getattr(other, "is_union", False):
            if others:
                return any(issub(o, *types) for o in others)
            return True
        return issub(other, *types)

    def __call__(met, *types, typesystem=None):
        types = set(types)

        if not types:
            from typed.mods.types.base import Empty
            return Empty

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(*tuple(types))

        if len(types) == 1:
            return types[0]

        from typed.mods.err import NotDefined
        from typed.mods.core import names

        name = f"Union({names(*types)})"

        return TYPE.__call__(name, tuple(types), {
            'is_type': True,
            'is_union': True,
            'is_parametric': True,
            '__display__': name,
            '__types__': types,
            '__null__': NotDefined
        })

class PROD(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.core import isterm
        if not isterm(trm, tuple):
            return False
        if len(trm) != len(typ.__types__):
            return False
        return all(isterm(x, t) for x, t in zip(trm, typ.__types__))

    def __issub__(typ, other):
        from typed.mods.core import issub
        types = getattr(typ, "__types__", set())
        others = getattr(other, "__types__", set())

        if getattr(other, "is_prod", False):
            if not types: return True
            if not others: return False
            if len(types) != len(others): return False

            return all(issub(others[i], types[i]) for i in range(0, len(types)))

        return False

    def __call__(met, *types, typesystem=None):
        if not types:
            from typed.mods.types.base import Tuple
            return Tuple

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(*tuple(types))

        if len(types) == 1:
            return types[0]

        from typed.mods.core import names, null
        from typed.mods.err import NotDefined

        name = f"Prod({names(*types)})"
        nulls = tuple(null(t) for t in types if null(t) is not NotDefined)

        return TYPE.__call__(name, types, {
            'is_type': True,
            'is_parametric': True,
            'is_prod': True,
            '__display__': name,
            '__types__': types,
            '__null__': nulls if len(nulls) == len(types) else NotDefined
        })


