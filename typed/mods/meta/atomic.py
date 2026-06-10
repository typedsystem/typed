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
    The atomic metatype of nothing.

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
    The atomic metatype of everything.

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
    The atomic metatype of None value type.

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
    The atomic metatype of integers.

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
    The atomic metatype of floating-point numbers.

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
    The atomic metatype of strings.

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
    The atomic metatype of booleans.

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
    The atomic metatype of bytes and bytearrays.

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
    The atomic metatype of enumerable types.

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

class FINITE(ENUMERABLE):
    """
    The atomic metatype of finite types.

    kindof(FINITE)    is  meta
    typeof(FINITE)    is  UNIVERSE(1)
    isterm(T, FINITE) iff issub(typeof(T), FINITE)
    nullof(FINITE)    is  NotDefined
    builtin(FINITE)   is  NotDefined
    """
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        if hasattr(trm, '__len__'):
            return True

        b = trm.__builtin__
        from typed.mods.err import NotDefined
        if b is not NotDefined and hasattr(b, '__len__'):
            return True

        return False

class MEMBER(TYPE):
    """
    The atomic metatype of TYPESYSTEM members.

    : kindof(MEMBER)    is  meta
    : typeof(MEMBER)    is  UNIVERSE(1)
    : isterm(T, MEMBER) iff issub(typeof(T), MEMBER)
    : nullof(MEMBER)    is  NotDefined
    : builtin(MEMBER)   is  NotDefined
    """
    def __isterm__(typ, trm):
        from typed.mods.typesystem import ismember
        return ismember(trm)

class DOM(TYPE):
    """
    The atomic metatype of domain types.

    kindof(DOM)    is  meta
    typeof(DOM)    is  UNIVERSE(1)
    isterm(T, DOM) iff issub(typeof(T), DOM)
    nullof(DOM)    is  NotDefined
    builtin(DOM)   is  NotDefined
    """
    def __isterm__(typ, trm):
        if not isinstance(trm, tuple):
            return False

        from typed.mods.err import NotDefined
        types = getattr(trm, "__types__", NotDefined)
        if types is NotDefined or types is None:
            return False

        from typed.mods.typesystem import ismember
        return all(ismember(t) for t in trm)

class COD(MEMBER):
    """
    The atomic metatype of codomain types.

    kindof(COD)    is  meta
    typeof(COD)    is  UNIVERSE(1)
    isterm(T, COD) iff issub(typeof(T), COD)
    nullof(COD)    is  NotDefined
    builtin(COD)   is  NotDefined
    """

class LAZY(TYPE):
    """
    The atomic metatype of lazy types.

    kindof(LAZY)    is  meta
    typeof(LAZY)    is  UNIVERSE(1)
    isterm(T, LAZY) iff issub(typeof(T), COD)
    nullof(LAZY)    is  NotDefined
    builtin(LAZY)   is  NotDefined
    """

    def __new__(mcs, name, bases, dct, **kwargs):
        if "materialize" not in dct and not any(hasattr(b, "materialize") for b in bases):
            from typed.mods.err import TypeErr
            raise TypeErr(message=f"Class '{name}' created from LAZY must implement the method 'materialize'")
        return super().__new__(mcs, name, bases, dct, **kwargs)

    def __isterm__(typ, trm):
        flags = getattr(trm, "__flags__", None)
        is_lazy = getattr(flags, "is_lazy", False) if flags else False
        if is_lazy and hasattr(trm, "materialize"):
            return True
        return False
