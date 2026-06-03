class __SAMENESS__:
    def __init__(self, suffices: tuple[callable]=(), needed: tuple[callable]=(), use_name: bool=True, use_duck: bool=False, use_id: bool=True):
        if suffices:
            from typed.mods.check import check
            for condition in suffices:
                check.isinstance(condition, callable)
        if needed:
            from typed.mods.check import check
            for condition in needed:
                check.isinstance(condition, callable)

        self.suffices = suffices
        self.needed = needed
        self.use_name = use_name
        self.use_duck = use_duck
        self.use_id   = use_id

class __MAGIC__:
    def __init__(
        self,
        __in__: callable=None,
        __eq__: callable=None,
        __le__: callable=None,
        __lt__: callable=None,
        __ge__: callable=None,
        __gt__: callable=None,
        __ne__: callable=None,
        __iter__: callable=None
    ):
        from typed.helper.typesystem import MAGIC
        self.__in__ = __in__ if __in__ is not None else MAGIC.__in__
        self.__eq__ = __eq__ if __eq__ is not None else MAGIC.__eq__
        self.__le__ = __le__ if __le__ is not None else MAGIC.__le__
        self.__lt__ = __lt__ if __lt__ is not None else MAGIC.__lt__
        self.__ge__ = __ge__ if __ge__ is not None else MAGIC.__ge__
        self.__gt__ = __gt__ if __gt__ is not None else MAGIC.__gt__
        self.__ne__ = __ne__ if __ne__ is not None else MAGIC.__ne__
        self.__iter__ = __iter__ if __iter__ is not None else MAGIC.__iter__

class __STATEFUL__:
    def __init__(
        self,
        __issame__: callable=None,
        __isterm__: callable=None,
        __issup__: callable=None,
        __issub__: callable=None,
        __isequiv__: callable=None,
    ):
        from typed.helper.typesystem import STATEFUL
        self.__issame__ = __issame__ if __issame__ is not None else STATEFUL.__issame__
        self.__isterm__ = __isterm__ if __isterm__ is not None else STATEFUL.__isterm__
        self.__issup__ = __issup__ if __issup__ is not None else STATEFUL.__issup__
        self.__issub__ = __issub__ if __issub__ is not None else STATEFUL.__issub__
        self.__isequiv__ = __isequiv__ if __isequiv__ is not None else STATEFUL.__isequiv__

class ___UNIVERSE___(type):
    """
    The universal metaclass of universes
    """
    __name__ = "___UNIVERSE___"
    __display__ = __name__

    def __new__(mcls, name, bases, dct, **kwds):
        cls = super().__new__(mcls, name, bases, dct, **kwds)
        cls.__display__ = name

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            cls.__terms__ = WeakSet()

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            mcls.__terms__ = WeakSet()

        try:
            mcls.__terms__.add(cls)
        except AttributeError:
            pass

        cls_type = getattr(cls, "__type__", None)
        if cls_type is not None:
            for typesystem in getattr(cls, "__typesystems__", set()):
                if cls_type in typesystem:
                    typesystem.add(cls)

        return cls

    def __iter__(cls):
        systems = getattr(cls, "__typesystems__", set())
        for typesystem in systems:
            yield from typesystem.__members__["universe"]

class ___ABSTRACT___(___UNIVERSE___):
    """
    The universal metaclass of abstracts.
    """

    __name__ = "___ABSTRACT___"
    __display__ = __name__

    def __new__(mcls, name, bases, dct, **kwds):
        cls = super().__new__(mcls, name, bases, dct, **kwds)
        cls.__display__ = name

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            cls.__terms__ = WeakSet()

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            mcls.__terms__ = WeakSet()

        try:
            mcls.__terms__.add(cls)
        except AttributeError:
            pass

        cls_type = getattr(cls, "__type__", None)
        if cls_type is not None:
            for typesystem in getattr(cls, "__typesystems__", set()):
                if cls_type in typesystem:
                    typesystem.add(cls)

        return cls

    def __iter__(cls):
        systems = getattr(cls, "__typesystems__", set())
        for typesystem in systems:
            yield from typesystem.__members__["abstract"]

