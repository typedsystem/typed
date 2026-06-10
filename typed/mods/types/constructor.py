from typed.mods.meta.constructor import (
    TUPLE, LIST, SET, DICT,
    EXTENSIONAL, UNION, INTER, NOT_IN,
    ALGEBRAIC, PROD, COPROD
)
from typed.mods.flags import Flags

class Tuple(metaclass=TUPLE):
    """
    The constructor type of tuples.

    : kindof(Tuple)    is  type
    : typeof(Tuple)    is  TUPLE
    : isterm(x, Tuple) iff isinstance(x, tuple) or issub(typeof(x), Tuple)
    : nullof(Tuple)    is  tuple()
    : builtin(Tuple)   is  tuple
    : flags(Tuple)     is  is_constructor
    """
    __flags     = Flags(is_constructor=True)
    __null__    = tuple()
    __builtin__ = tuple

class List(metaclass=LIST):
    """
    The constructor type of lists.

    : kindof(List)    is  type
    : typeof(List)    is  LIST
    : isterm(x, List) iff isinstance(x, list) or issub(typeof(x), List)
    : nullof(List)    is  []
    : builtin(List)   is  list
    : flags(List)     is  is_constructor
    """
    __flags__   = Flags(is_constructor=True)
    __null__    = []
    __builtin__ = list

class Set(metaclass=SET):
    """
    The constructor type of sets.

    : kindof(Set)    is  type
    : typeof(Set)    is  SET
    : isterm(x, Set) iff isinstance(x, set) or issub(typeof(x), Set)
    : nullof(Set)    is  set()
    : builtin(Set)   is  set
    : flags(Set)     is  is_constructor
    """
    __flags__   = Flags(is_constructor=True)
    __null__    = set()
    __builtin__ = set

class Dict(metaclass=DICT):
    """
    The constructor type of dicts.

    : kindof(Dict)    is  type
    : typeof(Dict)    is  DICT
    : isterm(x, Dict) iff isinstance(x, dict) or issub(typeof(x), Dict)
    : nullof(Dict)    is  {}
    : builtin(Dict)   is  dict
    : flags(Dict)     is  is_constructor
    """
    __flags__   = Flags(is_constructor=True)
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
    The constructor extensional type.

    : kindof(Extensional)     is  type
    : typeof(Extensional)     is  EXTENSIONAL
    : isterm(x, Extensional)  iff issub(typeof(x), Extensional)
    : nullof(Extensional)     is  NotDefined
    : builtin(Extensional)    is  NotDefined
    : flags(Extensional)      is  is_constructor, is_extensional
    """
    __flags__ = Flags(is_constructor=True, is_extensional=True)

class Union(metaclass=UNION):
    """
    The constructor extensional 'union' type.

    : kindof(Union)     is  type
    : typeof(Union)     is  UNION
    : isterm(x, Union)  iff issub(typeof(x), Union)
    : nullof(Union)     is  NotDefined
    : builtin(Union)    is  NotDefined
    : flags(Union)      is  is_constructor, is_extensional
    """
    __flags__ = Flags(is_constructor=True, is_extensional=True)

class Inter(metaclass=INTER):
    """
    The constructor extensional 'intersection' type.

    : kindof(Inter)     is  type
    : typeof(Inter)     is  INTER
    : isterm(x, Inter)  iff issub(typeof(x), Inter)
    : nullof(Inter)     is  NotDefined
    : builtin(Inter)    is  NotDefined
    : flags(Inter)      is  is_constructor, is_extensional
    """
    __flags__ = Flags(is_constructor=True, is_extensional=True)

class NotIn(metaclass=NOT_IN):
    """
    The constructor extensional 'not in' type.

    : kindof(NotIn)     is  type
    : typeof(NotIn)     is  NOT_IN
    : isterm(x, NotIn)  iff issub(typeof(x), NotIn)
    : nullof(NotIn)     is  NotDefined
    : builtin(NotIn)    is  NotDefined
    : flags(NotIn)      is  is_constructor, is_extensional
    """
    __flags__ = Flags(is_constructor=True, is_extensional=True)

class Algebraic(metaclass=ALGEBRAIC):
    """
    The constructor extensional type.

    : kindof(Algebraic)     is  type
    : typeof(Algebraic)     is  ALGEBRAIC
    : isterm(x, Algebraic)  iff issub(typeof(x), Algebraic)
    : nullof(Algebraic)     is  NotDefined
    : builtin(Algebraic)    is  NotDefined
    : flags(Algebraic)      is  is_constructor, is_extensional
    """
    __flags__ = Flags(is_constructor=True, is_extensional=True)

class Prod(metaclass=PROD):
    """
    The constructor algebraic 'product' type.

    : kindof(Prod)     is  type
    : typeof(Prod)     is  PROD
    : isterm(x, Prod)  iff issub(typeof(x), Prod)
    : nullof(Prod)     is  NotDefined
    : builtin(Prod)    is  NotDefined
    : flags(Prod)      is  is_constructor, is_algebraic
    """
    __flags__ = Flags(is_constructor=True, is_algebraic=True)

class Coprod(metaclass=COPROD):
    """
    The constructor algebraic 'coproduct' type.

    : kindof(Coprod)     is  type
    : typeof(Coprod)     is  COPROD
    : isterm(x, Coprod)  iff issub(typeof(x), Coprod)
    : nullof(Coprod)     is  NotDefined
    : builtin(Coprod)    is  NotDefined
    : flags(Coprod)      is  is_constructor, is_algebraic
    """
    __flags__ = Flags(is_constructor=True, is_algebraic=True)
