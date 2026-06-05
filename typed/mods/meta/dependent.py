from typed.mods.meta.base import TYPE, UNIVERSE_1
from typed.mods.init import TYPESYSTEM
from typed.mods.err import NotDefined
from typed.mods.flags import Flags

class TUPLE(TYPE):
    """
    The metatype of the dependent type of tuples.

    kindof(TUPLE)    is  meta
    typeof(TUPLE)    is  UNIVERSE(1)
    isterm(T, TUPLE) iff issub(typeof(T), TUPLE)
    nullof(TUPLE)    is  NotDefined
    builtin(TUPLE)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, tuple) and not issub(typeof(trm, level=2), TUPLE):
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
        from typed.mods.check import resolve, check

        typesystem = resolve.typesystem.entity(typesystem)
        check.every.ismember(types, typesystem)

        display_name = f"Tuple({typesystem.nameof(*types)})" if types else "Tuple"

        class DependentTuple(typ, metaclass=TUPLE):
            __kind__ = "type"
            __flags__ = Flags(is_dependent=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types
            __null__ = NotDefined

        DependentTuple.__name__ = display_name
        return DependentTuple

    __kind__ = "meta"
    __typesystems__ = {TYPESYSTEM, }
    __display__ = "TUPLE"
    __null__ = NotDefined
    __builtin__ = NotDefined


class LIST(TYPE):
    """
    The metatype of lists.

    kindof(LIST)    is  meta
    typeof(LIST)    is  UNIVERSE(1)
    isterm(T, LIST) iff issub(typof(T), LIST)
    nullof(LIST)    is  NotDefined
    builtin(LIST)   is  NotDefined
    """

    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, list) and not issub(typeof(trm, level=2), LIST):
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
        from typed.mods.check import check, resolve
        typesystem = resolve.typesystem.entity(typesystem)

        types = set(types)
        check.every.ismember(types, typesystem)

        display_name = f"List({typesystem.nameof(*types)})" if types else "List"

        class DependentList(typ, metaclass=LIST):
            __kind__ = "type"
            __flags__ = Flags(is_dependent=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types
            __null__ = NotDefined

        DependentList.__name__ = display_name
        return DependentList

    __kind__ = "meta"
    __typesystems__ = {TYPESYSTEM, }
    __display__ = "LIST"
    __null__ = NotDefined
    __builtin__ = NotDefined


class SET(TYPE):
    """
    The metatype of sets.

    kindof(SET)    is  meta
    typeof(SET)    is  UNIVERSE(1)
    isterm(T, SET) iff issub(typeof(T), SET)
    nullof(SET)    is  NotDefined
    builtin(SET)   is  NotDefined
    """
    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, set) and not issub(typeof(trm, level=2), SET):
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
        from typed.mods.check import check, resolve
        typesystem = resolve.typesystem.entity(typesystem)

        types = set(types)
        check.every.ismember(types, typesystem)

        display_name = f"Set({typesystem.nameof(*types)})" if types else "Set"

        class DependentSet(typ, metaclass=SET):
            __kind__ = "type"
            __flags__ = Flags(is_dependent=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types
            __null__ = NotDefined

        DependentSet.__name__ = display_name
        return DependentSet

    __kind__ = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __type__ = UNIVERSE_1
    __display__ = "SET"
    __null__ = NotDefined
    __builtin__ = NotDefined

class DICT(TYPE):
    """
    The metatype of dictionaries.

    kindof(DICT)    is  meta
    typeof(DICT)    is  UNIVERSE(1)
    isterm(T, DICT) iff issub(typeof(T), DICT)
    nullof(DICT)    is  NotDefined
    builtin(DICT)   is  NotDefined
    """
    def __isterm__(typ, trm):
        from typed.mods.typesystem import typeof, issub, isterm

        if not isinstance(trm, dict) and not issub(typeof(trm, level=2), DICT):
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

    def __call__(typ, *types, key=None, typesystem=None):
        from typed.mods.check import check, resolve
        typesystem = resolve.typesystem.entity(typesystem)

        types = set(types)
        
        if key is not None:
            display_name = f"Dict({typesystem.nameof(*types)}, key={typesystem.nameof(key)})" if types else f"Dict(key={typesystem.nameof(key)})"
        else:
            display_name = f"Dict({typesystem.nameof(*types)})" if types else "Dict"

        check.ismember(key, typesystem)
        check.every.ismember(types, typesystem)

        class DependentDict(typ, metaclass=DICT):
            __kind__ = "type"
            __flags__ = Flags(is_dependent=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types
            __key_type__ = key
            __null__ = NotDefined

        DependentDict.__name__ = display_name
        return DependentDict

    __kind__ = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __type__ = UNIVERSE_1
    __display__ = "DICT"
    __null__ = NotDefined
    __builtin__ = NotDefined

class EXTENSIONAL(TYPE):
    def __isterm__(typ, trm):
        quantifier = getattr(typ, "__quantifier__", None)
        types = set(getattr(typ, "__types__", (typ,)))
        from typed.mods.typesystem import isterm
        return isterm(trm, *types, quantifier=quantifier)

    def __issub__(typ, other):
        quantifier = getattr(typ, "__quantifier__", None)
        types = (t for t in getattr(typ, "__types__", (typ,)))
        others = (o for o in getattr(other, "__types__", (other,)))
        from typed.mods.typesystem import issub

        if other.__flags__.is_extensional:
            return quantifier(issub(o, *types, quantifier=quantifier) for o in others)

        return issub(other, *types, quantifier=quantifier)

    def __call__(met, name, *types, base=None, quantifier=None, typesystem=None):
        from typed.mods.check import check, resolve
        typesystem = resolve.typesystem.entity(typesystem)

        check.ismember(base, typesystem)
        check.every.ismember(types, typesystem)

        types = tuple(set(types))

        if not types:
            return base

        if len(types) == 1:
            return types[0]

        display_name = f"{name}({typesystem.nameof(*types)})"

        class Extensional(*types, metaclass=EXTENSIONAL):
            __kind__ = "type"
            __flags__ = Flags(is_dependent=True, is_extensional=True)
            __typesystems__ = {TYPESYSTEM, typesystem}
            __quantifier__ = quantifier
            __display__ = display_name
            __types__ = types
            __null__ = NotDefined

        Extensional.__name__ = display_name
        return Extensional

    __kind__ = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __type__ = UNIVERSE_1
    __display__ = "EXTENSIONAL"
    __null__ = NotDefined
    __builtin__ = NotDefined


class UNION(EXTENSIONAL):
    def __call__(met, *types, base=None, typesystem=None):
        from typed.mods.init import some
        return super().__call__("Union", *types, base=base, quantifier=some, typesystem=typesystem)

class INTER(EXTENSIONAL):
    def __call__(met, *types, base=None, typesystem=None):
        from typed.mods.init import every
        return super().__call__("Inter", *types, base=base, quantifier=every, typesystem=typesystem)

class NOT_IN(EXTENSIONAL):
    def __call__(met, name, *types, base=None, typesystem=None):
        from typed.mods.init import none
        return super().__call__("NotIn", *types, base=base, quantifier=none, typesystem=typesystem)


class ALGEBRAIC(TYPE):
    """
    The base metaclass for types built over a discourse of other types, 
    abstracting factory logic for Algebraic Data Types (Products and Coproducts).
    """
    def __call__(met, name_prefix, *types, typesystem=None):
        from typed.mods.check import check, resolve
        typesystem = resolve.typesystem.entity(typesystem)
        
        if not types:
            from typed.mods.types.base import Tuple
            return Tuple

        check.every.ismember(types, typesystem)
        types = tuple(types)

        from typed.mods.poly import null

        display_name = f"{name_prefix}({typesystem.nameof(*types)})"

        is_prod = getattr(met, '__name__', '') == 'PROD'
        is_coprod = getattr(met, '__name__', '') == 'COPROD'

        if is_prod:
            nulls = tuple(null(t) for t in types if null(t) is not NotDefined)
            canonical_null = nulls if len(nulls) == len(types) else NotDefined
        elif is_coprod:
            first_null = null(types[0]) if types else NotDefined
            canonical_null = (0, first_null) if first_null is not NotDefined else NotDefined
        else:
            canonical_null = NotDefined

        class Algebraic(*types, metaclass=met):
            __kind__ = "type"
            __flags__ = Flags(
                is_dependent=True, 
                is_algebraic=True, 
                is_prod=is_prod, 
                is_coprod=is_coprod
            )
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = display_name
            __types__ = types
            __null__ = canonical_null

        Algebraic.__name__ = display_name
        return Algebraic

    __kind__ = "meta"
    __typesystems__ = {TYPESYSTEM,}
    __type__ = UNIVERSE_1
    __display__ = "ALGEBRAIC"
    __null__ = NotDefined
    __builtin__ = NotDefined


class PROD(ALGEBRAIC):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        from typed.mods.init import every
        from typed.mods.logic import prod
        if not isterm(trm, tuple):
            return False
        try:
            return every(isterm(x, t) for x, t in prod(trm, typ.__types__))
        except Exception:
            return False

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        types = getattr(typ, "__types__", tuple())
        others = getattr(other, "__types__", tuple())

        if other.__flags__.is_prod:
            if not types: return True
            if not others: return False
            if len(types) != len(others): return False
            from typed.mods.logic import prod

            return all(issub(o, t) for o, t in prod(others, types))

        return False

    def __call__(met, *types, typesystem=None):
        return super().__call__("Prod", *types, typesystem=typesystem)

class COPROD(ALGEBRAIC):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        from typed.mods.init import some
        from typed.mods.logic import coprod

        if not isterm(trm, tuple) or len(trm) != 2:
            return False
        try:
            return some(
                trm[0] == i and isterm(trm[1], t)
                for i, t in coprod(typ.__types__)
            )
        except Exception:
            return False

    def __issub__(typ, other):
        from typed.mods.typesystem import issub
        types = getattr(typ, "__types__", tuple())
        others = getattr(other, "__types__", tuple())

        if other.__flags__.is_coprod:
            if not types: return False
            if not others: return True
            if len(types) != len(others): return False

            return 

        return False

    def __call__(met, *types, typesystem=None):
        if not types:
            from typed.mods.types.base import Empty
            return Empty
        return super().__call__("Coprod", *types, typesystem=typesystem)