class __UNIVERSE__(type, metaclass=___UNIVERSE___):
    """
    The default type of universes
    """
    __name__ = "__UNIVERSE__"
    __display__ = __name__

    def __new__(
        mcls,
        name="UNIVERSE",
        bases=(type,),
        dct={},
        stateful: __STATEFUL__=None,
        magic: __MAGIC__=None,
        **kwargs
    ):
        if stateful is None:
            for b in bases:
                if hasattr(b, "__stateful__"):
                    stateful = b.__stateful__
                    break
            if stateful is None:
                from typed.mods.check import resolve
                stateful = resolve.typesystem.stateful(stateful)

        if magic is None:
            for b in bases:
                if hasattr(b, "__magic__"):
                    magic = b.__magic__
                    break
            if magic is None:
                from typed.mods.check import resolve
                magic = resolve.typesystem.magic(magic)

        attrs = {
            "is_universe": True,
            "level": -1,
            "__stateful__": stateful,
            "__magic__": magic,
            "__isterm__": stateful.__isterm__,
            "__issub__": stateful.__issub__,
            "__issup__": stateful.__issup__,
            "__issame__": stateful.__issame__,
            "__contains__": magic.__in__,
            "__eq__": magic.__eq__,
            "__le__": magic.__le__,
            "__lt__": magic.__lt__,
            "__ge__": magic.__ge__,
            "__gt__": magic.__gt__,
            "__ne__": magic.__ne__,
            "__iter__": magic.__iter__,
            "__hash__": type.__hash__,
            "__display__": name
        }
        attrs.update(dct)
        attrs.update(kwargs)

        cls = super().__new__(mcls, name, bases, attrs)

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            cls.__terms__ = WeakSet()

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            mcls.__terms__ = WeakSet()

        try:
            mcls.__terms__.add(cls)
        except AttributeError:
            pass

        cls_type = getattr(cls, "__type__", None)
        if cls_type is not None:
            for typesystem in getattr(cls, "__typesystems__", set()):
                if cls_type in typesystem:
                    typesystem.add(cls)

        return cls

    def __init__(cls, name="UNIVERSE", bases=(type,), dct=None, **kwargs):
        super().__init__(name, bases, dct if dct is not None else {})

    def __iter__(typ):
        from typed.helper.typesystem import MAGIC
        return MAGIC.__iter__(typ)

    def __call__(typ, *args, typesystem=None, **kwargs):
        if len(args) == 3 and isinstance(args[0], str) and isinstance(args[1], tuple) and isinstance(args[2], dict):
            return super().__call__(*args, **kwargs)

        from typed.mods.check import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        from typed.mods.err import NotDefined
        if len(args) == 1 and isinstance(args[0], int):
            n = args[0]
            if n < 0:
                return typesystem.__universe__

            typesystem.enrich(level=n+1)
            UNI = typesystem.__members__["universe"][n]
            UNI.__typesystems__ = [typesystem]
            UNI.__type__ = typesystem.__members__["universe"][n+1]
            UNI.__builtin__ = NotDefined
            UNI.__null__ = NotDefined
            return UNI

        if len(args) == 0 and typesystem is not NotDefined:
            return typesystem.__universe__
        return super().__call__(*args, **kwargs)


