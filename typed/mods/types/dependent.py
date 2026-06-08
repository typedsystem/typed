from typed.mods.meta.dependent import (
    TUPLE, LIST, SET, DICT,
    EXTENSIONAL, UNION, INTER,
    ALGEBRAIC, PROD, COPROD,
    RELATED, SOME, SUBS, SUPS, EQUIV,
    FILTERED, BOUNDED, HAS
)
from typed.mods.flags import Flags

class Tuple(metaclass=TUPLE):
    """
    The dependent type of tuples.

    : kindof(Tuple)    is  type
    : typeof(Tuple)    is  TUPLE
    : isterm(x, Tuple) iff isinstance(x, tuple) or issub(typeof(x), Tuple)
    : nullof(Tuple)    is  tuple()
    : builtin(Tuple)   is  tuple
    : flags(Tuple)     is  is_dependent
    """
    __flags     = Flags(is_dependent=True)
    __null__    = tuple()
    __builtin__ = tuple

class List(metaclass=LIST):
    """
    The dependent type of lists.

    : kindof(List)    is  type
    : typeof(List)    is  LIST
    : isterm(x, List) iff isinstance(x, list) or issub(typeof(x), List)
    : nullof(List)    is  []
    : builtin(List)   is  list
    : flags(List)     is  is_dependent
    """
    __flags__   = Flags(is_dependent=True)
    __null__    = []
    __builtin__ = list

class Set(metaclass=SET):
    """
    The dependent type of sets.

    : kindof(Set)    is  type
    : typeof(Set)    is  SET
    : isterm(x, Set) iff isinstance(x, set) or issub(typeof(x), Set)
    : nullof(Set)    is  set()
    : builtin(Set)   is  set
    : flags(Set)     is  is_dependent
    """
    __flags__   = Flags(is_dependent=True)
    __null__    = set()
    __builtin__ = set

class Dict(metaclass=DICT):
    """
    The dependent type of dicts.

    : kindof(Dict)    is  type
    : typeof(Dict)    is  DICT
    : isterm(x, Dict) iff isinstance(x, dict) or issub(typeof(x), Dict)
    : nullof(Dict)    is  {}
    : builtin(Dict)   is  dict
    : flags(Dict)     is  is_dependent
    """
    __flags__   = Flags(is_dependent=True)
    __null__    = {}
    __builtin__ = dict

    def __getitem__(trm, key):
        return trm.__dict__[key]
    def __setitem__(trm, key, value):
        trm.__dict__[key] = value
    def __contains__(trm, key):
        return key in trm.__dict__

class Extensional(metaclass=EXTENSIONAL):
    """
    The dependent extensional type.

    : kindof(Extensional)     is  type
    : typeof(Extensional)     is  EXTENSIONAL
    : isterm(x, Extensional)  iff issub(typeof(x), Extensional)
    : nullof(Extensional)     is  NotDefined
    : builtin(Extensional)    is  NotDefined
    : flags(Extensional)      is  is_dependent, is_extensional
    """
    __flags__ = Flags(is_dependent=True, is_extensional=True)

class Union(metaclass=UNION):
    """
    The dependent extensional 'union' type.

    : kindof(Union)     is  type
    : typeof(Union)     is  UNION
    : isterm(x, Union)  iff issub(typeof(x), Union)
    : nullof(Union)     is  NotDefined
    : builtin(Union)    is  NotDefined
    : flags(Union)      is  is_dependent, is_extensional
    """
    __flags__ = Flags(is_dependent=True, is_extensional=True)

class Inter(metaclass=INTER):
    """
    The dependent extensional 'intersection' type.

    : kindof(Inter)     is  type
    : typeof(Inter)     is  INTER
    : isterm(x, Inter)  iff issub(typeof(x), Inter)
    : nullof(Inter)     is  NotDefined
    : builtin(Inter)    is  NotDefined
    : flags(Inter)      is  is_dependent, is_extensional
    """
    __flags__ = Flags(is_dependent=True, is_extensional=True)

class Algebraic(metaclass=ALGEBRAIC):
    """
    The dependent extensional type.

    : kindof(Algebraic)     is  type
    : typeof(Algebraic)     is  ALGEBRAIC
    : isterm(x, Algebraic)  iff issub(typeof(x), Algebraic)
    : nullof(Algebraic)     is  NotDefined
    : builtin(Algebraic)    is  NotDefined
    : flags(Algebraic)      is  is_dependent, is_extensional
    """
    __flags__ = Flags(is_dependent=True, is_extensional=True)

