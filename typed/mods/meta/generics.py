from typed.mods.meta.base import TYPE

class EXTENSIONAL(TYPE):
    def __isterm__(typ, trm):
        quantifier = getattr(typ, "__quantifier__", None)
        types = tuple(getattr(typ, "__types__", (typ,)))
        from typed.mods.core import isterm
        return isterm(trm, *types, quantifier=quantifier)

    def __issub__(typ, other):
        quantifier = getattr(typ, "__quantifier__", None)
        types = (t for t in getattr(typ, "__types__", (typ,)))
        others = (o for o in getattr(other, "__types__", (other,)))
        from typed.mods.core import issub
        if getattr(other, "is_extensional", False):
            return quantifier(issub(o, *types, quantifier=quantifier) for o in others)
        return issub(other, *types, quantifier=quantifier)

    def __call__(met, *types, base=None, quantifier=None, typesystem=None):
        if not isinstance(base, type):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=EXTENSIONAL.__call__,
                arg=base,
                expected=type,
                received=type(base)
            )
        from typed.mods.core import Quantifier
        if not isinstance(quantifier, Quantifier):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=EXTENSIONAL.__call__,
                arg=quantifier,
                expected=Quantifier,
                received=type(quantifier)
            )

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(quantifier)

        types = set(types)

        for t in types:
            if not isinstance(t, type):
                raise TypeErr(
                    term=EXTENSIONAL.__call__,
                    arg=t,
                    expected=type,
                    received=type(t)
                )
            typesystem.check(t)

        if not types:
            return base

        if len(types) == 1:
            return tuple(types)[0]

        from typed.mods.err import NotDefined
        from typed.mods.core import names

        name = f"Union({names(*types)})"

        return TYPE.__call__(name, tuple(types), {
            'is_type': True,
            'is_parametric': True,
            'is_extensional': True,
            '__display__': name,
            '__types__': types,
            '__null__': NotDefined
        })


class UNION(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.core import isterm, some
        return any(isterm(trm, t) for t in getattr(typ, "__types__", set()))

    def __issub__(typ, other):
        from typed.mods.core import issub, some
        types = getattr(typ, "__types__", set())
        others = getattr(other, "__types__", set())

        if getattr(other, "is_union", False):
            if others:
                return any(issub(o, *types) for o in others)
            return True
        return issub(other, *types)

    def __call__(met, *types, typesystem=None):
        types = set(types)

        if not types:
            from typed.mods.types.base import Empty
            return Empty

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(*tuple(types))

        if len(types) == 1:
            return types[0]

        from typed.mods.err import NotDefined
        from typed.mods.core import names

        name = f"Union({names(*types)})"

        return TYPE.__call__(name, tuple(types), {
            'is_type': True,
            'is_union': True,
            'is_parametric': True,
            '__display__': name,
            '__types__': types,
            '__null__': NotDefined
        })

class INTER(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.core import isterm
        return all(isterm(trm, t) for t in getattr(typ, "__types__", set()))

    def __issub__(typ, other):
        from typed.mods.core import issub
        types = getattr(typ, "__types__", set())
        others = getattr(other, "__types__", set())

        if getattr(other, "is_union", False):
            if others:
                return any(issub(o, *types) for o in others)
            return True
        return issub(other, *types)

    def __call__(met, *types, typesystem=None):
        types = set(types)

        if not types:
            from typed.mods.types.base import Empty
            return Empty

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(*tuple(types))

        if len(types) == 1:
            return types[0]

        from typed.mods.err import NotDefined
        from typed.mods.core import names

        name = f"Union({names(*types)})"

        return TYPE.__call__(name, tuple(types), {
            'is_type': True,
            'is_union': True,
            'is_parametric': True,
            '__display__': name,
            '__types__': types,
            '__null__': NotDefined
        })

class PROD(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.core import isterm
        if not isterm(trm, tuple):
            return False
        if len(trm) != len(typ.__types__):
            return False
        return all(isterm(x, t) for x, t in zip(trm, typ.__types__))

    def __issub__(typ, other):
        from typed.mods.core import issub
        types = getattr(typ, "__types__", set())
        others = getattr(other, "__types__", set())

        if getattr(other, "is_prod", False):
            if not types: return True
            if not others: return False
            if len(types) != len(others): return False

            return all(issub(others[i], types[i]) for i in range(0, len(types)))

        return False

    def __call__(met, *types, typesystem=None):
        if not types:
            from typed.mods.types.base import Tuple
            return Tuple

        if typesystem is None:
            from typed.mods.core import TYPESYSTEM
            typesystem = TYPESYSTEM

        typesystem.check(*tuple(types))

        if len(types) == 1:
            return types[0]

        from typed.mods.core import names, null
        from typed.mods.err import NotDefined

        name = f"Prod({names(*types)})"
        nulls = tuple(null(t) for t in types if null(t) is not NotDefined)

        return TYPE.__call__(name, types, {
            'is_type': True,
            'is_parametric': True,
            'is_prod': True,
            '__display__': name,
            '__types__': types,
            '__null__': nulls if len(nulls) == len(types) else NotDefined
        })