class __ABSTRACT__(__UNIVERSE__, metaclass=___ABSTRACT___):
    """
    The default type of abstracts
    """
    __name__ = "__ABSTRACT__"
    __display__ = __name__

    def __new__(
        mcls,
        name="ABSTRACT",
        bases=(type,),
        dct={},
        stateful: __STATEFUL__=None,
        magic: __MAGIC__=None,
        **kwargs
    ):
        if stateful is None:
            for b in bases:
                if hasattr(b, "__stateful__"):
                    stateful = b.__stateful__
                    break
            if stateful is None:
                from typed.mods.check import resolve
                stateful = resolve.typesystem.stateful(stateful)

        if magic is None:
            for b in bases:
                if hasattr(b, "__magic__"):
                    magic = b.__magic__
                    break
            if magic is None:
                from typed.mods.check import resolve
                magic = resolve.typesystem.magic(magic)

        attrs = {
            "is_abstract": True,
            "level": -1,
            "__stateful__": stateful,
            "__magic__": magic,
            "__isterm__": stateful.__isterm__,
            "__issub__": stateful.__issub__,
            "__issup__": stateful.__issup__,
            "__issame__": stateful.__issame__,
            "__contains__": magic.__in__,
            "__eq__": magic.__eq__,
            "__le__": magic.__le__,
            "__lt__": magic.__lt__,
            "__ge__": magic.__ge__,
            "__gt__": magic.__gt__,
            "__ne__": magic.__ne__,
            "__iter__": magic.__iter__,
            "__hash__": type.__hash__,
            "__display__": name
        }
        attrs.update(dct)
        attrs.update(kwargs)

        cls = super().__new__(mcls, name=name, bases=bases, dct=attrs, stateful=stateful, magic=magic)

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            cls.__terms__ = WeakSet()

        if "__terms__" not in mcls.__dict__:
            from weakref import WeakSet
            mcls.__terms__ = WeakSet()

        try:
            mcls.__terms__.add(cls)
        except AttributeError:
            pass

        cls_type = getattr(cls, "__type__", None)
        if cls_type is not None:
            for typesystem in getattr(cls, "__typesystems__", set()):
                if cls_type in typesystem:
                    typesystem.add(cls)

        return cls

    def __init__(cls, name="ABSTRACT", bases=(type,), dct=None, **kwargs):
        super().__init__(name=name, bases=bases, dct=dct if dct is not None else {})

    def __iter__(typ):
        from typed.helper.typesystem import MAGIC
        return MAGIC.__iter__(typ)

    def __call__(typ, *args, typesystem=None, **kwargs):
        if len(args) == 3 and isinstance(args[0], str) and isinstance(args[1], tuple) and isinstance(args[2], dict):
            return super().__call__(*args, **kwargs)

        from typed.mods.check import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if len(args) == 1 and isinstance(args[0], int):
            n = args[0]
            if n < 0:
                return typesystem.__abstract__

            from typed.mods.err import NotDefined
            typesystem.enrich(level=n+1)
            ABS = typesystem.__members__["abstract"][n]
            ABS.__typesystems__ = [typesystem]
            ABS.__type__ = typesystem.__members__["universe"][n+1]
            ABS.__builtin__ = NotDefined
            ABS.__null__ = NotDefined
            return ABS

        if len(args) == 0 and typesystem is not NotDefined:
            return typesystem.__abstract__

        return super().__call__(*args, **kwargs)

