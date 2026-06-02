class __SAMENESS__:
    def __init__(self, *conditions: tuple[callable], use_name: bool=True, use_duck: bool=False, use_id: bool=True):
        if conditions:
            from typed.mods.check import check
            for condition in conditions:
                check.isinstance(condition, callable)

        self.conditions = conditions
        self.use_name = use_name
        self.use_duck = use_duck
        self.use_id   = use_id

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
        dct=None,
        __isterm__=None,
        __issub__=None,
        __in__=None,
        __eq__=None,
        __le__=None,
        __lt__=None,
        __ge__=None,
        __gt__=None,
        __ne__=None,
        __iter__=None,
        **kwargs
    ):
        if dct is None:
            dct = {}

        if None in (__isterm__, __issub__):
            from typed.helper.typesystem import STATEFUL

        if None in (__in__, __eq__, __le__, __lt__, __ge__, __gt__, __ne__, __iter__):
            from typed.helper.typesystem import MAGIC

        __isterm__ = __isterm__ if __isterm__ is not None else STATEFUL.__isterm__
        __issub__ = __issub__ if __issub__ is not None else STATEFUL.__issub__
        __in__ = __in__ if __in__ is not None else MAGIC.__in__
        __eq__ = __eq__ if __eq__ is not None else MAGIC.__eq__
        __le__ = __le__ if __le__ is not None else MAGIC.__le__
        __lt__ = __lt__ if __lt__ is not None else MAGIC.__lt__
        __ge__ = __ge__ if __ge__ is not None else MAGIC.__ge__
        __gt__ = __gt__ if __gt__ is not None else MAGIC.__gt__
        __ne__ = __ne__ if __ne__ is not None else MAGIC.__ne__
        __iter__ = __iter__ if __iter__ is not None else MAGIC.__iter__

        attrs = {
            "is_universe": True,
            "level": -1,
            "__isterm__": __isterm__,
            "__issub__": __issub__,
            "__contains__": __in__,
            "__eq__": __eq__,
            "__le__": __le__,
            "__lt__": __lt__,
            "__ge__": __ge__,
            "__gt__": __gt__,
            "__ne__": __ne__,
            "__iter__": __iter__,
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
        typesystem = resolve.typesystem(typesystem)

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
        dct=None,
        __isterm__=None,
        __issub__=None,
        __in__=None,
        __eq__=None,
        __le__=None,
        __lt__=None,
        __ge__=None,
        __gt__=None,
        __ne__=None,
        __iter__=None,
        **kwargs
    ):
        if dct is None:
            dct = {}

        if None in (__isterm__, __issub__):
            from typed.helper.typesystem import STATEFUL

        if None in (__in__, __eq__, __le__, __lt__, __ge__, __gt__, __ne__, __iter__):
            from typed.helper.typesystem import MAGIC

        __isterm__ = __isterm__ if __isterm__ is not None else STATEFUL.__isterm__
        __issub__ = __issub__ if __issub__ is not None else STATEFUL.__issub__
        __in__ = __in__ if __in__ is not None else MAGIC.__in__
        __eq__ = __eq__ if __eq__ is not None else MAGIC.__eq__
        __le__ = __le__ if __le__ is not None else MAGIC.__le__
        __lt__ = __lt__ if __lt__ is not None else MAGIC.__lt__
        __ge__ = __ge__ if __ge__ is not None else MAGIC.__ge__
        __gt__ = __gt__ if __gt__ is not None else MAGIC.__gt__
        __ne__ = __ne__ if __ne__ is not None else MAGIC.__ne__
        __iter__ = __iter__ if __iter__ is not None else MAGIC.__iter__

        attrs = {
            "is_abstract": True,
            "level": -1,
            "__isterm__": __isterm__,
            "__issub__": __issub__,
            "__contains__": __in__,
            "__eq__": __eq__,
            "__le__": __le__,
            "__lt__": __lt__,
            "__ge__": __ge__,
            "__gt__": __gt__,
            "__ne__": __ne__,
            "__iter__": __iter__,
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

    def __init__(cls, name="ABSTRACT", bases=(type,), dct=None, **kwargs):
        super().__init__(name, bases, dct if dct is not None else {})

    def __iter__(typ):
        from typed.helper.typesystem import MAGIC
        return MAGIC.__iter__(typ)

    def __call__(typ, *args, typesystem=None, **kwargs):
        if len(args) == 3 and isinstance(args[0], str) and isinstance(args[1], tuple) and isinstance(args[2], dict):
            return super().__call__(*args, **kwargs)

        from typed.mods.check import resolve
        typesystem = resolve.typesystem(typesystem)

        if len(args) == 1 and isinstance(args[0], int):
            n = args[0]
            if n < 0:
                return typesystem.abstract

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
        quantifiers: set=None,
        kinds: set=None,
        typemap: dict=None,
        sameness: __SAMENESS__=None,
        is_strict: bool=None,
        __isterm__: callable=None,
        __issub__: callable=None,
        __in__: callable=None,
        __eq__: callable=None,
        __le__: callable=None,
        __lt__: callable=None,
        __ge__: callable=None,
        __gt__: callable=None,
        __ne__: callable=None
    ):
        from typed.mods.check import resolve

        universe = resolve.typesystem.universe(universe)
        abstract = resolve.typesystem.abstract(abstract)
        quantifiers = resolve.typesystem.quantifiers(quantifiers)
        typemap  = resolve.typesystem.typemap(typemap)
        sameness = resolve.typesystem.sameness(sameness)
        is_strict = resolve.typesystem.is_strict(is_strict)
        kinds = resolve.typesystem.kinds(kinds)

        self.__name__ = name
        self.__display__ = name
        self.__universe__ = universe
        self.__universe__.__typesystems__ = [self]
        self.__kinds__ = kinds
        self.__typemap__ = typemap
        self.__abstract__ = abstract
        self.__abstract__.__typesystems__ = [self]

        self.is_typesystem = True
        self.is_strict = is_strict

        if None in (__isterm__, __issub__):
            from typed.helper.typesystem import STATEFUL

        if None in (__in__, __eq__, __le__, __lt__, __ge__, __gt__, __ne__):
            from typed.helper.typesystem import MAGIC

        __isterm__ = __isterm__ if __isterm__ is not None else STATEFUL.__isterm__
        __issub__ = __issub__ if __issub__ is not None else STATEFUL.__issub__
        __in__ = __in__ if __in__ is not None else MAGIC.__in__
        __eq__ = __eq__ if __eq__ is not None else MAGIC.__eq__
        __le__ = __le__ if __le__ is not None else MAGIC.__le__
        __lt__ = __lt__ if __lt__ is not None else MAGIC.__lt__
        __ge__ = __ge__ if __ge__ is not None else MAGIC.__ge__
        __gt__ = __gt__ if __gt__ is not None else MAGIC.__gt__
        __ne__ = __ne__ if __ne__ is not None else MAGIC.__ne__

        self.__members__ = {}
        for kind in self.__kinds__:
            self.__members__[kind] = set() if kind not in ["universe", "abstract"] else {}

        self.__members__["universe"][-1] = self.__universe__
        self.__members__["abstract"][-1] = self.__abstract__
        self.__members__["quantifier"]=quantifiers

        def root_term(typ, trm):
            return "is_abstract" in getattr(trm, "__dict__", {})

        def root_sub(typ, other):
            return "is_abstract" in getattr(other, "__dict__", {})

        def sub_fn(univ, other):
            if "is_universe" in getattr(other, "__dict__", {}) and "is_universe" in getattr(univ, "__dict__", {}):
                return getattr(other, "level", -1) <= getattr(univ, "level", -1)
            return __issub__(univ, other)

        def abs_sub(abs, other):
            if "is_abstract" in getattr(other, "__dict__", {}) and "is_abstract" in getattr(abs, "__dict__", {}):
                return getattr(other, "level", -1) <= getattr(abs, "level", -1)
            return __issub__(abs, other)

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

            while True:
                univ_name = f"UNIVERSE({level})"
                abs_name  = f"ABSTRACT({level})"

                univ_cls = type(self.__universe__)(
                    name=univ_name,
                    bases=(type,),
                    __isterm__=__isterm__,
                    __issub__=sub_fn,
                    __in__=__in__,
                    __eq__=__eq__,
                    __le__=__le__,
                    __lt__=__lt__,
                    __ge__=__ge__,
                    __gt__=__gt__,
                    __ne__=__ne__,
                    __new__=__new__,
                    level=level,
                    __display__=univ_name
                )

                def make_abs_term(u_cls):
                    def abs_term(typ, trm):
                        return __issub__(trm, u_cls)
                    return abs_term

                abs_cls = type(self.__abstract__)(
                    name=abs_name,
                    bases=(univ_cls,),
                    __isterm__=make_abs_term(univ_cls),
                    __issub__=abs_sub,
                    __in__=__in__,
                    __eq__=__eq__,
                    __le__=__le__,
                    __lt__=__lt__,
                    __ge__=__ge__,
                    __gt__=__gt__,
                    __ne__=__ne__,
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
                if T in self.__members__[kind].values():
                    return True
            else:
                if T in self.__members__[kind]:
                    return True
        return False

    def __iter__(self):
        for kind in self.__kinds__:
            if kind in ["universe", "abstract"]:
                yield from self.__members__[kind].values()
            else:
                yield from self.__members__[kind]

def typemap(typ, typesystem: __TYPESYSTEM__=None):
    if typesystem is None:
        from typed.mods.init import conf
        typesystem = conf.typesystem.entity
    try:
        if type(typ) in typesystem.__members__["universe"].values():
            return typ
    except TypeError:
        pass

    try:
        if typ in typesystem.typemap:
            return typesystem.typemap[typ]
    except:
        from typed.mods.err import NotDefined
        return NotDefined

def typeof(obj: object, level: int=1, typesystem: __TYPESYSTEM__=None):
    if typesystem is None:
        from typed.mods.init import conf
        typesystem = conf.typesystem.entity
    from typed.mods.check import check
    check.isinstance(level, int)

    if level == 1:
        return typemap(type(obj), typesystem)

def kindof(x, typesystem: __TYPESYSTEM__=None):
    if typesystem is None:
        from typed.mods.init import conf
        typesystem = conf.typesystem.entity

    for kind in typesystem.__kinds__:
        if kind in ["universe", "abstract"]:
            if x in typesystem.__members__[kind].values():
                return kind
        else:
            if x in typesystem.__members__[kind]:
                return kind

    from typed.mods.err import NotDefined
    return NotDefined

def nameof(term: object, typesystem: __TYPESYSTEM__=None):
    """
    The 'nameof' polymorphism.
    """
    if typesystem is None:
        from typed.mods.init import conf
        typesystem = conf.typesystem.entity

    from typed.mods.err import NotDefined
    from typed.mods.poly import display
    d = display(term)
    if d is not NotDefined:
        return d

    type = typemap(term)

    if type is not NotDefined:
        d = display(type)
        if d is not NotDefined:
            return d

    from typed.mods.err import Anonymous
    return getattr(term, '__name__', Anonymous.__name__)

def names(*terms: tuple[object], typesystem=None) -> str:
    return ', '.join(nameof(t) for t in terms)

def trackof(type: type, typesystem: __TYPESYSTEM__=None) -> type:
    if typesystem is None:
        from typed.mods.init import conf
        typesystem  = conf.typesystem.entity

    from typed.mods.err import NotDefined
    from typed.mods.poly import builtin

    if builtin(type) is not NotDefined:
        name = f"Track({nameof(type)})"
        attrs = {
            "__display__": name,
            "is_trackof": True,
            "__builtin__": type
        }
        return type.__call__(name, (type,), attrs)

    return NotDefined

def term(value, type=None, typesystem:__TYPESYSTEM__=None):
    if typesystem is None:
        from typed.mods.init import conf
        typesystem  = conf.typesystem.entity

    from weakref import WeakSet
    from typed.mods.err import NotDefined, TypeErr

    if typesystem is None:
        from typed.mods.init import TYPESYSTEM
        typesystem = TYPESYSTEM

    if type is None:
        type = typeof(value)

    if type is NotDefined:
        raise NotDefined(
            message="Type not defined",
            type=nameof(type, typesystem),
            typesystem=nameof(type, typesystem)
        )

    if not isterm(value, type):
        raise TypeErr(
            message="Type mismatch in term declaration",
            term=value,
            expected=type,
            received=typeof(value)
        )

    from typed.mods.poly import builtin
    tracked = trackof(builtin(type))

    if tracked is not NotDefined:
        value = tracked(value)

    if not hasattr(type, "__terms__"):
        type.__terms__ = WeakSet()

    type.__terms__.add(value)

    return value

def ismember(type: type, *typesystems: tuple[__TYPESYSTEM__], quantifier=None) -> bool:
    from builtins import type as __type__
    from typed.mods.check import check, resolve

    check.isinstance(type, __type__)
    quantifier = resolve.quantifier(quantifier)
    typesystems = [resolve.typesystem(t) for t in typesystems]

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
    quantifier = resolve.quantifier(quantifier)

    quantifier(
        not set(getattr(type, "__typesystems__", [])).isdisjoint(getattr(other, "__typesystems__", []))
        for other in others
    )

def issame(typ, *others, quantifier=None, sameness: __SAMENESS__=None) -> bool:

    if sameness is None:
        from typed.mods.init import conf
        sameness = conf.typesystem.sameness

    from typed.mods.check import check
    checkisinstance(sameness, __SAMENESS__)
    check.iscognate(typ, other)
    if sameness.by_name:

def extends(typ, *others, quantifier=None, sameness: __SAMENESS__=None):
    return any(typ is T for T in other.__mro__)

def issup(type: type, *others: tuple[type], quantifier=None) -> bool:
    if quantifier is None:
        from typed.mods.init import some
        quantifier = some

    from typed.mods.logic import Quantifier
    from typed.mods.check import check
    check.isinstance(obj=quantifier, cls=Quantifier)

    from typed.helper.typesystem import STATEFUL
    return quantifier(STATEFUL.__issup__(type, other) for other in others)

def issub(type: type, *others: tuple[type], quantifier=None) -> bool:
    if quantifier is None:
        from typed.mods.init import some
        quantifier = some

    from typed.mods.logic import Quantifier
    from typed.mods.check import check
    check.isinstance(obj=quantifier, cls=Quantifier)

    from typed.helper.typesystem import STATEFUL
    return quantifier(STATEFUL.__issub__(type, other) for other in others)

def isterm(term: object, *types: tuple[type], quantifier=None) -> bool:
    if quantifier is None:
        from typed.mods.init import some
        quantifier = some

    from typed.mods.logic import Quantifier
    from typed.mods.check import check
    check.isinstance(obj=quantifier, cls=Quantifier)

    from typed.helper.typesystem import STATEFUL
    return quantifier(STATEFUL.__isterm__(type, term) for type in types)

def isequiv(type: type, *others: tuple[type],  quantifier=None) -> bool:
    if quantifier is None:
        from typed.mods.init import some
        quantifier = some

    from typed.mods.logic import Quantifier
    from typed.mods.check import check
    check.isinstance(obj=quantifier, cls=Quantifier)

    from typed.helper.typesystem import STATEFUL
    return quantifier(STATEFUL.__isequiv__(other, type) for other in others)

class new:
    @staticmethod
    def conf(enabled: bool=True, typesystem=None, err=None, **kwargs):
        from typed.mods.conf import Conf
        return Conf(
            enabled=enabled,
            typesystem=typesystem,
            err=err,
            **kwargs
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
