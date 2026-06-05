from typed.mods.typesystem import new

def __typemap__():
    from typed.mods.types.base import (
        Int, Float, Bool, Str, Byte
    )
    from typed.mods.types.dependent import (
        Tuple, List, Set, Dict
    )
    return {
        int:       Int,
        float:     Float,
        bool:      Bool,
        str:       Str,
        bytes:     Byte,
        bytearray: Byte,
        list:      List,
        tuple:     Tuple,
        set:       Set,
        dict:      Dict
    }

__kinds__ = {"universe", "abstract", "meta", "type", "quantifier", "dependent"}

some  = new.quantifier(new.reducer(any), order=1)
every = new.quantifier(new.reducer(all), order=1)
none  = new.quantifier(new.reducer(lambda iter: not any(iter)), order=1)
true  = new.quantifier(new.reducer(lambda iter: True), order=1)
false = new.quantifier(new.reducer(lambda iter: False), order=1)
only  = new.quantifier(reducer=new.reducer(lambda n: lambda iter: sum(bool(x) for x in iter) == n), order=1)

__quantifiers__ = { some, every, none, true, false, only }

SAMENESS = new.sameness()
STATEFUL = new.stateful()
MAGIC = new.magic()
UNIVERSE = new.universe(stateful=STATEFUL, magic=MAGIC)
ABSTRACT = new.abstract(stateful=STATEFUL, magic=MAGIC)
TYPESYSTEM = new.typesystem(
    stateful=STATEFUL,
    magic=MAGIC,
    universe=UNIVERSE,
    abstract=ABSTRACT,
    quantifiers=__quantifiers__,
    kinds=__kinds__,
    typemap={}
)

conf = new.conf()

TYPESYSTEM.__typemap__.update(__typemap__())