class __TYPESYSTEM__:
    def __init__(
        self,
        name: str="TYPESYSTEM",
        universe: __UNIVERSE__=None,
        abstract: __ABSTRACT__=None,
        stateful: __STATEFUL__=None,
        magic: __MAGIC__=None,
        quantifiers: set=None,
        kinds: set=None,
        typemap: dict=None
    ):
        from typed.mods.check import resolve
        universe = resolve.typesystem.universe(universe)
        abstract = resolve.typesystem.abstract(abstract)
        stateful = resolve.typesystem.stateful(stateful)
        magic = resolve.typesystem.magic(magic)
        quantifiers = resolve.typesystem.quantifiers(quantifiers)
        kinds = resolve.typesystem.kinds(kinds)
        typemap  = resolve.typesystem.typemap(typemap)

        self.__name__ = name
        self.__display__ = name
        self.__stateful__ = stateful
        self.__magic__ = magic
        self.__universe__ = universe
        self.__universe__.__typesystems__ = [self]
        self.__kinds__ = kinds
        self.__typemap__ = typemap
        self.__abstract__ = abstract
        self.__abstract__.__typesystems__ = [self]

        self.is_typesystem = True

        self.__members__ = {}
        for kind in self.__kinds__:
            self.__members__[kind] = set() if kind not in ["universe", "abstract"] else {}

        self.__members__["universe"][-1] = self.__universe__
        self.__members__["abstract"][-1] = self.__abstract__
        self.__members__["quantifier"]=quantifiers

        def __new__(univ, typ, bases, namespace, **kwds):
            cls = type.__new__(univ, typ, bases, namespace, **kwds)

            if "__terms__" not in cls.__dict__:
                from weakref import WeakSet
                cls.__terms__ = WeakSet()

            if "__terms__" not in univ.__dict__:
                from weakref import WeakSet
                univ.__terms__ = WeakSet()

            try:
                univ.__terms__.add(cls)
            except AttributeError:
                pass

            cls_type = getattr(cls, "__type__", None)
            if cls_type is not None:
                for typesystem in getattr(cls, "__typesystems__", []):
                    if cls_type in typesystem:
                        typesystem.add(cls)

            return cls

        def __enricher__():
            level = 0
            prev = None
            prev_abs = None

            from typed.helper.typesystem import _abstract_isterm, _abstract_issub, _universe_issub
            while True:
                univ_name = f"UNIVERSE({level})"
                abs_name  = f"ABSTRACT({level})"

                univ_stateful = __STATEFUL__(
                    __isterm__=stateful.__isterm__, 
                    __issub__=_universe_issub,
                    __issup__=stateful.__issup__,
                    __issame__=stateful.__issame__,
                    __isequiv__=stateful.__isequiv__,
                )

                univ_cls = type(self.__universe__)(
                    name=univ_name,
                    bases=(type,),
                    stateful=univ_stateful,
                    magic=magic,
                    __new__=__new__,
                    level=level,
                    __display__=univ_name
                )

                abs_stateful = __STATEFUL__(
                    __isterm__=_abstract_isterm(univ_cls, stateful=stateful, typesystem=self),
                    __issub__=_abstract_issub,
                    __issup__=stateful.__issup__,
                    __issame__=stateful.__issame__,
                    __isequiv__=stateful.__isequiv__
                )

                abs_cls = type(self.__abstract__)(
                    name=abs_name,
                    bases=(univ_cls,),
                    stateful=abs_stateful,
                    magic=magic,
                    level=level,
                    __display__=abs_name
                )

                if hasattr(self.__universe__, "__terms__"):
                    self.__universe__.__terms__.add(univ_cls)
                if hasattr(self.__abstract__, "__terms__"):
                    self.__abstract__.__terms__.add(abs_cls)

                if prev is not None:
                    prev.__class__ = univ_cls
                if prev_abs is not None:
                    prev_abs.__class__ = univ_cls

                prev = univ_cls
                prev_abs = abs_cls

                yield univ_cls, abs_cls
                level += 1

        self.__enricher__ = __enricher__()

    def enrich(self, level):
        while len(self.__members__["universe"]) <= level + 1:
            u, a = next(self.__enricher__)
            u_level = getattr(u, "level", -1)

            if u_level not in self.__members__["universe"]:
                self.__members__["universe"][u_level] = u
            if u_level not in self.__members__["abstract"]:
                self.__members__["abstract"][u_level] = a

    def add(self, *T):
        for t in T:
            for kind in self.__kinds__:
                attr = f"is_{kind}"
                is_k = False
                if hasattr(t, '__dict__') and attr in t.__dict__:
                    is_k = t.__dict__[attr]
                elif not isinstance(t, type) and hasattr(type(t), '__dict__') and attr in type(t).__dict__:
                    is_k = type(t).__dict__[attr]

                if is_k:
                    if kind in ["universe", "abstract"]:
                        self.__members__[kind][getattr(t, "level", -1)] = t
                    else:
                        self.__members__[kind].add(t)

    def rm(self, *T):
        for t in T:
            for kind in self.__kinds__:
                attr = f"is_{kind}"
                is_k = False
                if hasattr(t, '__dict__') and attr in t.__dict__:
                    is_k = t.__dict__[attr]
                elif not isinstance(t, type) and hasattr(type(t), '__dict__') and attr in type(t).__dict__:
                    is_k = type(t).__dict__[attr]

                if is_k:
                    if kind in ["universe", "abstract"]:
                        self.__members__[kind].pop(getattr(t, "level", -1), None)
                    else:
                        self.__members__[kind].discard(t)

    def prune(self):
        for kind in self.__kinds__:
            self.__members__[kind].clear()

    def __contains__(self, T):
        for kind in self.__kinds__:
            if kind in ["universe", "abstract"]:
                for v in self.__members__[kind].values():
                    if T is v:
                        return True
            else:
                for v in self.__members__[kind]:
                    if T is v:
                        return True
        return False

    def __iter__(self):
        for kind in self.__kinds__:
            if kind in ["universe", "abstract"]:
                yield from self.__members__[kind].values()
            else:
                yield from self.__members__[kind]

    def typemap(self, type):
        return typemap(type, typesystem=self)

    def typeof(self, term, level=1):
        return typeof(term, level=level, typesystem=self)

    def trackof(self, type):
        return trackof(type, typesystem=self)

    def nameof(self, term):
        return nameof(term, typesystem=self)

    def kindof(self, term):
        return kindof(term, typesystem=self)

    def issub(self, type, *others, quantifier=None):
        return issub(type, *others, quantifier=quantifier, typesystem=self)

    def issup(self, type, *others, quantifer=None):
        return issup(type, *others, quantifier=quantifer, typesystem=self)

    def isterm(self, term, *types, quantifier=None):
        return isterm(term, *types, quantifier=None, typesystem=self)

    def ismember(self, entity):
        return ismember(entity, self)

    def issame(self, type, *others, quantifier=None):
        return issame(type, *others, quantifier=None, typesystem=self)

    def isequiv(self, type, *others, quantifier=None):
        return isequiv(type, *others, quantifier=None, typesystem=self)

