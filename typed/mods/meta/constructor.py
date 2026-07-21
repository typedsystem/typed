import weakref
from typed.mods.meta.atomic import TYPE

class TUPLE(TYPE):
    """
    The metatype of the constructor type of tuples.
    : kindof(TUPLE)    is  meta
    : typeof(TUPLE)    is  UNIVERSE(1)
    : isterm(T, TUPLE) iff issub(typeof(T), TUPLE)
    : nullof(TUPLE)    is  NotDefined
    : builtin(TUPLE)   is  NotDefined
    """
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm
        if not isinstance(trm, tuple) and not issub(typeof(
            trm,
            level=2
        ), TUPLE):
            return False
        types = getattr(typ, '__types__', None)
        if types is not None:
            from typed.mods.init import every
            return every(isterm(x, *types) for x in trm)
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub, isequiv, typeof
        if isequiv(typeof(other), typeof(typ)):
            types = getattr(typ, '__types__', None)
            others = getattr(other, '__types__', None)
            if types is None and others is not None:
                return False
            if others is None:
                return True
            from typed.mods.init import every
            return every(issub(t, *others) for t in types)
        return False

    def __call__(typ, *types, typesystem=None):
        from typed.mods.resolve import resolve
        from typed.mods.check import require
        typesystem = resolve.typesystem.entity(typesystem)
        cache_key = (typ, tuple(types), id(typesystem))
        if cache_key in typ._type_cache:
            return typ._type_cache[cache_key]
        require.every.ismember(types, typesystem)
        display_name = f"Tuple({typesystem.nameof(*types)})" if types else "Tuple"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Tuple(typ, metaclass=TUPLE):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types

        Tuple.__name__ = display_name
        typ._type_cache[cache_key] = Tuple
        return Tuple

class LIST(TYPE):
    """
    The metatype of lists.
    : kindof(LIST)    is  meta
    : typeof(LIST)    is  UNIVERSE(1)
    : isterm(T, LIST) iff issub(typof(T), LIST)
    : nullof(LIST)    is  NotDefined
    : builtin(LIST)   is  NotDefined
    """
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm
        if not isinstance(trm, list) and not issub(typeof(
            trm,
            level=2
        ), LIST):
            return False
        types = getattr(typ, '__types__', None)
        if types is not None:
            from typed.mods.init import every
            return every(isterm(x, *types) for x in trm)
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub, isequiv, typeof
        if isequiv(typeof(other), typeof(typ)):
            types  = getattr(typ, '__types__', None)
            others = getattr(other, '__types__', None)
            if types is None and others is not None:
                return False
            if others is None:
                return True
            from typed.mods.init import every
            return every(issub(t, *others) for t in types)
        return False

    def __call__(typ, *types, typesystem=None):
        from typed.mods.resolve import resolve
        from typed.mods.check import require
        typesystem = resolve.typesystem.entity(typesystem)
        types_set = set(types)

        cache_key = (typ, frozenset(types_set), id(typesystem))
        if cache_key in typ._type_cache:
            return typ._type_cache[cache_key]
        require.every.ismember(types_set, typesystem)
        display_name = f"List({typesystem.nameof(*types)})" if types else "List"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class List(typ, metaclass=LIST):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types_set

        List.__name__ = display_name
        typ._type_cache[cache_key] = List
        return List

