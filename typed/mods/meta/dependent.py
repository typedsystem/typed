from typed.mods.meta.atomic import TYPE, STR, FINITE

class RELATED(TYPE):
    """
    The metatype of dependent types of 'related entities'.
    """
    def __isterm__(typ, trm):
        quantifier = getattr(typ, "__quantifier__", None)
        if not quantifier:
            from typed.mods.resolve import resolve
            quantifier = resolve.logic.quantifier(quantifier)
        entities = getattr(typ, "__entities__", None)
        if not entities:
            return False
        relations = getattr(typ, "__relations__", None)
        from typed.mods.check import require
        require.every.iscallable(relations)
        return all(
            quantifier(relation(trm, entity) for entity in entities)
            for relation in relations
        )

    def __call__(met, entities: tuple[object]=None, relations: tuple[callable]=None, name="Related", base: type=None, quantifier=None, typesystem=None):
        if base is None:
            from typed.mods.types.atomic import Empty
            base = Empty
        if entities is None:
            return base
        from typed.mods.resolve import resolve
        quantifier = resolve.logic.quantifier(quantifier)
        typesystem = resolve.typesystem.entity(typesystem)
        from typed.mods.check import require
        require.every.iscallable(relations)

        if len(entities) == 1 and isinstance(entities[0], tuple):
            entities = entities[0]

        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        name = f"{name}({typesystem.nameof(entities)}, relations={typesystem.nameof(relations)})"
        class Related(metaclass=RELATED):
            __quantifier__ = quantifier
            __entities__ = entities
            __relations__ = relations
            __typesystems__ = {TYPESYSTEM, typesystem}
            __flags__ = Flags(is_dependent=True)

        return Related

class SUBS(RELATED):
    """
    The metatype of dependent 'types of subs' of given entitites.
    """
    def __call__(met, *entities, base: type=None, quantifier=None, typesystem=None):
        from typed.mods.resolve import resolve

        if not entities: entities = None
        elif len(entities) == 1 and isinstance(entities[0], tuple): entities = entities[0]
        return super().__call__(
            name="Subs",
            entities=entities,
            relations=(resolve.typesystem.entity(typesystem).issub,),
            typesystem=typesystem,
            quantifier=quantifier,
            base=base
        )

class SUPS(RELATED):
    """
    The metatype of dependent 'types of sups' of given entitites.
    """
    def __call__(met, *entities, base: type=None, quantifier=None, typesystem=None):
        from typed.mods.resolve import resolve
        if not entities: entities = None
        elif len(entities) == 1 and isinstance(entities[0], tuple): entities = entities[0]
        return super().__call__(
            name="Sups",
            entities=entities,
            relations=(resolve.typesystem.entity(typesystem).issup,),
            typesystem=typesystem,
            quantifier=quantifier,
            base=base
        )

class SAME(RELATED):
    """
    The metatype of dependent 'types of some of them'.
    """
    def __call__(met, *entities, base: type=None, quantifier=None, typesystem=None):
        from typed.mods.resolve import resolve
        if not entities: entities = None
        elif len(entities) == 1 and isinstance(entities[0], tuple): entities = entities[0]
        return super().__call__(
            name="Same",
            entities=entities,
            relations=(resolve.typesystem.entity(typesystem).issame,),
            typesystem=typesystem,
            quantifier=quantifier,
            base=base
        )

class EQUIV(RELATED):
    """
    The metatype of dependent 'equivalent types'.
    """
    def __call__(met, *entities, base: type=None, quantifier=None, typesystem=None):
        from typed.mods.resolve import resolve
        if not entities: entities = None
        elif len(entities) == 1 and isinstance(entities[0], tuple): entities = entities[0]
        return super().__call__(
            name="Equiv",
            entities=entities,
            relations=(resolve.typesystem.entity(typesystem).isequiv,),
            typesystem=typesystem,
            quantifier=quantifier,
            base=base
        )

class HAS(RELATED):
    """
    The metatype of dependent 'has types'.
    """
    def __call__(met, *attrs, quantifier=None):
        from typed.mods.check import require
        from typed.mods.prop import prop
        if len(attrs) == 1 and isinstance(attrs[0], tuple): attrs = attrs[0]
        require.every.isinstance(attrs, str)
        return super().__call__(
            entities=attrs,
            relations=(prop.has,),
            name="Has",
            quantifier=quantifier
        )

class FILTERED(TYPE):
    def __isterm__(typ, trm):
        base = getattr(typ, "__basis__", None)
        from typed.mods.check import require
        require.isinstance(base, type)
        require.isterm(trm, base)
        filters = getattr(typ, "__filters__", [])
        if not filters: return True
        quantifier = getattr(typ, "__quantifier__")
        from typed.mods.resolve import resolve
        quantifier = resolve.logic.quantifier(quantifier)
        require.every.iscallable(filters)
        return quantifier(filter(trm) for filter in filters)

    def __issub__(typ, other):
        base = getattr(typ, "__basis__", None)
        if base and other <= base:
            return True
        from typed.mods.typesystem import issub
        return issub(other, typ)

    def __call__(met, type: type, filters: tuple[callable]=(), quantifier=None, typesystem=None):
        if typesystem is None:
            from typed.mods.resolve import resolve
            typesystem = resolve.typesystem.entity(typesystem)
        name = f"Filtered({typesystem.nameof(type)}, filters={typesystem.nameof(filters)})"
        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM
        from typed.mods.logic import Discourse

        class Filtered(metaclass=FILTERED):
            __typesystems__ = {TYPESYSTEM, typesystem}
            __flags__       = Flags(is_dependent=True)
            __basis__        = type
            __quantifier__  = quantifier
            __filters__     = filters if filters in Discourse else (filters,)

        return Filtered

