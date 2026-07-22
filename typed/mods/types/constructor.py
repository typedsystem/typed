from typing import TYPE_CHECKING
from typed.mods.meta.constructor import (
    TUPLE, LIST, SET, DICT,
    EXTENSIONAL, UNION, INTER, NOT_IN,
    ALGEBRAIC, PROD, COPROD
)
from typed.mods.flags import Flags

class Tuple(metaclass=TUPLE):
    if TYPE_CHECKING:
        def __new__(cls, *types, typesystem=None):
            ...

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

    def __size__(trm):
        return len(trm)

    def __include__(trm, *args, **kwargs):
        return trm + tuple(args)

    def __join__(trm, *args, **kwargs):
        res = tuple(trm)
        for a in args:
            res += tuple(a)
        return res

    def __split__(trm, by=None, size=None, key=None, predicate=None):
        from typed.mods.err import Err

        seq = tuple(trm)
        if size is not None:
            if size <= 0:
                raise Err(message="split(seq): 'size' must be positive")
            chunks = [seq[i : i + size] for i in range(0, len(seq), size)]
            return [type(trm)(chunk) for chunk in chunks]

        if predicate is not None:
            left = tuple(x for x in seq if predicate(x))
            right = tuple(x for x in seq if not predicate(x))
            return [type(trm)(left), type(trm)(right)]

        if key is not None:
            groups = {}
            for x in seq:
                groups.setdefault(key(x), []).append(x)
            return {k: type(trm)(tuple(v)) for k, v in groups.items()}

        raise Err(message="split(seq): must specify at least one of 'size', 'predicate', or 'key'")


class List(metaclass=LIST):
    if TYPE_CHECKING:
        def __new__(cls, *types, typesystem=None):
            ...

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

    def __size__(trm):
        return len(trm)

    def __include__(trm, *args, **kwargs):
        for v in args:
            trm.append(v)
        return trm

    def __join__(trm, *args, **kwargs):
        res = list(trm)
        for a in args:
            res.extend(a)
        return res

    def __split__(trm, by=None, size=None, key=None, predicate=None):
        from typed.mods.err import Err

        seq = list(trm)
        if size is not None:
            if size <= 0:
                raise Err(message="split(seq): 'size' must be positive")
            chunks = [seq[i : i + size] for i in range(0, len(seq), size)]
            return [type(trm)(chunk) for chunk in chunks]

        if predicate is not None:
            left = [x for x in seq if predicate(x)]
            right = [x for x in seq if not predicate(x)]
            return [type(trm)(left), type(trm)(right)]

        if key is not None:
            groups = {}
            for x in seq:
                k = key(x)
                groups.setdefault(k, []).append(x)
            return {k: type(trm)(v) for k, v in groups.items()}

        raise Err(message="split(seq): must specify at least one of 'size', 'predicate', or 'key'")


class Set(metaclass=SET):
    if TYPE_CHECKING:
        def __new__(cls, *types, typesystem=None):
            ...

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

    def __size__(trm):
        return len(trm)

    def __include__(trm, *args, **kwargs):
        for v in args:
            trm.add(v)
        return trm

    def __join__(trm, *args, **kwargs):
        res = set(trm)
        for a in args:
            res |= set(a)
        return res

    def __split__(trm, by=None, size=None, key=None, predicate=None):
        from typed.mods.err import Err

        if predicate is not None:
            left = {x for x in trm if predicate(x)}
            right = {x for x in trm if not predicate(x)}
            return [type(trm)(left), type(trm)(right)]

        if key is not None:
            groups = {}
            for x in trm:
                k = key(x)
                groups.setdefault(k, set()).add(x)
            return {k: type(trm)(v) for k, v in groups.items()}

        raise Err(message="split(set): must specify 'predicate' or 'key'")


class Dict(metaclass=DICT):
    if TYPE_CHECKING:
        def __new__(cls, *types, key=None, typesystem=None):
            ...

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

    def __size__(trm):
        return len(trm)

    def __getitem__(trm, key):
        return trm.__dict__[key]

    def __setitem__(trm, key, value):
        trm.__dict__[key] = value

    def __contains__(trm, key):
        return key in trm.__dict__

    def __include__(trm, *args, **kwargs):
        if args:
            if len(args) == 1 and isinstance(args[0], dict):
                trm.update(args[0])
            else:
                for k, v in args:
                    trm[k] = v
        if kwargs:
            trm.update(kwargs)
        return trm

    def __join__(trm, *args, on_conflict="error", **kwargs):
        from typed.mods.err import Err
        result = dict(trm)
        for d in args:
            for k, v in d.items():
                if k not in result:
                    result[k] = v
                else:
                    if on_conflict == "error":
                        raise Err(message=f"duplicate key {k!r}")
                    elif on_conflict == "first":
                        continue
                    elif on_conflict == "last":
                        result[k] = v
                    elif callable(on_conflict):
                        result[k] = on_conflict(k, result[k], v)
                    else:
                        raise Err(message=f"Unknown on_conflict={on_conflict!r}")
        return result

    def __split__(trm, by=None, size=None, key=None, predicate=None):
        from typed.mods.err import Err, TypeErr

        if by is not None:
            if not isinstance(by, (set, list, tuple)):
                raise TypeErr(message="split(dict): 'by' must be an iterable of keys", term=by, expected=(set, list, tuple))
            keyset = set(by)
            left = {k: v for k, v in trm.items() if k in keyset}
            right = {k: v for k, v in trm.items() if k not in keyset}
            return [left, right]

        if predicate is not None:
            left, right = {}, {}
            for k, v in trm.items():
                if predicate(k, v):
                    left[k] = v
                else:
                    right[k] = v
            return [left, right]

        if key is not None:
            groups = {}
            for k, v in trm.items():
                g = key(k, v)
                groups.setdefault(g, {})[k] = v
            return groups

        raise Err(message="split(dict): must specify one of 'by', 'predicate', or 'key'")


class Extensional(metaclass=EXTENSIONAL):
    if TYPE_CHECKING:
        def __new__(cls, name, *types, bases=(), base=None, quantifier=None, typesystem=None):
            ...

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
    if TYPE_CHECKING:
        def __new__(cls, *types, base=None, typesystem=None):
            ...

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
    if TYPE_CHECKING:
        def __new__(cls, *types, base=None, typesystem=None):
            ...

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
    if TYPE_CHECKING:
        def __new__(cls, name, *types, base=None, typesystem=None):
            ...

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
    if TYPE_CHECKING:
        def __new__(cls, name, *types, base=None, typesystem=None):
            ...

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
    if TYPE_CHECKING:
        def __new__(cls, *types, typesystem=None): 
            ...

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
    if TYPE_CHECKING:
        def __new__(cls, *types, typesystem=None): 
            ...

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