class SET(TYPE):
    """
    The metatype of sets.
    : kindof(SET)    is  meta
    : typeof(SET)    is  UNIVERSE(1)
    : isterm(T, SET) iff issub(typeof(T), SET)
    : nullof(SET)    is  NotDefined
    : builtin(SET)   is  NotDefined
    """
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm
        if not isinstance(trm, set) and not issub(typeof(
            trm,
            level=2
        ), SET):
            return False
        types = getattr(typ, '__types__', None)
        if types is not None:
            from typed.mods.init import every
            return every(isterm(x, *types) for x in trm)
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub, isequiv, typeof
        if isequiv(typeof(other), typeof(typ)):
            types  = getattr(typ, '__types__', None)
            others = getattr(other, '__types__', None)
            if types is None and others is not None:
                return False
            if others is None:
                return True
            from typed.mods.init import every
            return every(issub(t, *others) for t in types)
        return False

    def __call__(typ, *types, typesystem=None):
        from typed.mods.resolve import resolve
        from typed.mods.check import require
        typesystem = resolve.typesystem.entity(typesystem)
        types_set = set(types)
        cache_key = (typ, frozenset(types_set), id(typesystem))
        if cache_key in typ._type_cache:
            return typ._type_cache[cache_key]
        require.every.ismember(types_set, typesystem)
        display_name = f"Set({typesystem.nameof(*types)})" if types else "Set"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Set(typ, metaclass=SET):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types_set

        Set.__name__ = display_name
        typ._type_cache[cache_key] = Set
        return Set

class DICT(TYPE):
    """
    The metatype of dictionaries.
    : kindof(DICT)    is  meta
    : typeof(DICT)    is  UNIVERSE(1)
    : isterm(T, DICT) iff issub(typeof(T), DICT)
    : nullof(DICT)    is  NotDefined
    : builtin(DICT)   is  NotDefined
    """
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm
        if not isinstance(trm, dict) and not issub(typeof(
            trm,
            level=2
        ), DICT):
            return False
        types = getattr(typ, "__types__", None)
        key_type = getattr(typ, "__key_type__", None)
        if types is not None:
            from typed.mods.init import every
            if not every(isterm(v, *types) for v in trm.values()):
                return False
        if key_type is not None:
            from typed.mods.init import every
            if not every(isterm(k, key_type) for k in trm.keys()):
                return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        if type(other) is type(typ):
            types = getattr(typ, '__types__', None)
            others = getattr(other, '__types__', None)
            typ_key = getattr(typ, '__key_type__', None)
            other_key = getattr(other, '__key_type__', None)
            if types is None and others is not None:
                return False
            if typ_key is None and other_key is not None:
                return False
            if types is not None and others is not None:
                from typed.mods.init import every
                if not every(issub(t, *others) for t in types):
                    return False
            if typ_key is not None and other_key is not None:
                if not issub(typ_key, other_key):
                    return False
            return True
        return False

    def __call__(met, *types, key=None, typesystem=None):
        from typed.mods.resolve import resolve
        from typed.mods.check import require
        typesystem = resolve.typesystem.entity(typesystem)
        types_set = set(types)
        cache_key = (met, frozenset(types_set), key, id(typesystem))
        if cache_key in met._type_cache:
            return met._type_cache[cache_key]
        if key is not None:
            display_name = f"Dict({typesystem.nameof(*types)}, key={typesystem.nameof(key)})" if types else f"Dict(key={typesystem.nameof(key)})"
        else:
            display_name = f"Dict({typesystem.nameof(*types)})" if types else "Dict"
        require.ismember(key, typesystem)
        require.every.ismember(types_set, typesystem)
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Dict(met, metaclass=DICT):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types_set
            __key_type__ = key

        Dict.__name__ = display_name
        met._type_cache[cache_key] = Dict
        return Dict