def typemap(type, typesystem: __TYPESYSTEM__=None):
    from builtins import type as __type__
    from typed.mods.check import resolve
    typesystem = resolve.typesystem.entity(typesystem)
    try:
        for univ in typesystem.__members__["universe"].values():
            if __type__(type) is univ:
                return type
    except TypeError:
        pass

    try:
        for k, v in typesystem.__typemap__.items():
            if type is k:
                return v
    except:
        pass

    from typed.mods.err import NotDefined
    return NotDefined

def typeof(entity: object, level: int=1, typesystem: __TYPESYSTEM__=None):
    from typed.mods.check import check, resolve
    typesystem = resolve.typesystem.entity(typesystem)
    check.isinstance(level, int)

    if level <= 0:
        from typed.mods.err import NotDefined
        return NotDefined

    base = typemap(type(entity), typesystem=typesystem)
    if level == 1:
        return base

    for i in range(2, level+1):
        base = typeof(base)
    return base


def kindof(entity, typesystem: __TYPESYSTEM__=None):
    from typed.mods.check import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    kind = getattr(entity, "__kind__", None)
    if kind in ["universe", "abstract"]:
        if entity in typesystem.__members__[kind].values():
            return kind
    else:
        if kind in typesystem.__kinds__:
            if entity in typesystem.__members__[kind]:
                return kind

    from typed.mods.err import NotDefined
    return NotDefined

def nameof(entity: object, typesystem: __TYPESYSTEM__=None):
    """
    The 'nameof' polymorphism.
    """
    from typed.mods.check import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    from typed.mods.err import NotDefined
    from typed.mods.poly import display
    d = display(entity)
    if d is not NotDefined:
        return d

    type = typemap(entity, typesystem=typesystem)

    return getattr(term, '__name__', NotDefined)

def names(*terms: tuple[object], typesystem=None) -> str:
    return ', '.join(nameof(t) for t in terms)

def trackof(type: type, typesystem: __TYPESYSTEM__=None) -> type:
    from typed.mods.check import resolve
    typesystem = resolve.typesystem.entity(typesystem)

    from typed.mods.err import NotDefined
    from typed.mods.poly import builtin

    if builtin(type) is not NotDefined:
        name = f"Track({nameof(type)})"
        attrs = {
            "__display__": name,
            "is_track": True,
            "__builtin__": type
        }
        return type.__call__(name, (type,), attrs)

    return NotDefined

def ismember(type: type, *typesystems: tuple[__TYPESYSTEM__], quantifier=None) -> bool:
    from builtins import type as __type__
    from typed.mods.check import check, resolve

    check.isinstance(type, __type__)
    quantifier = resolve.logic.quantifier(quantifier)
    typesystems = set([resolve.typesystem.entity(t) for t in typesystems])

    return quantifier(type in typesystem for typesystem in typesystems)

def istype(type: type) -> bool:
    from builtins import type as __type__
    from typed.mods.check import check
    check.isinstance(type, __type__)
    return set(getattr(type, "__typesystems__", [])) != set()

