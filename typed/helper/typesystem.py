from functools import lru_cache as cache

class STATEFUL:
    EXTENDS = set()
    SUBS  = set()
    SUPS  = set()
    TERMS = set()
    EQUIVS = set()
    SAME = {}

    _issame_cache = {}
    _extends_cache = {}
    _issup_cache = {}
    _issub_cache = {}
    _isterm_cache = {}
    _isequiv_cache = {}

    @staticmethod
    def __issame__(X, Y, typesystem=None):
        if X is Y:
            return True

        cache_key = (id(X), id(Y), id(typesystem))
        if cache_key in STATEFUL._issame_cache:
            return STATEFUL._issame_cache[cache_key]

        if typesystem is None:
            from typed.mods.resolve import resolve
            typesystem = resolve.typesystem.entity(typesystem)

        if not STATEFUL.__issame__(typesystem.typeof(X), typesystem.typeof(Y), typesystem=typesystem):
            STATEFUL._issame_cache[cache_key] = False
            return False

        sameness = typesystem.__sameness__

        if getattr(sameness, 'use_name', False):
            if typesystem.nameof(X) == typesystem.nameof(Y):
                STATEFUL._issame_cache[cache_key] = True
                return True

        if getattr(sameness, 'use_duck', False):
            if getattr(X, '__dict__', None) == getattr(Y, '__dict__', None):
                STATEFUL._issame_cache[cache_key] = True
                return True

        for condition in getattr(sameness, 'needed', ()):
            if not condition(X, Y):
                STATEFUL._issame_cache[cache_key] = False
                return False

        for condition in getattr(sameness, 'suffices', ()):
            if condition(X, Y):
                STATEFUL._issame_cache[cache_key] = True
                return True

        STATEFUL._issame_cache[cache_key] = False
        return False

    @staticmethod
    def __extends__(t1, t2, typesystem=None):
        cache_key = (id(t1), id(t2), id(typesystem))
        if cache_key in STATEFUL._extends_cache:
            return STATEFUL._extends_cache[cache_key]

        if not STATEFUL.__issame__(typesystem.typeof(t1), typesystem.typeof(t2), typesystem=typesystem):
            STATEFUL._extends_cache[cache_key] = False
            return False

        res = any(STATEFUL.__issame__(base, t2, typesystem=typesystem) for base in getattr(t1, "__mro__", []))
        STATEFUL._extends_cache[cache_key] = res
        return res

    @staticmethod
    def __issup__(typ, other, typesystem=None):
        cache_key = (id(typ), id(other), id(typesystem))
        if cache_key in STATEFUL._issup_cache:
            return STATEFUL._issup_cache[cache_key]

        key = (id(typ), id(other))
        if key in STATEFUL.SUPS:
            return False

        STATEFUL.SUPS.add(key)
        try:
            if typesystem is None:
                from typed.mods.resolve import resolve
                typesystem = resolve.typesystem.entity(typesystem)

            meta_typ = typesystem.typeof(typ)
            meta_other = typesystem.typeof(other)
            if not STATEFUL.__issame__(meta_typ, meta_other, typesystem=typesystem):
                STATEFUL._issup_cache[cache_key] = False
                return False

            for base in getattr(meta_typ, "__mro__", [meta_typ]):
                if "__issup__" in getattr(base, "__dict__", {}):
                    issup = base.__dict__["__issup__"]
                    if issup is not STATEFUL.__issup__:
                        try:
                            res = issup(typ, other)
                            STATEFUL._issup_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            for base in getattr(meta_other, "__mro__", [meta_other]):
                if "__issub__" in getattr(base, "__dict__", {}):
                    issub = base.__dict__["__issub__"]
                    if issub is not STATEFUL.__issub__:
                        try:
                            res = issub(other, typ)
                            STATEFUL._issup_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            if STATEFUL.__extends__(typ, other, typesystem=typesystem):
                STATEFUL._issup_cache[cache_key] = True
                return True

            from typed.mods.err import NotDefined
            STATEFUL._issup_cache[cache_key] = NotDefined
            return NotDefined
        finally:
            STATEFUL.SUPS.remove(key)

    @staticmethod
    def __issub__(typ, other, typesystem=None):
        cache_key = (id(typ), id(other), id(typesystem))
        if cache_key in STATEFUL._issub_cache:
            return STATEFUL._issub_cache[cache_key]

        key = (id(typ), id(other))
        if key in STATEFUL.SUBS:
            return False

        STATEFUL.SUBS.add(key)
        try:
            if typesystem is None:
                from typed.mods.resolve import resolve
                typesystem = resolve.typesystem.entity(typesystem)

            meta_typ = typesystem.typeof(typ)
            meta_other = typesystem.typeof(other)
            if not STATEFUL.__issame__(meta_typ, meta_other, typesystem=typesystem):
                STATEFUL._issub_cache[cache_key] = False
                return False

            for base in getattr(meta_typ, "__mro__", [meta_typ]):
                if "__issub__" in getattr(base, "__dict__", {}):
                    issub = base.__dict__["__issub__"]
                    if issub is not STATEFUL.__issub__:
                        try:
                            res = issub(typ, other)
                            STATEFUL._issub_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            for base in getattr(meta_other, "__mro__", [meta_other]):
                if "__issup__" in getattr(base, "__dict__", {}):
                    issup = base.__dict__["__issup__"]
                    if issup is not STATEFUL.__issup__:
                        try:
                            res = issup(other, typ)
                            STATEFUL._issub_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            res = STATEFUL.__issup__(other, typ, typesystem=typesystem)
            STATEFUL._issub_cache[cache_key] = res
            return res
        finally:
            STATEFUL.SUBS.remove(key)

    @staticmethod
    def __isterm__(typ, trm, typesystem=None):
        cache_key = (id(typ), id(trm), id(typesystem))
        if cache_key in STATEFUL._isterm_cache:
            return STATEFUL._isterm_cache[cache_key]

        key = (id(typ), id(trm))
        if key in STATEFUL.TERMS:
            return False

        STATEFUL.TERMS.add(key)
        try:
            if typesystem is None:
                from typed.mods.resolve import resolve
                typesystem = resolve.typesystem.entity(typesystem)

            meta_typ = typesystem.typeof(typ)

            for base in getattr(meta_typ, "__mro__", [meta_typ]):
                if "__isterm__" in getattr(base, "__dict__", {}):
                    isterm = base.__dict__["__isterm__"]
                    if isterm is not STATEFUL.__isterm__:
                        try:
                            res = isterm(typ, trm)
                            STATEFUL._isterm_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            type_trm = typesystem.typeof(trm)
            for base in getattr(type_trm, "__mro__", [type_trm]):
                if "__issub__" in getattr(base, "__dict__", {}):
                    issub = base.__dict__["__issub__"]
                    if issub is not STATEFUL.__issub__:
                        try:
                            res = issub(type_trm, typ)
                            STATEFUL._isterm_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            res = STATEFUL.__issub__(typ, type_trm, typesystem=typesystem)
            STATEFUL._isterm_cache[cache_key] = res
            return res
        finally:
            STATEFUL.TERMS.remove(key)

    @staticmethod
    def __isequiv__(typ, other, typesystem=None):
        cache_key = (id(typ), id(other), id(typesystem))
        if cache_key in STATEFUL._isequiv_cache:
            return STATEFUL._isequiv_cache[cache_key]

        key = (id(typ), id(other))
        if key in STATEFUL.EQUIVS:
            return False

        STATEFUL.EQUIVS.add(key)
        try:
            if typesystem is None:
                from typed.mods.resolve import resolve
                typesystem = resolve.typesystem.entity(typesystem)

            meta_typ = typesystem.typeof(typ)
            for base in getattr(meta_typ, "__mro__", [meta_typ]):
                if "__isequiv__" in getattr(base, "__dict__", {}):
                    isequiv = base.__dict__["__isequiv__"]
                    if isequiv is not STATEFUL.__isequiv__:
                        try:
                            res = isequiv(typ, other)
                            STATEFUL._isequiv_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            meta_other = typesystem.typeof(other)
            for base in getattr(meta_other, "__mro__", [meta_other]):
                if "__isequiv__" in getattr(base, "__dict__", {}):
                    isequiv = base.__dict__["__isequiv__"]
                    if isequiv is not STATEFUL.__isequiv__:
                        try:
                            res = isequiv(other, typ)
                            STATEFUL._isequiv_cache[cache_key] = res
                            return res
                        except TypeError:
                            pass
                    break

            if STATEFUL.__issame__(typ, other, typesystem=typesystem):
                STATEFUL._isequiv_cache[cache_key] = True
                return True

            if STATEFUL.__issub__(typ, other, typesystem=typesystem) and STATEFUL.__issub__(other, typ, typesystem=typesystem):
                STATEFUL._isequiv_cache[cache_key] = True
                return True

            if STATEFUL.__issup__(typ, other, typesystem=typesystem) and STATEFUL.__issup__(other, typ, typesystem=typesystem):
                STATEFUL._isequiv_cache[cache_key] = True
                return True

            STATEFUL._isequiv_cache[cache_key] = False
            return False
        finally:
            STATEFUL.EQUIVS.remove(key)