class EXTENSIONAL(TYPE):
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        quantifier = getattr(typ, "__quantifier__", None)
        types = set(getattr(typ, "__types__", (typ,)))
        from typed.mods.typesystem import isterm
        return isterm(
            trm,
            *types,
            quantifier=quantifier
        )

    def __issub__(typ, other):
        quantifier = getattr(typ, "__quantifier__", None)
        types = (t for t in getattr(typ, "__types__", (typ,)))
        others = (o for o in getattr(other, "__types__", (other,)))
        from typed.mods.typesystem import issub
        if other.__flags__.is_extensional:
            return quantifier(
                issub(
                    o,
                    *types,
                    quantifier=quantifier
                ) for o in others
            )
        return issub(
            other,
            *types,
            quantifier=quantifier
        )

    def __call__(met, name, *types, bases=(), base=None, quantifier=None, typesystem=None):
        from typed.mods.resolve import resolve
        from typed.mods.check import require
        typesystem = resolve.typesystem.entity(typesystem)

        if base is None:
            from typed.mods.types.atomic import Empty
            base = Empty

        types_tuple = tuple(set(types))
        cache_key = (
            met,
            name,
            types_tuple,
            tuple(bases),
            base,
            quantifier,
            id(typesystem)
        )
        if cache_key in met._type_cache:
            return met._type_cache[cache_key]

        require.ismember(base, typesystem)
        require.every.ismember(types_tuple, typesystem)

        if not types_tuple:
            return base

        if len(types_tuple) == 1:
            return types_tuple[0]

        display_name = f"{name}({typesystem.nameof(*types_tuple)})"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Extensional(*bases, metaclass=type(met)):
            __flags__ = Flags(
                is_constructor=True,
                is_extensional=True
            )
            __typesystems__ = {TYPESYSTEM, typesystem}
            __quantifier__ = quantifier
            __display__ = display_name
            __types__ = types_tuple

        Extensional.__name__ = display_name
        met._type_cache[cache_key] = Extensional
        return Extensional

class UNION(EXTENSIONAL):
    def __call__(met, *types, base=None, typesystem=None):
        from typed.mods.init import some
        return super().__call__(
            "Union",
            *types,
            bases=(met,),
            base=base,
            quantifier=some,
            typesystem=typesystem
        )

class INTER(EXTENSIONAL):
    def __call__(met, *types, base=None, typesystem=None):
        from typed.mods.init import every
        return super().__call__(
            "Inter",
            *types,
            bases=(met,),
            base=base,
            quantifier=every,
            typesystem=typesystem
        )

class NOT_IN(EXTENSIONAL):
    def __call__(met, name, *types, base=None, typesystem=None):
        from typed.mods.init import none
        return super().__call__(
            "NotIn",
            *types,
            bases=(met,),
            base=base,
            quantifier=none,
            typesystem=typesystem
        )

class ALGEBRAIC(TYPE):
    """
    The base metaclass for types built over a discourse of other types,
    abstracting factory logic for Algebraic Data Types (Products and Coproducts).
    """
    _type_cache = weakref.WeakValueDictionary()

    def __call__(met, name, *types, base=None, typesystem=None):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        if base is None:
            from typed.mods.types.atomic import Empty
            base = Empty
        if not types:
            return base
        types_tuple = tuple(types)
        cache_key = (
            met,
            name,
            types_tuple,
            base,
            id(typesystem)
        )
        if cache_key in met._type_cache:
            return met._type_cache[cache_key]
        from typed.mods.check import require
        require.every.ismember(types_tuple, typesystem)
        from typed.mods.poly import nullof
        display_name = f"{name}({typesystem.nameof(*types_tuple)})"
        is_prod = getattr(type(met), '__name__', '') == 'PROD' or getattr(met, '__name__', '') == 'PROD'
        is_coprod = getattr(type(met), '__name__', '') == 'COPROD' or getattr(met, '__name__', '') == 'COPROD'
        from typed.mods.flags import Flags
        from typed.mods.err import NotDefined
        from typed.mods.init import TYPESYSTEM

        if is_prod:
            nulls = tuple(nullof(t) for t in types_tuple if nullof(t) is not NotDefined)
            canonical_null = nulls if len(nulls) == len(types_tuple) else NotDefined
        elif is_coprod:
            first_null = nullof(types_tuple[0]) if types_tuple else NotDefined
            canonical_null = (0, first_null) if first_null is not NotDefined else NotDefined
        else:
            canonical_null = NotDefined

        class Algebraic(met, metaclass=type(met)):
            __kind__ = "type"
            __flags__ = Flags(
                is_constructor=True,
                is_algebraic=True,
                is_prod=is_prod,
                is_coprod=is_coprod
            )
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types_tuple
            __null__ = canonical_null

        Algebraic.__name__ = display_name
        met._type_cache[cache_key] = Algebraic
        return Algebraic

