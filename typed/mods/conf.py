class __CONF__(type): pass

class ErrConf(metaclass=__CONF__):
    def __init__(self, multiline: bool=True):
        from typed.mods.check import check
        check.isinstance(multiline, bool)
        self.multiline=multiline

class TypeSystemConf(metaclass=__CONF__):
    def __init__(self, entity: type=None, sameness: type=None):
        if entity is None:
            from typed.mods.init import TYPESYSTEM
            entity = TYPESYSTEM
        if sameness is None:
            from typed.mods.init import SAMENESS
            sameness = SAMENESS

        from typed.mods.typesystem import __TYPESYSTEM__, __SAMENESS__
        from typed.mods.check import check

        check.isinstance(entity, __TYPESYSTEM__)
        check.isinstance(entity, __SAMENESS__)

        self.entity = entity
        self.sameness = sameness

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
