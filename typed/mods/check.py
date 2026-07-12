class __CHECKER__(type):
    pass

class Checker(metaclass=__CHECKER__):
    def __init__(self, func: callable = None, name: str = None, quantifier: str = None, count: int = None, explode: bool = True):
        self.__func__ = func
        self._quantifier = quantifier
        self.count = count
        self.explode = explode
        self.__name__ = name if name is not None else getattr(func, '__name__', 'checker')
        self.__display__ = self.__name__

    def __call__(self, *args, **kwargs):
        if self.__func__ is not None:
            return self.__func__(*args, **kwargs)
        if self._quantifier == 'only' and len(args) == 1 and isinstance(args[0], int):
            return Checker(quantifier=self._quantifier, count=args[0], explode=self.explode)

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

class TypedChecker(Checker):
    def _expected(self, kind, typesystems):
        from typed.mods.resolve import resolve
        expected_list = []
        for ts in (typesystems if typesystems else (None,)):
            ts_obj = resolve.typesystem.entity(ts)
            if kind in ("universe", "abstract"):
                expected_list.extend(ts_obj.__members__[kind].values())
            elif kind in ("member", "entity"):
                for k in ts_obj.__kinds__:
                    if k in ("universe", "abstract"):
                        expected_list.extend(ts_obj.__members__[k].values())
                    else:
                        expected_list.extend(ts_obj.__members__.get(k, []))
            else:
                expected_list.extend(ts_obj.__members__.get(kind, []))
        return tuple(expected_list)

    def hint_dom(self, func, expected_dom, received_dom) -> bool:
        if expected_dom and received_dom and expected_dom != received_dom:
            if self.explode:
                from typed.mods.err import HintErr
                raise HintErr(
                    message="Domain mismatch with actual Python hints",
                    func=func,
                    expected=expected_dom,
                    received=received_dom
                )
            return False
        return True

    def hint_cod(self, func, expected_cod, received_cod) -> bool:
        if expected_cod and received_cod and expected_cod != received_cod:
            if self.explode:
                from typed.mods.err import HintErr
                raise HintErr(
                    message="Codomain mismatch with actual Python hints",
                    func=func,
                    expected=expected_cod,
                    received=received_cod
                )
            return False
        return True

    def bind_dom(self, func, sig, args, kwargs) -> bool:
        from typed.mods.typesystem import typeof, isterm
        from typed.helper.func import _reduce_args
        arguments = _reduce_args(sig.args, *args, **kwargs)

        for i, arg in enumerate(sig.args):
            if i < len(sig.dom):
                expected_type = sig.dom[i]
                if arg.name in arguments:
                    actual_value = arguments[arg.name]
                    if not isterm(actual_value, expected_type):
                        if self.explode:
                            from typed.mods.err import DomErr
                            raise DomErr(
                                func=func,
                                arg=arg.name,
                                expected=expected_type,
                                received=typeof(actual_value)
                            )
                        return False
        return True

    def bind_cod(self, func, sig, result) -> bool:
        from typed.mods.typesystem import typeof, isterm
        if sig.cod is not None:
            if not isterm(result, sig.cod):
                if self.explode:
                    from typed.mods.err import CodErr
                    raise CodErr(
                        func=func,
                        expected=sig.cod,
                        received=typeof(result)
                    )
                return False
        return True

    def issafe(self, func, sig, args, kwargs, result) -> bool:
        if not self.bind_dom(func, sig, args, kwargs):
            return False
        if not self.bind_cod(func, sig, result):
            return False
        return True

    def istype(self, entities, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import istype
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = istype(entities, *typesystems, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="istype",
                        term=entities,
                        expected=self._expected("type", typesystems),
                        received=entities,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(istype(entity, *typesystems) for entity in entities))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="istype",
                    term=entities,
                    expected=self._expected("type", typesystems),
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def ismeta(self, entities, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import ismeta
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = ismeta(entities, *typesystems, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="ismeta",
                        term=entities,
                        expected=self._expected("meta", typesystems),
                        received=entities,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(ismeta(entity, *typesystems) for entity in entities))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="ismeta",
                    term=entities,
                    expected=self._expected("meta", typesystems),
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def isabstract(self, entities, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import isabstract
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = isabstract(entities, *typesystems, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isabstract",
                        term=entities,
                        expected=self._expected("abstract", typesystems),
                        received=entities,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(isabstract(entity, *typesystems) for entity in entities))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isabstract",
                    term=entities,
                    expected=self._expected("abstract", typesystems),
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def isuniverse(self, entities, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import isuniverse
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = isuniverse(entities, *typesystems, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isuniverse",
                        term=entities,
                        expected=self._expected("universe", typesystems),
                        received=entities,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(isuniverse(entity, *typesystems) for entity in entities))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isuniverse",
                    term=entities,
                    expected=self._expected("universe", typesystems),
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def isentity(self, objs) -> bool:
        from typed.mods.typesystem import isentity
        q = self.quantifier

        if q is None:
            res = isentity(objs)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isentity",
                        term=objs,
                        expected=self._expected("entity", ()),
                        received=objs
                    )
                return False
            return True

        res = q(isentity(obj) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isentity",
                    term=objs,
                    expected=self._expected("entity", ()),
                    received=objs,
                    quantifier=q
                )
            return False
        return True

    def isfunc(self, objs) -> bool:
        from typed.mods.types.func import Func
        from typed.mods.typesystem import isterm
        q = self.quantifier

        if q is None:
            res = isterm(objs, Func)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isfunc",
                        term=objs,
                        expected=(Func,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(isterm(obj, Func) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isfunc",
                    term=objs,
                    expected=(Func,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def ishinted(self, objs, dom: bool = True, cod: bool = True) -> bool:
        from typed.mods.func import signature
        from typed.mods.err import NotDefined
        q = self.quantifier

        if q is None:
            sig = signature(objs)
            if dom:
                non_hinted = [a.name for a in sig.args if a.hint is None or a.hint is NotDefined]
                if non_hinted:
                    if self.explode:
                        from typed.mods.err import HintErr
                        raise HintErr(
                            term=objs,
                            message=f"Missing type hints for parameters: {', '.join(non_hinted)}"
                        )
                    return False
            if cod:
                if sig.cod is None:
                    if self.explode:
                        from typed.mods.err import HintErr
                        raise HintErr(
                            term=objs,
                            message="Missing return type hint"
                        )
                    return False
            return True

        def _check(f):
            try:
                sig = signature(f)
            except Exception:
                return False
            if dom:
                if any(a.hint is None or a.hint is NotDefined for a in sig.args):
                    return False
            if cod:
                if sig.cod is None:
                    return False
            return True

        res = q(_check(f) for f in objs)
        if not res:
            if self.explode:
                from typed.mods.err import HintErr
                raise HintErr(
                    func="ishinted",
                    term=objs,
                    quantifier=q,
                    message="Missing type hints in one or more quantified functions"
                )
            return False
        return True

    def istyped(self, objs) -> bool:
        from typed.mods.types.func import Typed
        from typed.mods.typesystem import isterm
        q = self.quantifier

        if q is None:
            res = isterm(objs, Typed)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="istyped",
                        term=objs,
                        expected=(Typed,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(isterm(obj, Typed) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="istyped",
                    term=objs,
                    expected=(Typed,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def islazy(self, objs) -> bool:
        from typed.mods.meta.func import LAZY
        from typed.mods.typesystem import isterm
        q = self.quantifier

        if q is None:
            res = isterm(objs, LAZY)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="islazy",
                        term=objs,
                        expected=(LAZY,),
                        received=type(objs)
                    )
                return False
            return True

        res = q(isterm(obj, LAZY) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="islazy",
                    term=objs,
                    expected=(LAZY,),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def iscomposable(self, *funcs, revert=False) -> bool:
        q = self.quantifier

        def _check(f_tuple):
            if len(f_tuple) < 2: return False
            seq = f_tuple[::-1] if revert else f_tuple
            from typed.mods.func import signature
            from typed.mods.typesystem import issub
            for f, g in zip(seq, seq[1:]):
                try:
                    cod = signature(f).cod
                    dom = signature(g).dom
                except Exception:
                    return False

                if cod is None or dom is None: return False

                dom_tuple = tuple(dom) if hasattr(dom, "__iter__") and not isinstance(dom, str) else (dom,)
                if not dom_tuple or not issub(cod, dom_tuple[0]):
                    return False
            return True

        if q is None:
            res = _check(funcs)
            if not res:
                if self.explode:
                    from typed.mods.err import FuncErr
                    raise FuncErr(
                        func="iscomposable",
                        term=funcs,
                        details="Functions are not composable"
                    )
                return False
            return True

        res = q(_check(f_tuple) for f_tuple in funcs)
        if not res:
            if self.explode:
                from typed.mods.err import FuncErr
                raise FuncErr(
                    func="iscomposable",
                    term=funcs,
                    quantifier=q,
                    details="Functions are not composable"
                )
            return False
        return True

    def iscognate(self, strucs, *others, quantifier=None) -> bool:
        from typed.mods.typesystem import iscognate
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = iscognate(strucs, *others, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="iscognate",
                        term=strucs,
                        expected=others,
                        received=strucs,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(iscognate(s, *others) for s in strucs))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="iscognate",
                    term=strucs,
                    expected=others,
                    received=strucs,
                    quantifier=q
                )
            return False
        return True

    def iscongruent(self, strucs, *others, quantifier=None) -> bool:
        from typed.mods.typesystem import iscongruent
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = iscongruent(strucs, *others, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="iscongruent",
                        term=strucs,
                        expected=others,
                        received=strucs,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(iscongruent(s, *others) for s in strucs))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="iscongruent",
                    term=strucs,
                    expected=others,
                    received=strucs,
                    quantifier=q
                )
            return False
        return True

    def ismember(self, entities, *typesystems, quantifier=None) -> bool:
        from typed.mods.typesystem import ismember
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = ismember(entities, *typesystems, quantifier=quantifier)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="ismember",
                        term=entities,
                        expected=self._expected("member", typesystems),
                        received=entities,
                        quantifier=logic_q
                    )
                return False
            return True

        res = q(logic_q(ismember(t, *typesystems) for t in entities))
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="ismember",
                    term=entities,
                    expected=self._expected("member", typesystems),
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def iscallable(self, objs) -> bool:
        q = self.quantifier

        if q is None:
            res = callable(objs)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="iscallable",
                        term=objs,
                        expected=("callable",),
                        received=type(objs)
                    )
                return False
            return True

        res = q(callable(obj) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="iscallable",
                    term=objs,
                    expected=("callable",),
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def isinstance(self, objs, *classes, quantifier=None) -> bool:
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = logic_q(isinstance(objs, cls) for cls in classes)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isinstance",
                        term=objs,
                        expected=classes,
                        quantifier=logic_q,
                        received=type(objs)
                    )
                return False
            return True

        res = q(logic_q(isinstance(obj, cls) for cls in classes) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isinstance",
                    term=objs,
                    expected=classes,
                    quantifier=q,
                    received=type(objs) if not hasattr(objs, '__iter__') or isinstance(objs, str) else tuple(type(obj) for obj in objs)
                )
            return False
        return True

    def isterm(self, objs, *types, quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import isterm
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = isterm(objs, *types, quantifier=quantifier, typesystem=typesystem)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isterm",
                        term=objs,
                        expected=types,
                        quantifier=quantifier
                    )
                return False
            return True

        res = q(logic_q(isterm(obj, t) for t in types) for obj in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isterm",
                    term=objs,
                    expected=types,
                    quantifier=q
                )
            return False
        return True

    def issub(self, entities, *others, quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import issub
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = issub(entities, *others, quantifier=quantifier, typesystem=typesystem)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="issub",
                        term=entities,
                        expected=others,
                        received=entities,
                        quantifier=quantifier
                    )
                return False
            return True

        res = q(logic_q(issub(entity, o, typesystem=typesystem) for o in others) for entity in entities)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="issub",
                    term=entities,
                    expected=others,
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def issup(self, entities, *others, quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import issup
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = issup(entities, *others, quantifier=quantifier, typesystem=typesystem)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="issup",
                        term=entities,
                        expected=others,
                        received=entities,
                        quantifier=quantifier
                    )
                return False
            return True

        res = q(logic_q(issup(entity, o, typesystem=typesystem) for o in others) for entity in entities)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="issup",
                    term=entities,
                    expected=others,
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def issame(self, entities, *others, quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import issame
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = issame(entities, *others, quantifier=quantifier, typesystem=typesystem)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="issame",
                        term=entities,
                        expected=others,
                        received=entities,
                        quantifier=quantifier
                    )
                return False
            return True

        res = q(logic_q(issame(entity, o, typesystem=typesystem) for o in others) for entity in entities)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="issame",
                    term=entities,
                    expected=others,
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def isequiv(self, entities, *others, quantifier=None, typesystem=None) -> bool:
        from typed.mods.typesystem import isequiv
        from typed.mods.resolve import resolve
        logic_q = resolve.logic.quantifier(quantifier)
        q = self.quantifier

        if q is None:
            res = isequiv(entities, *others, quantifier=quantifier, typesystem=typesystem)
            if not res:
                if self.explode:
                    from typed.mods.err import TypeErr
                    raise TypeErr(
                        func="isequiv",
                        term=entities,
                        expected=others,
                        received=entities,
                        quantifier=quantifier
                    )
                return False
            return True

        res = q(logic_q(isequiv(entity, o, typesystem=typesystem) for o in others) for entity in entities)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="isequiv",
                    term=entities,
                    expected=others,
                    received=entities,
                    quantifier=q
                )
            return False
        return True

    def defaults(self, objs) -> bool:
        from typed.mods.func import signature
        from typed.mods.typesystem import isterm
        from typed.mods.err import NotDefined
        q = self.quantifier

        if q is None:
            try:
                sig = signature(objs)
            except Exception:
                return True

            for arg in sig.args:
                if arg.default is not NotDefined and arg.hint is not NotDefined and arg.hint is not None:
                    if not isterm(arg.default, arg.hint):
                        if self.explode:
                            from typed.mods.err import TypeErr
                            raise TypeErr(
                                func="defaults",
                                message=f"Default value for argument '{arg.name}' does not match its type hint",
                                term=arg.default,
                                expected=arg.hint
                            )
                        return False
            return True

        def _check(f):
            try:
                sig = signature(f)
            except Exception:
                return True
            for arg in sig.args:
                if arg.default is not NotDefined and arg.hint is not NotDefined and arg.hint is not None:
                    if not isterm(arg.default, arg.hint):
                        return False
            return True

        res = q(_check(f) for f in objs)
        if not res:
            if self.explode:
                from typed.mods.err import TypeErr
                raise TypeErr(
                    func="defaults",
                    term=objs,
                    quantifier=q,
                    message="Default values do not match type hints in one or more quantified functions"
                )
            return False
        return True

    def satisfy(self, conditions, *args) -> bool:
        from typed.mods.err import NotSatisfied
        q = self.quantifier

        if q is None:
            res = callable(conditions) and conditions(*args) is True
            if not res:
                if self.explode:
                    raise NotSatisfied(
                        condition=conditions,
                        args=args
                    )
                return False
            return True

        res = q(cond(*args) is True for cond in conditions)
        if not res:
            if self.explode:
                raise NotSatisfied(
                    condition=q,
                    args=args
                )
            return False
        return True


def checker(arg=None, name: str = None, quantifier: str = None, count: int = None, explode: bool = True):
    if isinstance(arg, str):
        return Checker(quantifier=arg, explode=explode)
    if callable(arg):
        return staticmethod(Checker(func=arg, name=name, explode=explode))
    return Checker(quantifier=quantifier, count=count, explode=explode)


__require__ = TypedChecker(quantifier=None, explode=True)
__check__ = TypedChecker(quantifier=None, explode=False)

class check:
    some = checker("some", explode=False)
    every = checker("every", explode=False)
    none = checker("none", explode=False)
    only = checker("only", explode=False)

    class hint:
        dom = __check__.hint_dom
        cod = __check__.hint_cod

    class bind:
        dom = __check__.bind_dom
        cod = __check__.bind_cod
        defaults = __check__.defaults

    issafe = __check__.issafe

    isinstance = __check__.isinstance
    iscallable = __check__.iscallable

    isentity = __check__.isentity
    istype = __check__.istype
    ismeta = __check__.ismeta
    isabstract = __check__.isabstract
    isuniverse = __check__.isuniverse

    iscognate = __check__.iscognate
    iscongruent = __check__.iscongruent

    ismember = __check__.ismember
    isterm = __check__.isterm
    issub = __check__.issub
    issup = __check__.issup
    issame = __check__.issame
    isequiv = __check__.isequiv
    satisfy = __check__.satisfy

    isfunc = __check__.isfunc
    iscomposable = __check__.iscomposable
    ishinted = __check__.ishinted
    istyped = __check__.istyped
    islazy = __check__.islazy

class require:
    some = checker("some", explode=True)
    every = checker("every", explode=True)
    none = checker("none", explode=True)
    only = checker("only", explode=True)

    class hint:
        dom = __require__.hint_dom
        cod = __require__.hint_cod

    class bind:
        dom = __require__.bind_dom
        cod = __require__.bind_cod
        defaults = __require__.defaults

    issafe = __require__.issafe

    isinstance = __require__.isinstance
    iscallable = __require__.iscallable

    isentity = __require__.isentity
    istype = __require__.istype
    ismeta = __require__.ismeta
    isabstract = __require__.isabstract
    isuniverse = __require__.isuniverse

    iscognate = __require__.iscognate
    iscongruent = __require__.iscongruent

    ismember = __require__.ismember
    isterm = __require__.isterm
    issub = __require__.issub
    issup = __require__.issup
    issame = __require__.issame
    isequiv = __require__.isequiv
    satisfy = __require__.satisfy

    isfunc = __require__.isfunc
    iscomposable = __require__.iscomposable
    ishinted = __require__.ishinted
    istyped = __require__.istyped
    islazy = __require__.islazy
