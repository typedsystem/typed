from typed.mods.init import TYPESYSTEM, UNIVERSE, ABSTRACT

UNIVERSE_1 = UNIVERSE(1, typesystem=TYPESYSTEM)

TYPE = UNIVERSE(0, typesystem=TYPESYSTEM)
TYPE.__name__ = "TYPE"
TYPE.__display__ = TYPE.__name__

META = ABSTRACT(0, typesystem=TYPESYSTEM)
META.__name__ = "META"
META.__display__ = META.__name__

class EMPTY(TYPE):
    """
    The metatype of nothing.

    : kindof(EMPTY)    is  meta
    : typeof(EMPTY)    is  UNIVERSE(1)
    : isterm(T, EMPTY) iff issub(typeof(T), EMPTY)
    : nullof(EMPTY)    is  NotDefined
    : builtin(EMPTY)   is  NotDefined
    """
    __terms__ = {}

    def __isterm__(typ, trm):
        return False

    def __issub__(typ, other):
        return False

    def __issup__(typ, other):
        return True

class ANY(TYPE):
    """
    The metatype of everything.

    kindof(ANY)     is  meta
    typeof(ANY)     is  UNIVERSE(1)
    isterm(T, ANY)  iff issub(typeof(T), ANY)
    nullof(ANY)     is  NotDefined
    builtin(ANY)    is  NotDefined
    """
    def __isterm__(typ, trm):
        return True

    def __issub__(typ, other):
        return True

    def __issup__(typ, other):
        return False

class NILL(TYPE):
    """
    The metatype of None value type.

    : kindof(NILL)    is  meta
    : typeof(NILL)    is  UNIVERSE(1)
    : isterm(T, NILL) iff issub(typeof(T), NILL)
    : nullof(NILL)    is  NotDefined
    : builtin(NILL)   is  NotDefined
    """
    def __isterm__(typ, trm):
        return trm is None

class INT(TYPE):
    """
    The metatype of integers.

    : kindof(INT)    is  meta
    : typeof(INT)    is  UNIVERSE(1)
    : isterm(T, INT) iff issub(typeof(T), INT)
    : nullof(INT)    is  NotDefined
    : builtin(INT)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, int) or issub(typeof(typeof(trm)), INT)

class FLOAT(TYPE):
    """
    The metatype of floating-point numbers.

    kindof(FLOAT)    is  meta
    typeof(FLOAT)    is  UNIVERSE(1)
    isterm(T, FLOAT) iff issub(typeof(T)), FLOAT)
    nullof(FLOAT)    is  NotDefined
    builtin(FLOAT)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, float) or issub(typeof(typeof(trm)), FLOAT)

class STR(TYPE):
    """
    The metatype of strings.

    kindof(STR)    is  meta
    typeof(STR)    is  UNIVERSE(1)
    isterm(T, STR) iff issub(typeof(T), STR)
    nullof(STR)    is  NotDefined
    builtin(STR)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, str) or issub(typeof(typeof(trm)), STR)

class BOOL(TYPE):
    """
    The metatype of booleans.

    kindof(BOOL)    is  meta
    typeof(BOOL)    is  UNIVERSE(1)
    isterm(T, BOOL) iff issub(typeof(T), BOOL)
    nullof(BOOL)    is  NotDefined
    builtin(BOOL)   is  NotDefined
    """

    __terms__ = frozenset({True, False})

    def __iter__(typ):
        yield True
        yield False

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, bool) or issub(typeof(typeof(trm)), BOOL)

class BYTE(TYPE):
    """
    The metatype of bytes and bytearrays.

    kindof(BYTE)    is  meta
    typeof(BYTE)    is  UNIVERSE(1)
    isterm(T, BYTE) iff issub(typeof(T), BYTE)
    nullof(BYTE)    is  NotDefined
    builtin(BYTE)   is  NotDefined
    """
    def __isterm__(typ, trm):
        from builtins import bytes, bytearray
        from typed.mods.typesystem import typeof, issub
        return isinstance(trm, (bytes, bytearray)) or issub(typeof(typeof(trm)), BYTE)

class ENUMERABLE(TYPE):
    """
    The metatype of enumerable types.

    kindof(ENUMERABLE)    is  meta
    typeof(ENUMERABLE)    is  UNIVERSE(1)
    isterm(T, ENUMERABLE) iff issub(typeof(T), ENUMERABLE)
    nullof(ENUMERABLE)    is  NotDefined
    builtin(ENUMERABLE)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import istype, issub
        if not istype(trm):
            return False
        from typed.mods.logic import Discourse
        return issub(trm, Discourse)

    def __issub__(typ, other):
        from typed.mods.flags import flag, flagged
        return flagged(other, flag.is_enumerable)
