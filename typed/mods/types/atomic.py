from typed.mods.meta.atomic import (
    EMPTY, NILL, ANY,
    TYPE, META,
    ENUMERABLE, FINITE,
    STR, INT, FLOAT, BOOL, BYTE,
    MEMBER, DOM, COD
)

class Empty(metaclass=EMPTY):
    """
    The atomic type with no terms

    : kindof(Empty)    is  type
    : typeof(Empty)    is  EMPTY
    : isterm(x, Empty) :=  False
    : nullof(Empty)    is  NotDefined
    : builtin(Empty)   is  NotDefined
    """

class Nill(metaclass=NILL):
    """
    The atomic type of the None value

    : kindof(Empty)   is  type
    : typeof(Nill)    is  NILL
    : isterm(x, Nill) iff x is None
    : nullof(Nill)    is  None
    : builtin(Nill)   is  NotDefined
    """
    __null__ = None

class Any(metaclass=ANY):
    """
    The atomic type of anything

    : kindof(Empty)  is  type
    : typeof(Any)    is ANY
    : isterm(x, Any) := True
    : issub(T, Any)  iff issub(typeof(T), ANY)
    : nullof(Any)    is None
    : builtin(Any)   is NotDefined
    """
    __null__        = None

class Type(metaclass=TYPE):
    """
    The atomic type of all types

    : kindof(Type)    is  type
    : typeof(Type)    is  TYPE := UNIVERSE(0)
    : isterm(x, Type) iff issub(typeof(x), Type)
    : nullof(Type)    is  Nill
    : builtin(Type)   is  type
    """
    __null__        = Nill
    __builtin__     = type

class Meta(metaclass=META):
    """
    The atomic type of all metaypes

    : kindof(Meta)    is  type
    : typeof(Meta)    is  META := ABSTRACT(0)
    : isterm(x, Meta) iff issub(typeof(x), Meta)
    : nullof(Meta)    is  NotDefined
    : builtin(Meta)   is  NotDefined
    """

class Enumerable(metaclass=ENUMERABLE):
    """
    The atomic type of all enumerable types.

    : kindof(Enumerable)    is  type
    : typeof(Enumerable)    is  ENUMERABLE
    : isterm(x, Enumerable) iff issub(typeof(x), Enumerable)
    : nullof(Enumerable)    is  NotDefined
    : builtin(Enumerable)   is  NotDefined
    """

class Finite(metaclass=FINITE):
    """
    The atomic type of all finite types.

    : kindof(Finite)    is  type
    : typeof(Finite)    is  FINITE
    : isterm(x, Finite) iff issub(typeof(x), Finite)
    : nullof(Finite)    is  NotDefined
    : builtin(Finite)   is  NotDefined
    """

class Int(metaclass=INT):
    """
    The atomic type of integers.

    : kindof(Int)    is  type
    : typeof(Int)    is  INT
    : isterm(x, Int) iff issub(typeof(x), Int)
    : null(Int)      is  0
    : builtin(Int)   is  int
    """
    __null__        = 0
    __builtin__     = int

class Float(metaclass=FLOAT):
    """
    The atomic type of floats.

    : kindof(Float)    is  type
    : typeof(Float)    is  FLOAT
    : isterm(x, Float) iff issub(typeof(x), Float)
    : nullof(Float)    is  0.0
    : builtin(Float)   is  float
    """
    __null__        = 0.0
    __builtin__     = float

class Bool(metaclass=BOOL):
    """
    The atomic type of booleans

    : kindof(Bool)    is type
    : typeof(Bool)    is BOOL
    : isterm(x, Bool) iff issub(typeof(x), Bool)
    : nullof(Bool)    is False
    : builtin(Bool)   is bool
    """
    __null__        = False
    __builtin__     = bool

class Str(metaclass=STR):
    """
    The atomic type of strings

    : kindof(Str)    is type
    : typeof(Str)    is STR
    : isterm(x, Str) iff issub(typeof(x), Str)
    : nullof(Str)    is ""
    : builtin(Str)   is str
    """
    __null__        = ""
    __builtin__     = str

    def __len__(self, obj):
        return len(obj)

    def __size__(obj):
        return len(obj)

    def __include__(obj, *args, **kwargs):
        return obj + "".join(str(a) for a in args)

    def __join__(obj, *args, **kwargs):
        if not args:
            return obj
        if len(args) == 1 and isinstance(args[0], (list, tuple, set)):
            return obj.join(args[0])
        if all(isinstance(a, str) for a in args):
            return obj + "".join(args)

        from typed.mods.err import TypeErr
        raise TypeErr(message="Unsupported argument types for Str.__join__", term=args)

    def __split__(obj, by=None, size=None, key=None, predicate=None):
        from typed.mods.err import Err

        if by is not None and size is not None:
            raise Err(message="split(str): specify either 'by' or 'size', not both")
        if by is not None:
            return obj.split(by)
        if size is not None:
            if size <= 0:
                raise Err(message="split(str): 'size' must be positive")
            return [obj[i : i + size] for i in range(0, len(obj), size)]
        return obj.split()

class Byte(metaclass=BYTE):
    """
    The atomic type of bytes

    : kindof(Byte)    is type
    : typeof(Byte)    is BYTE
    : isterm(x, Byte) iff issub(typeof(x), Byte)
    : nullof(Byte)    is bytes()
    : builtin(Byte)   is bytes
    """
    __null__        = bytes()
    __builtin__     = bytes

class Member(metaclass=MEMBER):
    """
    The atomic type of TYPESYSTEM members

    : kindof(Member)    is type
    : typeof(Member)    is MEMBER
    : isterm(x, Member) iff x in TYPESYSTEM
    : nullof(Member)    is NotDefined
    : builtin(Member)   is NotDefined
    """

class Dom(metaclass=COD):
    """
    The atomic type of domains

    : kindof(Dom)    is type
    : typeof(Dom)    is DOM
    : isterm(x, Dom) iff x in Tuple and t in Member for t in x
    : nullof(Dom)    is NotDefined
    : builtin(Dom)   is NotDefined
    """

class Cod(Member, metaclass=COD):
    """
    The atomic type of codomains

    : kindof(Cod)    is type
    : typeof(Cod)    is COD
    : isterm(x, Cod) iff x in Member
    : nullof(Cod)    is NotDefined
    : builtin(Cod)   is NotDefined
    """
