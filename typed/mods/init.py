from typed.mods.typesystem import new

def __typemap__():
    from typed.mods.types.base import (
        Int, Float, Bool, Str, Bytes,
        List, Tuple, Set, Dict
    )
    return {
        int:       Int,
        float:     Float,
        bool:      Bool,
        str:       Str,
        bytes:     Bytes,
        bytearray: Bytes,
        list:      List,
        tuple:     Tuple,
        set:       Set,
        dict:      Dict
    }

some  = new.quantifier(new.reducer(any))
every = new.quantifier(new.reducer(all))
none  = new.quantifier(new.reducer(lambda iter: not any(iter)))
true  = new.quantifier(new.reducer(lambda iter: True))
false = new.quantifier(new.reducer(lambda iter: False))

UNIVERSE   = new.universe()
ABSTRACT   = new.abstract()
TYPESYSTEM = new.typesystem(
    universe=UNIVERSE,
    abstract=ABSTRACT,
    quantifiers={some, every, none, true, false},
    typemap={},
    is_strict=False,
    kinds=set()
)

conf = new.conf()

TYPESYSTEM.__typemap__.update(__typemap__())
