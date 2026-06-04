class Resolver:
    def __init__(self, func: callable, name: str = None):
        self.__func__ = func
        self.__name__ = name if name is not None else getattr(func, '__name__', 'resolver')
        self.__display__ = self.__name__

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)

def resolver(func: callable, name: str = None):
    return staticmethod(Resolver(func=func, name=name))

def _resolve(provided: object, default: object) -> object:
    from typed.mods.err import NotDefined
    val = default if provided is None or provided is NotDefined else provided

    from typed.mods.check import check

    check.isinstance(val, type(default))
    return val

class resolve:
    @resolver
    def conf(conf=None):
        from typed.mods.err import NotDefined
        if conf is not None and conf is not NotDefined:
            return conf
        try:
            from typed.mods.init import conf as _conf
            return _resolve(provided=conf, default=_conf)
        except ImportError:
            return None

    class err:
        @resolver
        def multiline(multiline=None, conf=None):
            from typed.mods.err import NotDefined
            if multiline is not None and multiline is not NotDefined:
                return multiline
            c = resolve.conf(conf)
            if c is None:
                return True
            return _resolve(provided=multiline, default=c.err.multiline)

    class logic:
        @resolver
        def quantifier(quantifier=None, conf=None):
            from typed.mods.err import NotDefined
            if quantifier is not None and quantifier is not NotDefined:
                return quantifier
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import some
                return some
            return _resolve(provided=quantifier, default=c.logic.quantifier)

    class typesystem:
        @resolver
        def entity(typesystem=None, conf=None):
            from typed.mods.err import NotDefined
            if typesystem is not None and typesystem is not NotDefined:
                return typesystem
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import TYPESYSTEM
                return TYPESYSTEM
            return _resolve(provided=typesystem, default=c.typesystem.entity)

        @resolver
        def stateful(stateful=None, conf=None):
            from typed.mods.err import NotDefined
            if stateful is not None and stateful is not NotDefined:
                return stateful
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import STATEFUL
                return STATEFUL
            return _resolve(provided=stateful, default=c.typesystem.stateful)

        @resolver
        def magic(magic=None, conf=None):
            from typed.mods.err import NotDefined
            if magic is not None and magic is not NotDefined:
                return magic
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import MAGIC
                return MAGIC
            return _resolve(provided=magic, default=c.typesystem.magic)

        @resolver
        def universe(universe=None, conf=None):
            from typed.mods.err import NotDefined
            if universe is not None and universe is not NotDefined:
                return universe
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import UNIVERSE
                return UNIVERSE
            return _resolve(provided=universe, default=c.typesystem.universe)

        @resolver
        def abstract(abstract=None, conf=None):
            from typed.mods.err import NotDefined
            if abstract is not None and abstract is not NotDefined:
                return abstract
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import ABSTRACT
                return ABSTRACT
            return _resolve(provided=abstract, default=c.typesystem.abstract)

        @resolver
        def typemap(typemap=None, conf=None):
            from typed.mods.err import NotDefined
            if typemap is not None and typemap is not NotDefined:
                return typemap
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import __typemap__
                return __typemap__()
            return _resolve(provided=typemap, default=c.typesystem.typemap)

        @resolver
        def quantifiers(quantifiers=None, conf=None):
            from typed.mods.err import NotDefined
            if quantifiers is not None and quantifiers is not NotDefined:
                return quantifiers
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import __quantifiers__
                return __quantifiers__
            return _resolve(provided=quantifiers, default=c.typesystem.quantifiers)

        @resolver
        def kinds(kinds=None, conf=None):
            from typed.mods.err import NotDefined
            if kinds is not None and kinds is not NotDefined:
                return kinds
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import __kinds__
                return __kinds__
            return _resolve(provided=kinds, default=c.typesystem.kinds)
