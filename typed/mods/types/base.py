from typed.mods.meta.base import (
    EMPTY, NILL, ANY,
    TYPE,
    STR, INT, FLOAT, BOOL, BYTE
)
from typed.mods.init import TYPESYSTEM
from typed.mods.err import NotDefined

class Empty(metaclass=EMPTY):
    """
    The type with no terms.

    : kindof(Empty)    is  type
    : typeof(Empty)    is  EMPTY
    : isterm(x, Empty) :=  False
    : nullof(Empty)    is  NotDefined
    : builtin(Empty)   is  NotDefined
    """
    __kind__       = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__       = EMPTY
    __display__    = "Empty"
    __null__       = NotDefined
    __builtin__    = NotDefined

class Nill(metaclass=NILL):
    """
    The type with None value.

    : kindof(Empty)   is  type
    : typeof(Nill)    is  NILL
    : isterm(x, Nill) iff x is None
    : nullof(Nill)    is  None
    : builtin(Nill)   is  NotDefined
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = NILL
    __display__     = "Nill"
    __null__        = None

class Any(metaclass=ANY):
    """
    The type of anything.

    : kindof(Empty)  is  type
    : typeof(Any)    is ANY
    : isterm(x, Any) := True
    : issub(T, Any)  iff issub(typeof(T), ANY)
    : nullof(Any)    is None
    : builtin(Any)   is NotDefined
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = ANY
    __display__     = "Any"
    __null__        = None
    __builtin__     = NotDefined

class Type(metaclass=TYPE):
    """
    The type of all non-universe types.

    : kindof(Empty)   is  type
    : typeof(Type)    is  TYPE := UNIVERSE(0)
    : isterm(x, Type) iff issub(typeof(x), Type)
    : nullof(Type)    is  Nill
    : builtin(Type)   is  type
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = TYPE
    __display__     = "Type"
    __null__        = Nill
    __builtin__     = type

class Int(metaclass=INT):
    """
    The type of integers.

    : kindof(Int)    is  type
    : typeof(Int)    is  INT
    : isterm(x, Int) iff issub(typeof(x), Int)
    : null(Int)      is  0
    : builtin(Int)   is  int
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = INT
    __display__     = "Int"
    __null__        = 0
    __builtin__     = int

class Float(metaclass=FLOAT):
    """
    The type of floats.

    : kindof(Float)    is  type
    : typeof(Float)    is  FLOAT
    : isterm(x, Float) iff issub(typeof(x), Float)
    : nullof(Float)    is  0.0
    : builtin(Float)   is  float
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = FLOAT
    __display__     = "Float"
    __null__        = 0.0
    __builtin__     = float

class Bool(metaclass=BOOL):
    """
    The type of booleans.

    : kindof(Bool)    is type
    : typeof(Bool)    is BOOL
    : isterm(x, Bool) iff issub(typeof(x), Bool)
    : nullof(Bool)    is False
    : builtin(Bool)   is bool
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = BOOL
    __display__     = "Bool"
    __null__        = False
    __builtin__     = bool

class Str(metaclass=STR):
    """
    The type of strings.

    : kindof(Str)    is type
    : typeof(Str)    is STR
    : isterm(x, Str) iff issub(typeof(x), Str)
    : nullof(Str)    is ""
    : builtin(Str)   is str
    """
    def __len__(self, obj):
        return len(obj)

    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = STR
    __display__     = "Str"
    __null__        = ""
    __builtin__     = str

class Byte(metaclass=BYTE):
    """
    The type of bytes.

    : kindof(Byte)    is type
    : typeof(Byte)    is BYTE
    : isterm(x, Byte) iff issub(typeof(x), Byte)
    : nullof(Byte)    is bytes()
    : builtin(Byte)   is bytes
    """
    __kind__        = "type"
    __typesystems__ = {TYPESYSTEM,}
    __type__        = BYTE
    __display__     = "Byte"
    __null__        = bytes()
    __builtin__     = bytes