class Prod(metaclass=PROD):
    """
    The dependent algebraic 'product' type.

    : kindof(Prod)     is  type
    : typeof(Prod)     is  PROD
    : isterm(x, Prod)  iff issub(typeof(x), Prod)
    : nullof(Prod)     is  NotDefined
    : builtin(Prod)    is  NotDefined
    : flags(Prod)      is  is_dependent, is_algebraic
    """
    __flags__ = Flags(is_dependent=True, is_algebraic=True)

class Coprod(metaclass=COPROD):
    """
    The dependent algebraic 'coproduct' type.

    : kindof(Coprod)     is  type
    : typeof(Coprod)     is  COPROD
    : isterm(x, Coprod)  iff issub(typeof(x), Coprod)
    : nullof(Coprod)     is  NotDefined
    : builtin(Coprod)    is  NotDefined
    : flags(Coprod)      is  is_dependent, is_algebraic
    """
    __flags__ = Flags(is_dependent=True, is_algebraic=True)

class Bounded(metaclass=BOUNDED):
    """
    The dependent 'bounded' type.

    : kindof(Bounded)     is  type
    : typeof(Bounded)     is  BOUNDED
    : isterm(x, Bounded)  iff issub(typeof(x), Bounded)
    : nullof(Bounded)     is  NotDefined
    : builtin(Bounded)    is  NotDefined
    : flags(Bounded)      is  is_dependent, is_enumerable, is_finite, is_bounded
    """
    __flags__ = Flags(is_dependent=True, is_enumerable=True, is_finite=True, is_bounded=True)

class Related(metaclass=RELATED):
    """
    The dependent 'bounded' type.

    : kindof(Related)     is  type
    : typeof(Related)     is  BOUNDED
    : isterm(x, Related)  iff issub(typeof(x), Related)
    : nullof(Related)     is  NotDefined
    : builtin(Related)    is  NotDefined
    : flags(Related)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Filtered(metaclass=FILTERED):
    """
    The dependent 'bounded' type.

    : kindof(Filtered)     is  type
    : typeof(Filtered)     is  FILTERED
    : isterm(x, Filtered)  iff issub(typeof(x), Filtered)
    : nullof(Filtered)     is  NotDefined
    : builtin(Filtered)    is  NotDefined
    : flags(Filtered)      is  is_dependent, is_filtered
    """
    __flags__ = Flags(is_dependent=True, is_filtered=True)

class Some(metaclass=SOME):
    """
    The dependent 'some of them' type.

    : kindof(Some)     is  type
    : typeof(Some)     is  SOME
    : isterm(x, Some)  iff issub(typeof(x), Some)
    : nullof(Some)     is  NotDefined
    : builtin(Some)    is  NotDefined
    : flags(Some)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Subs(metaclass=SUBS):
    """
    The dependent 'issub of them' type.

    : kindof(Subs)     is  type
    : typeof(Subs)     is  SUBS
    : isterm(x, Subs)  iff issub(typeof(x), Subs)
    : nullof(Subs)     is  NotDefined
    : builtin(Subs)    is  NotDefined
    : flags(Subs)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Sups(metaclass=SUPS):
    """
    The dependent 'issub of them' type.

    : kindof(Sups)     is  type
    : typeof(Sups)     is  SUPS
    : isterm(x, Sups)  iff issub(typeof(x), Sups)
    : nullof(Sups)     is  NotDefined
    : builtin(Sups)    is  NotDefined
    : flags(Sups)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Equiv(metaclass=EQUIV):
    """
    The dependent 'isequiv to them' type.

    : kindof(Equiv)     is  type
    : typeof(Equiv)     is  EQUIV
    : isterm(x, Equiv)  iff issub(typeof(x), Equiv)
    : nullof(Equiv)     is  NotDefined
    : builtin(Equiv)    is  NotDefined
    : flags(Equiv)      is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)

class Has(metaclass=HAS):
    """
    The dependent 'has' type.

    : kindof(Has)    is  type
    : typeof(Has)    is  HAS
    : isterm(x, Has) iff issub(typeof(x), Has)
    : nullof(Has)    is  NotDefined
    : builtin(Has)   is  NotDefined
    : flags(Has)     is  is_dependent, is_related
    """
    __flags__ = Flags(is_dependent=True, is_related=True)
