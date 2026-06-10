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

class TypeCheck(metaclass=__CONF__):
    def __init__(
        self,
        lazy:     bool=None,
        defaults: bool=None,
        envs:     list[str]=None
    ):
        if lazy is None:
            from typed.mods.init import __typecheck__
            lazy = __typecheck__.lazy

        if defaults is None:
            from typed.mods.init import __typecheck__
            defaults = __typecheck__.defaults

        if envs is None:
            from typed.mods.init import __typecheck__
            envs = __typecheck__.envs

        from typed.mods.check import check
        check.isinstance(lazy, bool)
        check.isinstance(defaults, bool)
        check.isinstance(envs, list, tuple, set)

        self.lazy = lazy
        self.defaults = defaults
        self.envs = envs

class TypeSystemConf(metaclass=__CONF__):
    def __init__(
        self,
        entity:      type=None,
        sameness:    type=None,
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

        if sameness is None:
            from typed.mods.init import SAMENESS
            sameness = SAMENESS

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

        if quantifiers is None:
            from typed.mods.init import __quantifiers__
            quantifiers = __quantifiers__

        from typed.mods.typesystem import __SAMENESS__, __STATEFUL__, __MAGIC__, __UNIVERSE__, __ABSTRACT__, __TYPESYSTEM__
        from typed.mods.check import check

        check.isinstance(entity, __TYPESYSTEM__)
        check.isinstance(sameness, __SAMENESS__)
        check.isinstance(stateful, __STATEFUL__)
        check.isinstance(magic, __MAGIC__)
        check.isinstance(universe, __UNIVERSE__)
        check.isinstance(abstract, __ABSTRACT__)
        check.isinstance(kinds, set)
        check.isinstance(quantifiers, set)

        if typemap is not None:
            check.isinstance(typemap, dict)

        self.entity = entity
        self.sameness = sameness
        self.stateful = stateful
        self.magic = magic
        self.universe = universe
        self.abstract = abstract
        self._typemap = typemap
        self.kinds = kinds
        self.quantifiers = quantifiers

    @property
    def typemap(self):
        if self._typemap is None:
            from typed.mods.init import __typemap__
            self._typemap = __typemap__()
        return self._typemap

    @typemap.setter
    def typemap(self, value):
        from typed.mods.check import check
        check.isinstance(value, dict)
        self._typemap = value

class Conf(metaclass=__CONF__):
    def __init__(
        self,
        logic:      LogicConf=None,
        typesystem: TypeSystemConf=None,
        err:        ErrConf=None,
        typecheck:  TypeCheck=None
    ):
        if typesystem is None: typesystem = TypeSystemConf()
        if err is None:        err = ErrConf()
        if logic is None:      logic = LogicConf()
        if typecheck is None:  typecheck = TypeCheck()

        from typed.mods.check import check
        check.isinstance(logic, LogicConf)
        check.isinstance(typesystem, TypeSystemConf)
        check.isinstance(err, ErrConf)
        check.isinstance(typecheck, TypeCheck)

        self.typesystem=typesystem
        self.typecheck=typecheck
        self.err=err
        self.logic=logic
