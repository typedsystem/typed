class __CONF__(type): pass

class ErrConf(metaclass=__CONF__):
    def __init__(
        self,
        multiline: bool=True
    ):
        from typed.mods.check import check
        check.isinstance(multiline, bool)

        self.multiline=multiline

class TypeSystemConf(metaclass=__CONF__):
    def __init__(
        self,
        entity:      type=None,
        universe:    type=None,
        abstract:    type=None,
        quantifiers: type=None,
        typemap:     dict=None,
        is_strict:   bool=True
    ):
        if entity      is None:
            from typed.mods.init import TYPESYSTEM
            entity = TYPESYSTEM
        if universe    is None: universe    = entity.__universe__
        if abstract    is None: abstract    = entity.__abstract__
        if quantifiers is None: quantifiers = entity.__members__.get("quantifiers", set())
        if typemap     is None: typemap     = entity.__typemap__

        from typed.mods.typesystem import __TYPESYSTEM__, __UNIVERSE__, __ABSTRACT__
        from typed.mods.check import check

        check.isinstance(entity,   __TYPESYSTEM__)
        check.isinstance(universe, __UNIVERSE__)
        check.isinstance(abstract, __ABSTRACT__)
        check.isinstance(quantifiers, set)
        check.isinstance(typemap, dict)
        check.isinstance(is_strict, bool)

        self.entity = entity
        self.universe = universe
        self.abstract = abstract
        self.quantifiers = quantifiers
        self.typemap = typemap
        self.is_strict = is_strict

class Conf(metaclass=__CONF__):
    def __init__(
        self,
        enabled:    bool=True,
        typesystem: TypeSystemConf=None,
        err:        ErrConf=None,
        **kwargs
    ):
        if typesystem is None:
            typesystem = TypeSystemConf()
        if err is None:
            err = ErrConf()

        from typed.mods.check import check
        check.isinstance(enabled, bool)
        check.isinstance(typesystem, TypeSystemConf)
        check.isinstance(err, ErrConf)

        self.enabled=enabled
        self.typesystem=typesystem
        self.err=err

        for k, v in kwargs.items():
            setattr(self, k, v)
