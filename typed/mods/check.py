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
    def __init__(self, quantifier_name: str, n: int = None):
        self.quantifier_name = quantifier_name
        self.n = n

    @property
    def quantifier(self):
        from typed.mods.init import some, every, none, only
        if self.quantifier_name == 'some':
            return some
        elif self.quantifier_name == 'every':
            return every
        elif self.quantifier_name == 'none':
            return none
        elif self.quantifier_name == 'only':
            return only(self.n)
        raise ValueError(f"Unknown quantifier {self.quantifier_name}")

    def istype(self, objs) -> bool:
        from typed.mods.typesystem import istype
        from typed.mods.err import IsNotType
        q = self.quantifier

        if not q(istype(obj) for obj in objs):
            raise IsNotType(object=objs)
        return True

    def iscognate(self, types, *others, quantifier=None) -> bool:
        from typed.mods.typesystem import iscognate
        from typed.mods.err import TypeSystemErr
        q = self.quantifier

        if not q(iscognate(t, *others, quantifier=quantifier) for t in types):
            raise TypeSystemErr(
                details="Types do not share a common typesystem",
                types=(types, *others)
            )
        return True

    def isinstance(self, objs, *classes, quantifier=None) -> bool:
        from typed.mods.err import TypeErr
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some
        q = self.quantifier

        if not q(quantifier(isinstance(obj, cls) for cls in classes) for obj in objs):
            raise TypeErr(
                term=objs,
                expected=classes,
                quantifier=q,
                received=tuple(type(obj) for obj in objs)
            )
        return True

    def isterm(self, objs, *types, quantifier=None) -> bool:
        from typed.mods.err import TypeErr
        from typed.mods.typesystem import isterm
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some
        q = self.quantifier

        if not q(quantifier(isterm(obj, t) for t in types) for obj in objs):
            raise TypeErr(
                term=objs,
                expected=types,
                quantifier=q
            )
        return True

    def ismember(self, types, *typesystems, quantifier=None) -> bool:
        from typed.mods.err import TypeSystemErr, NotDefined
        from typed.mods.typesystem import ismember
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some
        q = self.quantifier

        if not q(quantifier(ismember(t, *typesystems) for t in types)):
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
    def only(n: int) -> QuantifiedCheck:
        """
        Dynamically initializes a QuantifiedCheck for exactly `n` occurrences.
        Example: check.only(2).isinstance(objs, int, str)
        """
        return QuantifiedCheck("only", n=n)

    @checker
    def istype(obj: type) -> bool:
        from typed.mods.typesystem import istype
        if not istype(obj):
            from typed.mods.err import IsNotType
            raise IsNotType(object=obj)
        return True

    @checker
    def iscognate(type: type, *others: tuple[type], quantifier=None) -> bool:
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
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some

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
        from typed.mods.typesystem import isterm
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some

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
        from typed.mods.typesystem import ismember
        if quantifier is None:
            from typed.mods.init import some
            quantifier = some

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
