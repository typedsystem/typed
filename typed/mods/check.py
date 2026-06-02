class Checker:
    def __init__(self, func: callable, name: str = None):
        self.__func__ = func
        self.__name__ = name if name is not None else getattr(func, '__name__', 'checker')
        self.__display__ = self.__name__

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)

def checker(func: callable, name: str = None) -> staticmethod: 
    return staticmethod(Checker(func=func, name=name))

class QuantifiedCheck:
    def __init__(self, quantifier: str, count: int = None):
        self._quantifier = quantifier
        self.count = count

    @property
    def quantifier(self):
        from typed.mods.init import some, every, none, only
        if self._quantifier == 'some':
            return some
        elif self._quantifier == 'every':
            return every
        elif self._quantifier == 'none':
            return none
        elif self._quantifier == 'only':
            return only(self.count)
        raise ValueError(f"Unknown quantifier {self._quantifier}")

    def istype(self, objs) -> bool:
        quantifier = self.quantifier

        from typed.mods.typesystem import istype

        if not quantifier(istype(obj) for obj in objs):
            from typed.mods.err import IsNotType
            raise IsNotType(object=objs)
        return True

    def iscognate(self, types, *others, quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        q = self.quantifier

        from typed.mods.typesystem import iscognate

        if not q(iscognate(t, *others, quantifier=quantifier) for t in types):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                details="Types do not share a common typesystem",
                types=(types, *others)
            )
        return True

    def isinstance(self, objs, *classes, quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        q = self.quantifier

        if not q(quantifier(isinstance(obj, cls) for cls in classes) for obj in objs):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=objs,
                expected=classes,
                quantifier=q,
                received=tuple(type(obj) for obj in objs)
            )
        return True

    def isterm(self, objs, *types, quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        q = self.quantifier

        from typed.mods.typesystem import isterm

        if not q(quantifier(isterm(obj, t) for t in types) for obj in objs):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=objs,
                expected=types,
                quantifier=q
            )
        return True

    def ismember(self, types, *typesystems, quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        q = self.quantifier

        from typed.mods.typesystem import ismember

        if not q(quantifier(ismember(t, *typesystems) for t in types)):
            from typed.mods.err import TypeSystemErr, NotDefined
            raise TypeSystemErr(
                type=types,
                typesystems=typesystems,
                quantifier=q,
                received=tuple(getattr(t, "__typesystems__", NotDefined) for t in types)
            )
        return True

    def satisfy(self, conditions, *args) -> bool:
        from typed.mods.err import NotSatisfied
        q = self.quantifier

        if not q(cond(*args) is True for cond in conditions):
            raise NotSatisfied(
                condition=q,
                args=args
            )
        return True

class check:
    some  = QuantifiedCheck("some")
    every = QuantifiedCheck("every")
    none  = QuantifiedCheck("none")

    @staticmethod
    def only(count: int) -> QuantifiedCheck:
        return QuantifiedCheck("only", count=count)

    @checker
    def istype(obj: type) -> bool:
        from typed.mods.typesystem import istype
        if not istype(obj):
            from typed.mods.err import IsNotType
            raise IsNotType(object=obj)
        return True

    @checker
    def iscognate(type: type, *others: tuple[type], quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        from typed.mods.typesystem import iscognate
        if not iscognate(type, *others, quantifier=quantifier):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                details="Types do not share a common typesystem",
                types=(type, *others),
                typesystems=(*(getattr(type, "__typesystems__", ())), *(getattr(other, "__typesystems__", ()) for other in others))
            )
        return True

    @checker
    def isinstance(obj: object, *classes: tuple[type], quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        if not quantifier(isinstance(obj, cls) for cls in classes):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=obj,
                expected=classes,
                quantifier=quantifier,
                received=type(obj)
            )
        return True

    @checker
    def isterm(term: object, *types: tuple[type], quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        from typed.mods.typesystem import isterm
        if not isterm(term, *types, quantifier=quantifier):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=term,
                expected=types,
                quantifier=quantifier
            )
        return True

    @checker
    def ismember(type: type, *typesystems: tuple[type], quantifier=None) -> bool:
        quantifier = resolve.quantifier(quantifier)
        from typed.mods.typesystem import ismember

        if not ismember(type, *typesystems, quantifier=quantifier):
            from typed.mods.err import NotDefined
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                type=type,
                typesystems=typesystems,
                quantifier=quantifier,
                received=getattr(type, "__typesystems__", NotDefined)
            )
        return True

    @checker
    def satisfy(condition: callable, *args: tuple) -> bool:
        check.isinstance(condition, callable)
        if condition(*args) is not True:
            from typed.mods.err import NotSatisfied
            raise NotSatisfied(
                condition=condition,
                args=args
            )
        return True

def _resolve(provided: object, default: object) -> object:
    from typed.mods.err import NotDefined
    val = default if provided is None or provided is NotDefined else provided

    check.isinstance(val, type(default))
    return val

class resolve:
    """
    Resolves optional arguments to their global typed configurations,
    ensuring strict type safety.
    """
    @staticmethod
    def conf(conf=None):
        from typed.mods.init import conf as _conf
        return _resolve(
            provided=conf,
            default=_conf
        )

    class logic:
        @staticmethod
        def quantifier(quantifier=None, conf=None):
            conf = resolve.conf(conf)
            return _resolve(
                provided=quantifier,
                default=conf.logic.quantifier
            )

    @staticmethod
    def sameness(sameness=None, conf=None):
        conf = resolve.conf(conf)
        return _resolve(
            provided=sameness,
            default=conf.typesystem.sameness
        )

    @staticmethod
    def typesystem(typesystem=None, conf=None):
        conf = resolve.conf(conf)
        return _resolve(
            provided=typesystem,
            default=conf.typesystem.entity
        )

    @staticmethod
    def universe(universe=None, conf=None):
        conf = resolve.conf(conf)
        return _resolve(
            provided=universe,
            default=conf.typesystem.universe
        )

    @staticmethod
    def abstract(abstract=None, conf=None):
        conf = resolve.conf(conf)
        return _resolve(
            provided=abstract,
            default=conf.typesystem.abstract
        )
