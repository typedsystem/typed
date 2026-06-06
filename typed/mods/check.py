class Checker:
    def __init__(self, func: callable = None, name: str = None, quantifier: str = None, count: int = None):
        self.__func__ = func
        self._quantifier = quantifier
        self.count = count
        self.__name__ = name if name is not None else getattr(func, '__name__', 'checker')
        self.__display__ = self.__name__

    def __call__(self, *args, **kwargs):
        if self.__func__ is not None:
            return self.__func__(*args, **kwargs)
        if self._quantifier == 'only' and len(args) == 1 and isinstance(args[0], int):
            return Checker(quantifier=self._quantifier, count=args[0])

        raise TypeError("This Checker is not callable in this context.")

    @property
    def quantifier(self):
        if self._quantifier is None:
            return None
        if self._quantifier == 'some':
            from typed.mods.init import some
            return some
        elif self._quantifier == 'every':
            from typed.mods.init import every
            return every
        elif self._quantifier == 'none':
            from typed.mods.init import none
            return none
        elif self._quantifier == 'only':
            from typed.mods.init import only
            return only(self.count)
        raise ValueError(f"Unknown quantifier {self._quantifier}")

    def istype(self, entities, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import istype
        q = self.quantifier

        if q is None:
            if not istype(entities, *typesystems, quantifier=quantifier):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    entity=entities,
                    expected="type",
                    typesystems=typesystems
                )
            return True

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
        from typed.mods.typesystem import ismeta
        q = self.quantifier

        if q is None:
            if not ismeta(entities, *typesystems, quantifier=quantifier):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    entity=entities,
                    expected="meta",
                    typesystems=typesystems
                )
            return True

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
        from typed.mods.typesystem import isabstract
        q = self.quantifier

        if q is None:
            if not isabstract(entities, *typesystems, quantifier=quantifier):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    entity=entities,
                    expected="abstract",
                    typesystems=typesystems
                )
            return True

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
        from typed.mods.typesystem import isuniverse
        q = self.quantifier

        if q is None:
            if not isuniverse(entities, *typesystems, quantifier=quantifier):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    entity=entities,
                    expected="universe",
                    typesystems=typesystems
                )
            return True

        if not q(isuniverse(entity, *typesystems) for entity in entities):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entities=entities,
                typesystems=typesystems,
                expected="universe",
                quantifier=quantifier
            )
        return True

    def isentity(self, objs) -> bool:
        from typed.mods.typesystem import isentity
        q = self.quantifier

        if q is None:
            if not isentity(objs):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    entity=objs,
                    expected="struc"
                )
            return True

        if not q(isentity(obj) for obj in objs):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                entities=objs,
                expected="struc",
                quantifier=q
            )
        return True

    def iscognate(self, strucs, *others, quantifier=None) -> bool:
        from typed.mods.typesystem import iscognate
        q = self.quantifier

        if q is None:
            if not iscognate(strucs, *others, quantifier=quantifier):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    details="Types do not share a common typesystem",
                    types=(strucs, *others)
                )
            return True

        if not q(iscognate(s, *others, quantifier=quantifier) for s in strucs):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                details="Types do not share a common typesystem",
                types=(strucs, *others),
                quantifier=q
            )
        return True

    def iscongruent(self, strucs, *others, quantifier=None) -> bool:
        from typed.mods.typesystem import iscongruent
        q = self.quantifier

        if q is None:
            if not iscongruent(strucs, *others, quantifier=quantifier):
                from typed.mods.err import TypeSystemErr
                raise TypeSystemErr(
                    details="Structures are not congruent",
                    types=(strucs, *others)
                )
            return True

        if not q(iscongruent(s, *others, quantifier=quantifier) for s in strucs):
            from typed.mods.err import TypeSystemErr
            raise TypeSystemErr(
                details="Structures are not congruent",
                types=(strucs, *others),
                quantifier=q
            )
        return True

    def iscallable(self, objs) -> bool:
        q = self.quantifier

        if q is None:
            if not callable(objs):
                from typed.mods.err import TypeErr
                raise TypeErr(
                    term=objs,
                    expected=("callable",),
                    received=type(objs)
                )
            return True

        if not q(callable(obj) for obj in objs):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=objs,
                expected=("callable",),
                quantifier=q,
                received=tuple(type(obj) for obj in objs)
            )
        return True

    def isinstance(self, objs, *classes, quantifier=None) -> bool:
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            if not logic_q(isinstance(objs, cls) for cls in classes):
                from typed.mods.err import TypeErr
                raise TypeErr(
                    term=objs,
                    expected=classes,
                    quantifier=logic_q,
                    received=type(objs)
                )
            return True

        if not q(logic_q(isinstance(obj, cls) for cls in classes) for obj in objs):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=objs,
                expected=classes,
                quantifier=q,
                received=tuple(type(obj) for obj in objs)
            )
        return True

    def isterm(self, objs, *types, quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import isterm
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            if not isterm(objs, *types, quantifier=quantifier, typesystem=typesystem):
                from typed.mods.err import TypeErr
                raise TypeErr(
                    term=objs,
                    expected=types,
                    quantifier=quantifier
                )
            return True

        if not q(logic_q(isterm(obj, t) for t in types) for obj in objs):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=objs,
                expected=types,
                quantifier=q
            )
        return True

    def ismember(self, types, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import ismember
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            if not ismember(types, *typesystems, quantifier=quantifier):
                from typed.mods.err import NotDefined, TypeSystemErr
                raise TypeSystemErr(
                    type=types,
                    typesystems=typesystems,
                    quantifier=quantifier,
                    received=getattr(types, "__typesystems__", NotDefined)
                )
            return True

        if not q(logic_q(ismember(t, *typesystems) for t in types)):
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

        if q is None:
            self.isinstance(conditions, callable)
            if conditions(*args) is not True:
                raise NotSatisfied(
                    condition=conditions,
                    args=args
                )
            return True

        if not q(cond(*args) is True for cond in conditions):
            raise NotSatisfied(
                condition=q,
                args=args
            )
        return True

def checker(arg=None, name: str = None, quantifier: str = None, count: int = None):
    if isinstance(arg, str):
        return Checker(quantifier=arg)
    if callable(arg):
        return staticmethod(Checker(func=arg, name=name))
    return Checker(quantifier=quantifier, count=count)


__checker__ = Checker(quantifier=None)

class check:
    some = checker("some")
    every = checker("every")
    none = checker("none")
    only = checker("only")

    istype = __checker__.istype
    ismeta = __checker__.ismeta
    isabstract = __checker__.isabstract
    isuniverse = __checker__.isuniverse
    isentity = __checker__.isentity
    iscognate = __checker__.iscognate
    iscongruent = __checker__.iscongruent
    ismember = __checker__.ismember
    isinstance = __checker__.isinstance
    iscallable = __checker__.iscallable
    isterm = __checker__.isterm
    ismember = __checker__.ismember
    satisfy = __checker__.satisfy