def iscognate(type, *others: tuple[type], quantifier=None) -> bool:
    from builtins import type as __type__
    from typed.mods.check import check, resolve

    check.istype(type)
    check.every.istype(others)
    quantifier = resolve.logic.quantifier(quantifier)

    return quantifier(
        not set(getattr(type, "__typesystems__", [])).isdisjoint(getattr(other, "__typesystems__", []))
        for other in others
    )

def issame(type: type, *others: tuple[type], quantifier=None, typesystem: __TYPESYSTEM__=None) -> bool:
    from typed.mods.check import check, resolve
    typesystem = resolve.typesystem.entity(typesystem)
    quantifier = resolve.logic.quantifier(quantifier)
    __issame__ = typesystem.__stateful__.__issame__

    from typed.mods.logic import Quantifier
    check.isinstance(obj=quantifier, cls=Quantifier)

    return quantifier(__issame__(other, type, typesystem=typesystem) for other in others)

def issup(type: type, *others: tuple[type], quantifier=None, typesystem: __TYPESYSTEM__=None) -> bool:
    from typed.mods.check import check, resolve
    typesystem = resolve.typesystem.entity(typesystem)
    quantifier = resolve.logic.quantifier(quantifier)
    __issup__ = typesystem.__stateful__.__issup__

    from typed.mods.logic import Quantifier
    check.isinstance(obj=quantifier, cls=Quantifier)
    return quantifier(__issup__(other, type, typesystem=typesystem) for other in others)

def issub(type: type, *others: tuple[type], quantifier=None, typesystem: __TYPESYSTEM__=None) -> bool:
    from typed.mods.check import check, resolve
    typesystem = resolve.typesystem.entity(typesystem)
    quantifier = resolve.logic.quantifier(quantifier)
    __issub__ = typesystem.__stateful__.__issub__

    from typed.mods.logic import Quantifier
    check.isinstance(obj=quantifier, cls=Quantifier)
    return quantifier(__issub__(other, type, typesystem=typesystem) for other in others)

def isterm(term: object, *types: tuple[type], quantifier=None, typesystem: __TYPESYSTEM__=None) -> bool:
    from typed.mods.check import check, resolve
    typesystem = resolve.typesystem.entity(typesystem)
    quantifier = resolve.logic.quantifier(quantifier)
    __isterm__ = typesystem.__stateful__.__isterm__

    from typed.mods.logic import Quantifier
    check.isinstance(obj=quantifier, cls=Quantifier)
    return quantifier(__isterm__(type, term, typesystem=typesystem) for type in types)

def isequiv(type: type, *others: tuple[type],  quantifier=None, typesystem: __TYPESYSTEM__=None) -> bool:
    from typed.mods.check import check, resolve
    typesystem = resolve.typesystem.entity(typesystem)
    quantifier = resolve.logic.quantifier(quantifier)
    __isequiv__ = typesystem.__stateful__.__isequiv__

    from typed.mods.logic import Quantifier
    check.isinstance(obj=quantifier, cls=Quantifier)
    return quantifier(__isequiv__(other, type, typesystem=typesystem) for other in others)

def term(value, type: type=None, typesystem:__TYPESYSTEM__=None):
    from typed.mods.check import resolve
    typesystem = resolve.typesystem.entity(typesystem)
    if type is None:
        type = typeof(value, typesystem=typesystem)

    from weakref import WeakSet
    from typed.mods.err import NotDefined, TypeErr

    if type is NotDefined:
        raise NotDefined(
            message="Type not defined",
            type=nameof(type, typesystem),
            typesystem=nameof(type, typesystem)
        )

    if not isterm(value, type, typesystem=typesystem):
        raise TypeErr(
            message="Type mismatch in term declaration",
            term=value,
            expected=type,
            received=typeof(value)
        )

    from typed.mods.poly import builtin
    tracked = trackof(builtin(type), typesystem=typesystem)

    if tracked is not NotDefined:
        value = tracked(value)

    if not hasattr(type, "__terms__"):
        type.__terms__ = WeakSet()

    type.__terms__.add(value)

    return value