class MAGIC:
    def __in__(typ, trm):
        return STATEFUL.__isterm__(typ, trm)

    def __le__(typ, other):
        return STATEFUL.__issub__(typ, other)

    def __lt__(typ, other):
        return STATEFUL.__issub__(typ, other) and not STATEFUL.__issub__(other, typ)

    def __ge__(typ, other):
        return STATEFUL.__issub__(other, typ)

    def __gt__(typ, other):
        return STATEFUL.__issub__(other, typ) and not STATEFUL.__issub__(typ, other)

    def __eq__(typ, other):
        return STATEFUL.__isequiv__(typ, other)

    def __ne__(typ, other):
        return not MAGIC.__eq__(typ, other)

    def __iter__(cls):
        if hasattr(cls, "__terms__"):
            yield from list(cls.__terms__)
            return

        systems = getattr(cls, "__typesystems__", [])
        if systems:
            from typed.mods.typesystem import isterm
            for x in systems[0]:
                if isterm(x, cls):
                    yield x
            return

        raise TypeError(f"Cannot iterate over {getattr(cls, '__name__', str(cls))}")

def _abstract_isterm(univ, stateful, typesystem):
    def __isterm__(typ, trm):
        return stateful.__issub__(trm, univ, typesystem=typesystem)
    return __isterm__

def _universe_issub(univ, other, stateful):
    if "is_universe" in getattr(other, "__dict__", {}) and "is_universe" in getattr(univ, "__dict__", {}):
        return getattr(other, "__level__", -1) <= getattr(univ, "__level__", -1)
    return stateful.__issub__(univ, other)

def _abstract_issub(abs, other, stateful):
    if "is_abstract" in getattr(other, "__dict__", {}) and "is_abstract" in getattr(abs, "__dict__", {}):
        return getattr(other, "__level__", -1) <= getattr(abs, "__level__", -1)
    return stateful.__issub__(abs, other)

@cache
def _typeof_cache(typ, level: int, typesystem):
    from typed.mods.typesystem import typemap
    base = typemap(typ, typesystem=typesystem)
    if level == 1:
        return base
    for i in range(2, level+1):
        base = _typeof_cache(type(base), 1, typesystem)
    return base
