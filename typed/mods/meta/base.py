from typed.mods.init import TYPESYSTEM, UNIVERSE, ABSTRACT
from typed.mods.err import NotDefined

UNIVERSE_1 = UNIVERSE(1, typesystem=TYPESYSTEM)

TYPE = UNIVERSE(0, typesystem=TYPESYSTEM)
TYPE.__name__ = "TYPE"
TYPE.__display__ = TYPE.__name__
TYPE.__null__ = NotDefined
TYPE.__builtin__ = NotDefined

META = ABSTRACT(0, typesystem=TYPESYSTEM)
META.__name__ = "META"
META.__display__ = META.__name__
META.__null__ = NotDefined
META.__builtin__ = NotDefined

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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "EMPTY"
    __null__        = NotDefined
    __builtin__     = NotDefined

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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "ANY"
    __null__        = NotDefined
    __builtin__     = NotDefined

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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "NILL"
    __null__        = NotDefined
    __builtin__     = NotDefined

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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "INT"
    __null__        = NotDefined
    __builtin__     = NotDefined


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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,} 
    __display__     = "FLOAT"
    __null__        = NotDefined
    __builtin__     = NotDefined


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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "STR"
    __null__        = NotDefined
    __builtin__     = NotDefined


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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "BOOL"
    __null__        = NotDefined
    __builtin__     = NotDefined


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

    __kind__        = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __display__     = "BYTE"
    __null__        = NotDefined
    __builtin__     = NotDefined
