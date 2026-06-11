from typed.mods.typesystem import new

def __typemap__():
    from typed.mods.types.atomic import (
        Int, Float, Bool, Str, Byte
    )
    from typed.mods.types.constructor import (
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
some.__display__ = "some"

every = new.quantifier(new.reducer(all), order=1)
every.__display__ = "every"

none  = new.quantifier(new.reducer(lambda iter: not any(iter)), order=1)
none.__display__ = "none"

only  = new.quantifier(reducer=new.reducer(lambda n: lambda iter: sum(bool(x) for x in iter) == n), order=1)
only.__display__ = "only"

__quantifiers__ = { some, every, none, only }

class __typecheck__:
    lazy = True
    defaults = False
    envs = ()

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
