class __CONF__(type): pass

class ErrConf(metaclass=__CONF__):
    def __init__(self, multiline: bool=True):
        from typed.mods.check import check
        check.isinstance(multiline, bool)
        self.multiline=multiline

class LogicConf(metaclass=__CONF__):
    def __init__(self, quantifier: type=None) -> None:
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some

        from typed.mods.check import check
        from typed.mods.logic import Quantifier

        check.isinstance(quantifier, Quantifier)
        self.quantifier = quantifier

class TypeSystemConf(metaclass=__CONF__):
    def __init__(
        self,
        entity:      type=None,
        stateful:    type=None,
        magic:       type=None,
        universe:    type=None,
        abstract:    type=None,
        kinds:       set=None,
        typemap:     dict=None,
        quantifiers: set=None,
    ):
        if entity is None:
            from typed.mods.init import TYPESYSTEM
            entity = TYPESYSTEM

        if stateful is None:
            from typed.mods.init import STATEFUL
            stateful = STATEFUL

        if magic is None:
            from typed.mods.init import MAGIC
            magic = MAGIC

        if universe is None:
            from typed.mods.init import UNIVERSE
            universe = UNIVERSE

        if abstract is None:
            from typed.mods.init import ABSTRACT
            abstract = ABSTRACT

        if kinds is None:
            from typed.mods.init import __kinds__
            kinds = __kinds__

        if typemap is None:
            from typed.mods.init import __typemap__
            typemap = __typemap__()

        if quantifiers is None:
            from typed.mods.init import __quantifiers__
            quantifiers = __quantifiers__

        from typed.mods.typesystem import __STATEFUL__, __MAGIC__, __UNIVERSE__, __ABSTRACT__, __TYPESYSTEM__
        from typed.mods.check import check

        check.isinstance(entity, __TYPESYSTEM__)
        check.isinstance(stateful, __STATEFUL__)
        check.isinstance(magic, __MAGIC__)
        check.isinstance(universe, __UNIVERSE__)
        check.isinstance(abstract, __ABSTRACT__)
        check.isinstance(typemap, dict)
        check.isinstance(kinds, set)
        check.isinstance(quantifiers, set)

        self.entity = entity
        self.stateful = stateful
        self.magic = magic
        self.universe = universe
        self.abstract = abstract
        self.typemap = typemap
        self.kinds = kinds
        self.quantifiers = quantifiers

class Conf(metaclass=__CONF__):
    def __init__(
        self,
        logic:      LogicConf=None,
        typesystem: TypeSystemConf=None,
        err:        ErrConf=None,
    ):
        if typesystem is None:
            typesystem = TypeSystemConf()
        if err is None:
            err = ErrConf()
        if logic is None:
            logic = LogicConf()

        from typed.mods.check import check
        check.isinstance(logic, LogicConf)
        check.isinstance(typesystem, TypeSystemConf)
        check.isinstance(err, ErrConf)

        self.typesystem=typesystem
        self.err=err
        self.logic=logic
