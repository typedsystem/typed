__wrap_attrs__ = ["__func__", "__wrapped__", "func", "original_func"]

def unwrap(func: callable, attrs: list[str]=None) -> callable:
    from typed.mods.check import require
    require.iscallable(func)
    attrs_tuple = tuple(attrs) if attrs is not None else tuple(__wrap_attrs__)
    from typed.helper.wrap import _unwrap_cache
    return _unwrap_cache(func, attrs_tuple)

def func(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None, err=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)
        from typed.mods.types.func import Func, LazyFunc
        if lz:
            inst = LazyFunc(fn, check=check, defaults=defaults, envs=envs)
        else:
            inst = Func(fn, check=check, defaults=defaults, envs=envs)
        if err is not None:
            inst.__err__ = err
        inst.__type__ = type(inst)
        return inst
    if f is None:
        return decorator
    return decorator(f)

def hinted(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None, err=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)
        from typed.mods.types.func import Hinted, LazyHinted
        if lz:
            inst = LazyHinted(fn, check=check, defaults=defaults, envs=envs)
        else:
            inst = Hinted(fn, check=check, defaults=defaults, envs=envs)
        if err is not None:
            inst.__err__ = err
        inst.__type__ = type(inst)
        return inst
    if f is None:
        return decorator
    return decorator(f)


def typed(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None, err=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)
        from typed.mods.types.func import Typed, LazyTyped
        if lz:
            inst = LazyTyped(fn, check=check, defaults=defaults, envs=envs)
        else:
            inst = Typed(fn, check=check, defaults=defaults, envs=envs)
        if err is not None:
            inst.__err__ = err
        inst.__type__ = type(inst)
        return inst
    if f is None:
        return decorator
    return decorator(f)


def condition(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None, err=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)
        from typed.mods.types.func import Condition, LazyCondition
        if lz:
            inst = LazyCondition(fn, check=check, defaults=defaults, envs=envs)
        else:
            inst = Condition(fn, check=check, defaults=defaults, envs=envs)
        if err is not None:
            inst.__err__ = err
        inst.__type__ = type(inst)
        return inst
    if f is None:
        return decorator
    return decorator(f)


def family(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None, err=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)
        from typed.mods.types.func import Family, LazyFamily
        if lz:
            inst = LazyFamily(fn, check=check, defaults=defaults, envs=envs)
        else:
            inst = Family(fn, check=check, defaults=defaults, envs=envs)
        if err is not None:
            inst.__err__ = err
        inst.__type__ = type(inst)
        return inst
    if f is None:
        return decorator
    return decorator(f)

def constructor(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None, err=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)
        from typed.mods.types.func import Constructor, LazyConstructor
        if lz:
            inst = LazyConstructor(fn, check=check, defaults=defaults, envs=envs)
        else:
            inst = Constructor(fn, check=check, defaults=defaults, envs=envs)
        if err is not None:
            inst.__err__ = err
        inst.__type__ = type(inst)
        return inst
    if f is None:
        return decorator
    return decorator(f)

def enum(cls=None, *, typesystem=None):
    def decorator(target_cls):
        kwargs = {
            k: v
            for k, v in target_cls.__dict__.items()
            if not k.startswith('_')
        }
        from typed.mods.types.dependent import Enum
        return Enum(
            typesystem=typesystem,
            **kwargs
        )
    if cls is None:
        return decorator
    return decorator(cls)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import TypeVar, Callable, Any, overload
    T = TypeVar('T')
    F = TypeVar('F', bound=Callable[..., Any])

    @overload
    def service(*, name: str=None) -> Callable[[type[T]], type[T]]: 
        ...
    @overload
    def service(cls: type[T], *, name: str=None, err: Exception=None) -> type[T]:
        ...

    @overload
    def action(*, check: bool=None, defaults: bool=None, envs=None, err: Exception=None) -> Callable[[F], F]:
        ...
    @overload
    def action(f: F, *, check: bool=None, defaults: bool=None, envs=None, err: Exception=None) -> F:
        ...

class action:
    _fallback_ctx = None

    def __new__(
        cls,
        f=None,
        *,
        check=None,
        lazy=None,
        defaults=None,
        envs=None,
        err=None
    ):
        def decorator(fn):
            import inspect
            from typed.mods.types.atomic import Any

            if not hasattr(fn, "__annotations__"):
                fn.__annotations__ = {}
            try:
                sig = inspect.signature(fn)
                for name in sig.parameters:
                    if name not in fn.__annotations__:
                        fn.__annotations__[name] = Any
                if "return" not in fn.__annotations__:
                    fn.__annotations__["return"] = Any
            except Exception:
                pass

            inst = typed(
                check=check,
                lazy=lazy,
                defaults=defaults,
                envs=envs,
                err=err
            )(fn)

            if hasattr(inst, "__flags__"):
                inst.__flags__.is_action = True
            else:
                from typed.mods.flags import Flags
                inst.__flags__ = Flags(is_action=True)
            return inst

        if f is None:
            return decorator
        return decorator(f)

    @classmethod
    def term(cls, trm, type=None):
        if type is Ellipsis:
            if cls._fallback_ctx is not None:
                type = cls._fallback_ctx
            else:
                try:
                    type = trm.__type__.__service__.__fallback__
                except AttributeError:
                    type = getattr(
                        trm,
                        '__type__',
                        trm.__class__
                    )

        from typed.mods.typesystem import term
        return term(value=trm, type=type)