class PROD(ALGEBRAIC):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        if not isinstance(trm, tuple):
            return False
        types = getattr(typ, "__types__", None)
        if types is None:
            return True
        if len(trm) != len(types):
            return False
        for x, t in zip(trm, types):
            if not isterm(x, t):
                return False
        return True

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        types = getattr(typ, "__types__", tuple())
        others = getattr(other, "__types__", tuple())
        if getattr(other.__flags__, "is_prod", False):
            if not types:
                return True
            if not others:
                return False
            if len(types) != len(others):
                return False
            for o, t in zip(others, types):
                if not issub(o, t):
                    return False
            return True
        return False

    def __call__(met, *types, typesystem=None):
        return super().__call__(
            "Prod",
            *types,
            typesystem=typesystem
        )

class COPROD(ALGEBRAIC, TUPLE):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        from typed.mods.logic import codiag
        if not isinstance(trm, tuple) or len(trm) != 2:
            return False
        types = getattr(typ, "__types__", None)
        if types is None:
            return False
        for i, t in codiag(trm, types):
            if isterm(i, t):
                return True
        return False

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        types = getattr(typ, "__types__", tuple())
        others = getattr(other, "__types__", tuple())
        if getattr(other.__flags__, "is_coprod", False):
            if not types:
                return False
            if not others:
                return True
            if len(types) != len(others):
                return False
            for o, t in zip(others, types):
                if not issub(o, t):
                    return False
            return True
        return False

    def __isequiv__(typ, other):
        from typed.mods.typesystem import isequiv, issame
        from typed.mods.types.atomic import Empty
        types = list(getattr(typ, "__types__", []))
        if len(types) == 2:
            if issame(types[1], Empty) and isequiv(types[0], other):
                return True
            if issame(types[0], Empty) and isequiv(types[1], other):
                return True
        if getattr(other, "__flags__", None) and other.__flags__.is_coprod:
            others = list(getattr(other, "__types__", []))
            types_clean = [t for t in types if not issame(t, Empty)]
            others_clean = [o for o in others if not issame(o, Empty)]
            if len(types_clean) == len(others_clean):
                used = set()
                for t in types_clean:
                    found = False
                    for i, o in enumerate(others_clean):
                        if i not in used and isequiv(t, o):
                            used.add(i)
                            found = True
                            break
                    if not found:
                        return False
                return True
        return False

    def __call__(met, *types, typesystem=None):
        return super().__call__(
            "Coprod",
            *types,
            typesystem=typesystem
        )

class DIAG(TYPE):
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        base = getattr(typ, "__base_type__", None)
        if not base:
            return False
        if not isinstance(trm, tuple) or len(trm) != 2:
            return False
        return trm[0] == trm[1] and isterm(trm[0], base)

    def __issub__(typ, other):
        from typed.mods.types.constructor import Prod
        from typed.mods.typesystem import issub
        base = getattr(typ, "__base_type__", None)
        if issub(Prod(base, base), other):
            return True
        return False

    def __call__(met, base_type, typesystem=None):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        cache_key = (met, base_type, id(typesystem))
        if cache_key in met._type_cache:
            return met._type_cache[cache_key]
        display_name = f"Diag({typesystem.nameof(base_type)})"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Diag(met, metaclass=DIAG):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __base_type__ = base_type

        Diag.__name__ = display_name
        met._type_cache[cache_key] = Diag
        return Diag

class CODIAG(TYPE):
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        base = getattr(typ, "__base_type__", None)
        if not base:
            return False
        if not isinstance(trm, tuple) or len(trm) != 2:
            return False
        return trm[0] in (0, 1) and isterm(trm[1], base)

    def __call__(met, base_type, typesystem=None):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        cache_key = (met, base_type, id(typesystem))
        if cache_key in met._type_cache:
            return met._type_cache[cache_key]
        display_name = f"Codiag({typesystem.nameof(base_type)})"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Codiag(met, metaclass=CODIAG):
            __kind__ = "type"
            __flags__ = Flags(is_constructor=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __base_type__ = base_type

        Codiag.__name__ = display_name
        met._type_cache[cache_key] = Codiag
        return Codiag
