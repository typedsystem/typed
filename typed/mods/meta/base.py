from typed.mods.init import TYPESYSTEM, UNIVERSE, ABSTRACT
from typed.mods.err import NotDefined

UNIVERSE_1 = UNIVERSE(1)

TYPE = UNIVERSE(0)
TYPE.__name__ = "TYPE"
TYPE.__display__ = TYPE.__name__
TYPE.__builtin__ = NotDefined

META = ABSTRACT(0)
META.__name__ = "META"
META.__display__ = META.__name__
META.__builtin__ = NotDefined

class EMPTY(TYPE):
    """
    The metatype of nothing.

    type(EMTPY) is UNIVERSE(1)
    """
    __terms__ = {}

    def __isterm__(typ, trm):
        return False

    def __issub__(typ, other):
        return True

    def __issup__(typ, other):
        return False

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE(1)
    __display__ = "EMPTY"
    __null__ = NotDefined
    __builtin__ = NotDefined

class PARAMETRIC(TYPE):
    """
    The metatype of parametric types.

    """
    def __isterm__(typ, trm):
        from typed.mods.types.func import Factory
        from typed.mods.typesystem import type
        if hasattr(type(trm), "__call__"):
            return type(trm).__iter__ in Factory
        return False

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "PARAMETRIC"
    __null__    = NotDefined
    __builtin__ = NotDefined

class NILL(TYPE):
    """
    The metatype of None value.
    """
    def __isterm__(typ, trm):
        return trm is None

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "NILL"
    __null__ = NotDefined
    __builtin__ = NotDefined

class ANY(TYPE):
    """
    The metatype of any value.
    """
    def __isterm__(typ, trm):
        return True

    def __issub__(typ, other):
        return True

    def __issup__(typ, other):
        return False

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "ANY"
    __null__ = NotDefined
    __builtin__ = NotDefined


class INT(TYPE):
    """
    The metatype of integers.
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, int) or issub(typeof(typeof(trm)), INT)

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "INT"
    __null__ = NotDefined
    __builtin__ = NotDefined


class FLOAT(TYPE):
    """
    The metatype of floating-point numbers.
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, float) or issub(typeof(typeof(trm)), FLOAT)

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "FLOAT"
    __null__ = NotDefined
    __builtin__ = NotDefined


class STR(TYPE):
    """
    The metatype of strings.
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, str) or issub(typeof(typeof(trm)), STR)

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "STR"
    __null__ = NotDefined
    __builtin__ = NotDefined


class BOOL(TYPE):
    """
    The metatype of booleans.
    """

    __terms__ = frozenset({True, False})

    def __iter__(typ):
        yield True
        yield False

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, bool) or issub(typeof(typeof(trm)), BOOL)

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "BOOL"
    __null__ = NotDefined
    __builtin__ = NotDefined


class BYTES(TYPE):
    """
    The metatype of bytes and bytearrays.
    """

    def __isterm__(typ, trm):
        from builtins import bytes, bytearray
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, (bytes, bytearray)) or issub(typeof(typeof(trm)), BYTES)

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "BYTES"
    __null__ = NotDefined
    __builtin__ = NotDefined


class TUPLE(TYPE):
    """
    The metatype of tuples.
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
        if typesystem is None:
            typesystem = TYPESYSTEM

        types = set(types)
        if typesystem.is_restrictive:
            for t in types:
                if t not in typesystem.__types__:
                    raise TypeError(f"Type {t} not in typesystem.__types__")

        name = f"Tuple({names(*types)})" if types else "Tuple"

        return TYPE(name, (typ,), {
            "__display__": name,
            "__types__": types,
            "__typesystems__": [typesystem],
            "is_type": True
        })

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "TUPLE"
    __null__ = NotDefined
    __builtin__ = NotDefined


class LIST(TYPE):
    """
    The metatype of lists.
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
            typesystem = TYPESYSTEM

        types = set(types)
        if typesystem.is_restrictive:
            for t in types:
                if t not in typesystem.__types__:
                    raise TypeError(f"Type {t} not in typesystem.__types__")

        name = f"List({names(*types)})" if types else "List"

        return type.__new__(typ.__class__, name, (typ,), {
            "__display__": name,
            "__types__": types,
            "__typesystems__": [typesystem],
            "is_type": True
        })

    is_meta = True
    __typesystems__ = [TYPESYSTEM]
    __type__ = UNIVERSE_1
    __display__ = "LIST"
    __null__ = NotDefined
    __builtin__ = NotDefined


class SET(TYPE):
    """
    The metatype of sets.
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

TYPESYSTEM.add(
    EMPTY, PARAMETRIC, ANY,
    NILL, INT, FLOAT, STR, BOOL, BYTES,
    TUPLE, LIST, SET, DICT
)
