import weakref
from functools import lru_cache as cache
from typed.mods.types.atomic import Dom, Cod, Nill, Bool
from typed.mods.meta.atomic import TYPE

class Arg:
    def __init__(self, name: str, hint: object, default: object):
        self.name = name
        self.hint = hint
        self.default = default

class Signature:
    def __init__(self, func: callable, dom: Dom, cod: Cod, args: tuple[Arg, ...]):
        self.func = func
        self.dom = dom
        self.cod = cod
        self.args = args

    def bind(self, *args, **kwargs):
        return self.func(*args, **kwargs)

    def reduce(self, *reduce_args, **reduce_kwargs):
        fixed_values = {}

        for i, arg_val in enumerate(reduce_args):
            if arg_val is not Ellipsis:
                if i < len(self.args):
                    fixed_values[self.args[i].name] = arg_val

        for k, v in reduce_kwargs.items():
            if v is not Ellipsis:
                fixed_values[k] = v

        new_args = []
        new_dom = []
        for i, arg in enumerate(self.args):
            if arg.name not in fixed_values:
                new_args.append(arg)
                if i < len(self.dom):
                    new_dom.append(self.dom[i])

        new_sig = Signature(
            func=self.func,
            dom=tuple(new_dom),
            cod=self.cod,
            args=tuple(new_args)
        )
        return new_sig, fixed_values

def compose(f, g):
    def composed(*args, **kwargs):
        return f(g(*args, **kwargs))

    if hasattr(g, 'dom'):
        composed.dom = g.dom
    if hasattr(f, 'cod'):
        composed.cod = f.cod

    composed.__name__ = f"({getattr(f, '__name__', str(f))} << {getattr(g, '__name__', str(g))})"
    return composed

@cache
def hints(func):
    from typing import get_type_hints
    try:
        return get_type_hints(func)
    except Exception:
        return {}

@cache
def args(func: callable) -> tuple[Arg, ...]:
    from inspect import signature as _signature, Parameter
    from typed.mods.err import NotDefined

    actual_func = unwrap(func)
    try:
        sig = _signature(actual_func)
    except Exception:
        return ()

    hints_dict = hints(actual_func)

    arg_objs = []
    for name, param in sig.parameters.items():
        if param.kind in (Parameter.POSITIONAL_ONLY, Parameter.POSITIONAL_OR_KEYWORD, Parameter.KEYWORD_ONLY):
            hint = hints_dict.get(name, NotDefined)
            default = NotDefined if param.default is Parameter.empty else param.default
            arg_objs.append(Arg(name=name, hint=hint, default=default))

    return tuple(arg_objs)

@cache
def signature(func: callable) -> Signature:
    from typed.mods.meta.atomic import TYPE
    from typed.mods.err import NotDefined

    target = unwrap(func)

    target_args = args(func)
    hints_dict = hints(target)

    hint_dom = tuple(a.hint for a in target_args if a.hint is not None and a.hint is not NotDefined)
    hint_cod = hints_dict.get('return', None)

    if not isinstance(hint_cod, TYPE):
        hint_cod = None

    orig_dom, orig_cod = (), None

    if hasattr(func, "_dom"):
        orig_dom = func._dom
        orig_cod = getattr(func, "_cod", None)
    elif hasattr(func, "__dict__") and "dom" in func.__dict__:
        orig_dom = func.__dict__["dom"]
        orig_cod = func.__dict__.get("cod", None)
    elif hasattr(target, "__dict__") and "dom" in target.__dict__:
        orig_dom = target.__dict__["dom"]
        orig_cod = target.__dict__.get("cod", None)
    else:
        orig_dom = hint_dom
        orig_cod = hint_cod

    from typed.mods.check import require
    require.hint.dom(func, orig_dom, hint_dom)

    if hint_cod is not None:
        require.hint.cod(func, orig_cod, hint_cod)

    return Signature(
        func=target,
        dom=orig_dom,
        cod=orig_cod,
        args=target_args
    )

def reduce(func, *reduce_args, **reduce_kwargs):
    sig = signature(func)
    new_sig, fixed_values = sig.reduce(*reduce_args, **reduce_kwargs)

    def reduced(*args, **kwargs):
        call_kwargs = dict(fixed_values)
        for i, arg_val in enumerate(args):
            if i < len(new_sig.args):
                call_kwargs[new_sig.args[i].name] = arg_val
        call_kwargs.update(kwargs)

        final_args = []
        final_kwargs = dict(call_kwargs)
        for arg in sig.args:
            if arg.name in final_kwargs:
                final_args.append(final_kwargs.pop(arg.name))

        return func(*final_args, **final_kwargs)

    reduced.__name__ = getattr(func, "__name__", "reduced")
    reduced._dom = new_sig.dom
    reduced._cod = new_sig.cod

    hints_dict = getattr(func, "__annotations__", {}).copy()
    for k in fixed_values:
        if k in hints_dict:
            del hints_dict[k]
    reduced.__annotations__ = hints_dict

    return reduced

__wrap_attrs__ = ["__func__", "__wrapped__", "func", "original_func"]

def unwrap(func: callable, attrs: list[str]=None) -> callable:
    from typed.mods.check import require
    require.iscallable(func)
    attrs_tuple = tuple(attrs) if attrs is not None else tuple(__wrap_attrs__)
    from typed.helper.func import _unwrap_cache
    return _unwrap_cache(func, attrs_tuple)

def func(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Func, LazyFunc
        if lz:
            return LazyFunc(fn, check=check, defaults=defaults, envs=envs)
        return Func(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def hinted(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Hinted, LazyHinted
        if lz:
            return LazyHinted(fn, check=check, defaults=defaults, envs=envs)
        return Hinted(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def typed(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Typed, LazyTyped
        if lz:
            return LazyTyped(fn, check=check, defaults=defaults, envs=envs)
        return Typed(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def condition(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Condition, LazyCondition
        if lz:
            return LazyCondition(fn, check=check, defaults=defaults, envs=envs)
        return Condition(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)


def family(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Family, LazyFamily
        if lz:
            return LazyFamily(fn, check=check, defaults=defaults, envs=envs)
        return Family(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)

def constructor(f=None, *, check: bool = None, lazy: bool = None, defaults: bool = None, envs=None):
    def decorator(fn):
        from typed.mods.resolve import resolve
        lz = resolve.typecheck.lazy(lazy)

        from typed.mods.types.func import Constructor, LazyConstructor
        if lz:
            return LazyConstructor(fn, check=check, defaults=defaults, envs=envs)
        return Constructor(fn, check=check, defaults=defaults, envs=envs)

    if f is None:
        return decorator
    return decorator(f)

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

class nill:
    def func():
        return None

    class cls:
        def nill(self):
            return None

    def comp():
        return None

    class dom:
        def func():
            return None

        def hinted(x: Nill):
            return None

        def typed(x: Nill):
            return None

    class cod:
        def func():
            pass

        def hinted() -> Nill:
            return None

        def typed() -> Nill:
            return None

    def hinted(x: Nill) -> Nill:
        return None

    def typed(x: Nill) -> Nill:
        return None

    def condition(x: Nill) -> Bool:
        return False

    def family(x: Nill) -> TYPE:
        return Nill

    def constructor(x: TYPE) -> TYPE:
        return Nill
