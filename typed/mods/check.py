class Checker:
    def __init__(self, func: callable, name: str = None):
        self.__func__ = func
        self.__name__ = name if name is not None else getattr(func, '__name__', 'checker')
        self.__display__ = self.__name__

    def __call__(self, *args, **kwargs):
        return self.__func__(*args, **kwargs)

def checker(arg, name: str = None):
    if isinstance(arg, str):
        return QuantifiedChecker(quantifier=arg)
    return staticmethod(Checker(func=arg, name=name))

class QuantifiedChecker:
    def __init__(self, quantifier: str, count: int = None):
        self._quantifier = quantifier
        self.count = count

    def __call__(self, count: int):
        return QuantifiedCheck(self._quantifier, count=count)

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

    def istype(self, entities, *typesystems, quantifier=None) -> bool:
        q = self.quantifier

        from typed.mods.typesystem import istype

        if not q(istype(entity, *typesystems) for entity in entities):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entities=entities,
                typesystems=typesystems,
                expected="type",
                quantifier=quantifier
            )
        return True

    def ismeta(self, entities, *typesystems, quantifier=None) -> bool:
        q = self.quantifier

        from typed.mods.typesystem import ismeta

        if not q(ismeta(entity, *typesystems) for entity in entities):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entities=entities,
                typesystems=typesystems,
                expected="meta",
                quantifier=quantifier
            )
        return True

    def isabstract(self, entities, *typesystems, quantifier=None) -> bool:
        q = self.quantifier

        from typed.mods.typesystem import isabstract

        if not q(isabstract(entity, *typesystems) for entity in entities):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entities=entities,
                typesystems=typesystems,
                expected="abstract",
                quantifier=quantifier
            )
        return True

    def isuniverse(self, entities, *typesystems, quantifier=None) -> bool:
        q = self.quantifier

        from typed.mods.typesystem import isuniverse

        if not q(isuniverse(entity, *typesystems) for entity in entities):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entities=entities,
                typesystems=typesystems,
                expected="universe",
                quantifier=quantifier
            )
        return True

    def iscognate(self, types, *others, quantifier=None) -> bool:
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
        from typed.mods.resolve import resolve

        quantifier = resolve.logic.quantifier(quantifier)
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
        from typed.mods.resolve import resolve

        quantifier = resolve.logic.quantifier(quantifier)
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
        from typed.mods.resolve import resolve
        quantifier = resolve.logic.quantifier(quantifier)
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
    some = checker("some")
    every = checker("every")
    none = checker("none")
    only = checker("only")

    @checker
    def istype(entity: type, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import istype
        if not istype(entity, *typesystems, quantifier=quantifier):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entity=entity,
                expcted="type",
                typesystems=typesystems             
            )
        return True

    @checker
    def ismeta(entity: type, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import ismeta
        if not ismeta(entity, *typesystems, quantifier=quantifier):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entity=entity,
                expected="meta",
                typesystems=typesystems
            )
        return True

    @checker
    def isabstract(entity: type, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import isabstract
        if not isabstract(entity, *typesystems, quantifier=quantifier):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entity=entity,
                expected="abstract",
                typesystems=typesystems
            )
        return True

    @checker
    def isuniverse(entity: type, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import isuniverse
        if not isuniverse(entity, *typesystems, quantifier=quantifier):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entity=entity,
                expected="universe",
                typesystems=typesystems
            )
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
    def isterm(term: object, *types: tuple[type], quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import isterm
        if not isterm(term, *types, quantifier=quantifier, typesystem=typesystem):
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