class REGEX(STR):
    def __isterm__(typ, trm):
        if not isinstance(trm, str):
            return False
        try:
            import re
            pattern = re.compile(typ.__pattern__)
            return pattern.match(trm) is not None
        except:
            return False

    def __call__(typ, pattern):
        from typed.mods.types.atomic import Str, Pattern
        from typed.mods.check import require
        require.isterm(pattern, Pattern)

        display_name = f"Regex({pattern})"

        from typed.mods.flags import Flags
        class Regex(Str, metaclass=REGEX):
            __display__ = display_name
            __name__ = display_name
            __pattern__ = pattern
            __flags__ = Flags(is_dependent=True)

        return Regex


class BOUNDED(FINITE):
    """
    The dependent metatype for 'length-bounded' types.
    """
    def __isterm__(met, trm):
        from typed.mods.typesystem import isterm

        base_type = getattr(met, "__basis__", None)
        bound = getattr(met, "__bound__", -1)
        op = getattr(met, "__op__", None)

        if base_type is None or op is None:
            return False

        if not isterm(trm, base_type):
            return False
        try:
            from typed.mods.poly import sizeof
            return op(sizeof(trm), bound)
        except Exception:
            return False

    def __call__(met, type: type=None, bound=-1, op='==', base: type=None, typesystem=None):
        from typed.mods.types.atomic import Empty
        from typed.mods.check import require
        from typed.mods.resolve import resolve

        typesystem = resolve.typesystem.entity(typesystem)

        if base is None:
            base = Empty

        if type is None:
            return base

        require.isinstance(bound, int)

        if not typesystem.issub(typesystem.typeof(type), FINITE):
            from typed.mods.err import TypeErr
            raise TypeErr(
                message="Type must be a FINITE type.",
                term=type,
                expected=f"subtype of {FINITE}",
                received=typesystem.typeof(type)
            )

        if bound < 0:
            return type

        if isinstance(op, str):
            import operator
            op_map = {
                '<': operator.lt,
                '<=': operator.le,
                '==': operator.eq,
                '!=': operator.ne,
                '>=': operator.ge,
                '>': operator.gt,
            }
            if op not in op_map:
                raise ValueError(f"Unknown operator string: '{op}'. Expected one of {list(op_map.keys())}")
            op_func = op_map[op]
        elif callable(op):
            op_func = op
        else:
            raise TypeError("The 'op' argument must be a string operator or a callable binary function.")

        display_name = f"Bounded({typesystem.nameof(type)}, {typesystem.nameof(op_func)}, {bound})"

        from typed.mods.flags import Flags
        from typed.mods.init import TYPESYSTEM

        class Bounded(type, metaclass=type(met)):
            __kind__         = "type"
            __typesystems__  = {TYPESYSTEM, typesystem}
            __display__      = display_name
            __basis__        = type
            __bound__        = bound
            __op__           = op_func
            __flags__        = Flags(is_dependent=True, is_enumerable=True, is_finite=True, is_bounded=True)

        Bounded.__name__ = display_name
        return Bounded

class VALUES(TYPE):
    def __isterm__(typ, trm):
        return trm in typ.__values__

    def __issub__(typ, other):
        if not getattr(other, "__values__", None):
            return False
        return set(other.__values__).issubset(typ.__values__)

    def __iter__(typ):
        return iter(typ.__values__)

    def __call__(typ, *values, typesystem=None):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        from typed.mods.check import require
        for v in values:
            require.iscallable(hash)
            hash(v)
        require.every.ismember([typesystem.typeof(v) for v in values], typesystem)
        display_name = f"Values({typesystem.nameof(values)})"
        from typed.mods.init import TYPESYSTEM
        from typed.mods.flags import Flags
        class Values(metaclass=VALUES):
            __kind__ = "type"
            __display__ = display_name
            __name__ = display_name
            __typesystems__ = {TYPESYSTEM, typesystem}
            __flags__ = Flags(is_dependent=True)
            __values__ = frozenset(values)
        return Values

class ENUM(TYPE):
    def __isterm__(typ, trm):
        return trm in typ.__values__

    def __issub__(typ, other):
        if not getattr(other, "__values__", None):
            return False
        return set(other.__values__).issubset(typ.__values__)

    def __getattr__(typ, name):
        if name in typ.__kwargs__:
            return typ.__kwargs__[name]
        raise AttributeError(f"Enum has no attribute '{name}'")

    def __iter__(typ):
        return iter(typ.__values__)

    def __call__(typ, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        from typed.mods.check import require
        for v in kwargs.values():
            require.iscallable(hash)
            hash(v)
        values = frozenset(kwargs.values())
        require.every.ismember([typesystem.typeof(v) for v in values], typesystem)
        display_name = f"Enum({', '.join(f'{k}={v}' for k, v in kwargs.items())})"
        from typed.mods.init import TYPESYSTEM
        from typed.mods.flags import Flags
        class Enum(metaclass=ENUM):
            __kind__ = "type"
            __display__ = display_name
            __name__ = display_name
            __typesystems__ = {TYPESYSTEM, typesystem}
            __flags__ = Flags(is_dependent=True)
            __values__ = values
            __kwargs__ = kwargs
        return Enum