def service(cls=None, *, name=None, err=None, fallback=Ellipsis):
    def decorator(target_cls):
        if err is not None:
            for attr_name, attr_value in target_cls.__dict__.items():
                if callable(attr_value) and not attr_name.startswith('_'):
                    flags = getattr(attr_value, "__flags__", None)
                    if flags and getattr(flags, "is_action", False):
                        if getattr(attr_value, "__err__", None) is None:
                            attr_value.__err__ = err
        from typed.mods.types.service import Service
        service_obj = Service(target_cls)
        if name:
            service_obj.__display__ = name
        if err is not None:
            service_obj.__err__ = err
        service_obj.__fallback__ = fallback
        return service_obj

    if cls is None:
        return decorator
    return decorator(cls)

def closure(cls=None, *, lt="__lt__"):
    if cls is None:
        def wrapper(c):
            return closure(c, lt=lt)
        return wrapper

    if lt != "__lt__" and hasattr(cls, lt):
        if '__lt__' not in cls.__dict__:
            source_method = getattr(cls, lt)
            def _lt(self, other):
                try:
                    return getattr(type(self), lt)(self, other)
                except Exception:
                    return NotImplemented

            _lt.__name__ = '__lt__'
            cls.__lt__ = _lt

    import weakref
    _eq_cache = weakref.WeakKeyDictionary()

    def _eq(self, other):
        if self is other:
            return True

        try:
            if self in _eq_cache and other in _eq_cache[self]:
                return _eq_cache[self][other]
        except TypeError:
            pass

        try:
            try:
                lt_self = type(self).__lt__(self, other)
            except AttributeError:
                lt_self = NotImplemented

            if lt_self is NotImplemented:
                result = NotImplemented
            elif not lt_self:
                result = False
            else:
                try:
                    lt_other = type(other).__lt__(other, self)
                except AttributeError:
                    lt_other = NotImplemented

                if lt_other is NotImplemented:
                    result = NotImplemented
                else:
                    result = bool(lt_self and lt_other)

            if result is not NotImplemented:
                try:
                    if self not in _eq_cache:
                        _eq_cache[self] = weakref.WeakKeyDictionary()
                    _eq_cache[self][other] = result
                    if other not in _eq_cache:
                        _eq_cache[other] = weakref.WeakKeyDictionary()
                    _eq_cache[other][self] = result
                except TypeError:
                    pass

            return result
        except Exception:
            return NotImplemented

    _eq.__name__ = '__eq__'

    def _hash(self):
        return id(self)
    _hash.__name__ = '__hash__'

    def _le(self, other):
        try:
            try:
                lt_self = type(self).__lt__(self, other)
            except AttributeError:
                lt_self = NotImplemented

            if lt_self is True:
                return True

            try:
                eq_self = type(self).__eq__(self, other)
            except AttributeError:
                eq_self = NotImplemented

            if eq_self is True:
                return True

            if lt_self is NotImplemented and eq_self is NotImplemented:
                return NotImplemented
            return False
        except Exception:
            return NotImplemented
    _le.__name__ = '__le__'

    def _gt(self, other):
        try:
            return type(other).__lt__(other, self)
        except AttributeError:
            return NotImplemented
        except Exception:
            return NotImplemented
    _gt.__name__ = '__gt__'

    def _ge(self, other):
        try:
            try:
                lt_other = type(other).__lt__(other, self)
            except AttributeError:
                lt_other = NotImplemented

            if lt_other is True:
                return True

            try:
                eq_self = type(self).__eq__(self, other)
            except AttributeError:
                eq_self = NotImplemented

            if eq_self is True:
                return True

            if lt_other is NotImplemented and eq_self is NotImplemented:
                return NotImplemented
            return False
        except Exception:
            return NotImplemented
    _ge.__name__ = '__ge__'

    def _dir(self):
        try:
            base_dir = set(super(cls, self).__dir__())
        except AttributeError:
            base_dir = set(dir(type(self)))

        base_dir.update({'__lt__', '__le__', '__eq__', '__gt__', '__ge__', '__hash__'})
        return sorted(list(base_dir))
    _dir.__name__ = '__dir__'

    if '__eq__' not in cls.__dict__:
        cls.__eq__ = _eq

    if '__hash__' not in cls.__dict__ or cls.__hash__ is None:
        cls.__hash__ = _hash

    if hasattr(cls, '__lt__'):
        if '__le__' not in cls.__dict__:
            cls.__le__ = _le
        if '__gt__' not in cls.__dict__:
            cls.__gt__ = _gt
        if '__ge__' not in cls.__dict__:
            cls.__ge__ = _ge

    if '__dir__' not in cls.__dict__:
        cls.__dir__ = _dir

    return cls