class new:
    @staticmethod
    def conf(typesystem=None, logic=None, err=None):
        from typed.mods.conf import Conf
        return Conf(
            logic=logic,
            typesystem=typesystem,
            err=err
        )

    @staticmethod
    def sameness(
        suffices: tuple[callable]=(),
        needed: tuple[callable]=(),
        use_name: bool=True,
        use_duck: bool=False,
        use_id: bool=True
    ):
        return __SAMENESS__(
            suffices=suffices,
            needed=needed,
            use_name=use_name,
            use_duck=use_duck,
            use_id=use_id
        )

    @staticmethod
    def magic(
        __in__: callable=None,
        __eq__: callable=None,
        __le__: callable=None,
        __lt__: callable=None,
        __ge__: callable=None,
        __gt__: callable=None,
        __ne__: callable=None,
        __iter__: callable=None
    ):
        return __MAGIC__(
            __in__=__in__,
            __eq__=__eq__,
            __le__=__le__,
            __lt__=__lt__,
            __ge__=__ge__,
            __gt__=__gt__,
            __ne__=__ne__,
            __iter__=__iter__
        )

    @staticmethod
    def stateful(
        __isterm__: callable=None,
        __issub__: callable=None,
        __issup__: callable=None,
        __issame__: callable=None,
        __isequiv__: callable=None,
    ):
        return __STATEFUL__(
            __isterm__=__isterm__,
            __issub__=__issub__,
            __issup__=__issup__,
            __issame__=__issame__,
            __isequiv__=__isequiv__,
        )

    @staticmethod
    def reducer(func):
        from typed.mods.logic import Reducer
        return Reducer(func=func)

    @staticmethod
    def evaluator(*args, **kwargs):
        from typed.mods.logic import __EVALUATOR__
        return __EVALUATOR__(*args, **kwargs)

    @staticmethod
    def quantifier(reducer=None, evaluator=None, order=None, count=None, **kwargs):
        from typed.mods.logic import Quantifier
        return Quantifier(reducer=reducer, evaluator=evaluator, order=order, count=count)

    @staticmethod
    def universe(*args, **kwargs):
        if not args:
            args = ("UNIVERSE", (type,), {})
        return __UNIVERSE__(*args, **kwargs)

    @staticmethod
    def abstract(*args, **kwargs):
        if not args:
            args = ("ABSTRACT", (type,), {})
        return __ABSTRACT__(*args, **kwargs)

    @staticmethod
    def typesystem(*args, **kwargs):
        return __TYPESYSTEM__(*args, **kwargs)

    @staticmethod
    def meta(name: str, sups: tuple[type]=(), attrs: dict={}, typesystem: __TYPESYSTEM__=None):
        if typesystem is None:
            from typed.mods.init import conf
            typesystem = conf.typesystem.entity

        for sup in sups:
            if sup not in typesystem.__members__["meta"]:
                raise TypeError(f"sup {sup} not in typesystem.__members__['meta']")

        typesystem.enrich(0)
        base_meta = typesystem.__members__["abstract"][0]

        attrs["__display__"] = name
        attrs["is_meta"] = True
        attrs["__typesystems__"] = [typesystem]

        bases = tuple(sups) if sups else (base_meta,)

        M = base_meta(name, bases, attrs)
        typesystem.add(M)
        return M

    @staticmethod
    def type(name: str, meta: type, sups: tuple[type]=(), attrs: dict={}, typesystem: __TYPESYSTEM__=None):
        if typesystem is None:
            from typed.mods.init import conf
            typesystem = conf.typesystem.entity

        if meta not in typesystem.__members__["meta"]:
            raise TypeError(f"meta {meta} not in typesystem.__members__['meta']")

        for s in sups:
            if s not in typesystem.__members__["type"]:
                raise TypeError(f"sup {s} not in typesystem.__members__['type']")
            if type(s, typesystem) not in typesystem.__members__["meta"]:
                raise TypeError(f"type(s) not in typesystem.__members__['meta']")

        attrs["__display__"] = name
        attrs["is_type"] = True
        attrs["__typesystems__"] = [typesystem]

        T = meta(name, tuple(sups), attrs)
        typesystem.add(T)
        return T

    @staticmethod
    def err(name):
        from typed.mods.err import Err
        return type(name, (Err,), {"__name__": name, "__display__": name})
