class Resolver:
    def __init__(self, func: callable, name: str = None):
        self.__func__ = func
        self.__name__ = name if name is not None else getattr(func, '__name__', 'resolver')
        self.__display__ = self.__name__
        self._cache = {}

    def __call__(self, *args, **kwargs):
        cache_key = (
            tuple(id(a) for a in args),
            tuple((k, id(v)) for k, v in sorted(kwargs.items()))
        )

        if cache_key not in self._cache:
            self._cache[cache_key] = self.__func__(*args, **kwargs)

        return self._cache[cache_key]

def resolver(func: callable, name: str = None):
    return staticmethod(Resolver(func=func, name=name))

def resolved(provided: object, default: object) -> object:
    from typed.mods.err import NotDefined
    val = default if provided is None or provided is NotDefined else provided

    if val is default:
        return val

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
            return resolved(provided=conf, default=_conf)
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
            return resolved(provided=multiline, default=c.err.multiline)

    class logic:
        @resolver
        def quantifier(quantifier=None, conf=None):
            from typed.mods.err import NotDefined
            if quantifier is not None and quantifier is not NotDefined:
                return quantifier
            c = resolve.conf(conf)
            if c is None:
                try:
                    from typed.mods.init import some
                    return some
                except ImportError:
                    return any
            return resolved(provided=quantifier, default=c.logic.quantifier)

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
            return resolved(provided=typesystem, default=c.typesystem.entity)

        @resolver
        def sameness(sameness=None, conf=None):
            from typed.mods.err import NotDefined
            if sameness is not None and sameness is not NotDefined:
                return sameness
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import SAMENESS
                return SAMENESS
            return resolved(provided=sameness, default=c.typesystem.sameness)

        @resolver
        def stateful(stateful=None, conf=None):
            from typed.mods.err import NotDefined
            if stateful is not None and stateful is not NotDefined:
                return stateful
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import STATEFUL
                return STATEFUL
            return resolved(provided=stateful, default=c.typesystem.stateful)

        @resolver
        def magic(magic=None, conf=None):
            from typed.mods.err import NotDefined
            if magic is not None and magic is not NotDefined:
                return magic
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import MAGIC
                return MAGIC
            return resolved(provided=magic, default=c.typesystem.magic)

        @resolver
        def universe(universe=None, conf=None):
            from typed.mods.err import NotDefined
            if universe is not None and universe is not NotDefined:
                return universe
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import UNIVERSE
                return UNIVERSE
            return resolved(provided=universe, default=c.typesystem.universe)

        @resolver
        def abstract(abstract=None, conf=None):
            from typed.mods.err import NotDefined
            if abstract is not None and abstract is not NotDefined:
                return abstract
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import ABSTRACT
                return ABSTRACT
            return resolved(provided=abstract, default=c.typesystem.abstract)

        @resolver
        def typemap(typemap=None, conf=None):
            from typed.mods.err import NotDefined
            if typemap is not None and typemap is not NotDefined:
                return typemap
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import __typemap__
                return __typemap__()
            return resolved(provided=typemap, default=c.typesystem.typemap)

        @resolver
        def quantifiers(quantifiers=None, conf=None):
            from typed.mods.err import NotDefined
            if quantifiers is not None and quantifiers is not NotDefined:
                return quantifiers
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import __quantifiers__
                return __quantifiers__
            return resolved(provided=quantifiers, default=c.typesystem.quantifiers)

        @resolver
        def kinds(kinds=None, conf=None):
            from typed.mods.err import NotDefined
            if kinds is not None and kinds is not NotDefined:
                return kinds
            c = resolve.conf(conf)
            if c is None:
                from typed.mods.init import __kinds__
                return __kinds__
            return resolved(provided=kinds, default=c.typesystem.kinds)

    class typecheck:
        @resolver
        def check(check=None, envs=None, conf=None):
            from typed.mods.err import NotDefined
            c = resolve.conf(conf)

            if check is not None and check is not NotDefined:
                chk = check
            else:
                chk = resolved(provided=check, default=getattr(c.typecheck, 'check', True) if c else True)

            if envs is not None and envs is not NotDefined:
                resolved_envs = envs
            else:
                resolved_envs = resolved(provided=envs, default=getattr(c.typecheck, 'envs', ()) if c else ())

            if chk and resolved_envs:
                import os
                current_env = os.getenv("TYPED_ENV", "").upper()
                allowed_envs = {str(e).upper() for e in resolved_envs}
                if current_env not in allowed_envs:
                    chk = False

            return chk

        @resolver
        def lazy(lazy=None, conf=None):
            from typed.mods.err import NotDefined
            if lazy is not None and lazy is not NotDefined:
                return lazy
            c = resolve.conf(conf)
            if c is None:
                return True
            return resolved(provided=lazy, default=c.typecheck.lazy)

        @resolver
        def defaults(defaults=None, conf=None):
            from typed.mods.err import NotDefined
            if defaults is not None and defaults is not NotDefined:
                return defaults
            c = resolve.conf(conf)
            if c is None:
                return False
            return resolved(provided=defaults, default=c.typecheck.defaults) 
