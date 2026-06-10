from typed.mods.meta.atomic import TYPE, LAZY

class CALLABLE(TYPE):
    """
    The metatype of 'callable types'.
    """

    def __isterm__(typ, trm):
        from inspect import isbuiltin, ismethod, isfunction, isclass
        from typed.mods.func import unwrap
        unwrapped = unwrap(trm)

        return (
            isbuiltin(unwrapped)
            or ismethod(unwrapped)
            or isfunction(unwrapped)
            or isclass(unwrapped)
        )

    def __call__(typ, *args, **kwargs):
        if len(args) == 1 and callable(args[0]) and not kwargs:
            from typed.mods.check import check
            func = args[0]
            check.iscallable(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            return inst
        return super().__call__(*args, **kwargs)

class CLASS(CALLABLE):
    """
    The metatype of 'Python classes'
    """
    def __isterm__(typ, trm):
        from inspect import isclass
        from typed.mods.func import unwrap
        from typed.mods.typesystem import issub

        unwrapped = unwrap(trm)
        if issub(type(trm), typ) or issub(type(unwrapped), typ):
            return True

        return isclass(unwrap(trm))

class METHOD(CALLABLE):
    """
    The metatype of 'method types'.
    """
    def __isterm__(typ, trm):
        from inspect import ismethod
        from typed.mods.func import unwrap
        from typed.mods.typesystem import issub

        unwrapped = unwrap(trm)
        if issub(type(trm), typ) or issub(type(unwrapped), typ):
            return True

        return ismethod(unwrap(trm))

class LAMBDA(CALLABLE):
    """
    The metatype of 'lambda types'.
    """
    def __isterm__(typ, trm):
        from inspect import isfunction
        from typed.mods.func import unwrap
        from typed.mods.typesystem import issub

        unwrapped = unwrap(trm)
        if issub(type(trm), typ) or issub(type(unwrapped), typ):
            return True

        return isfunction(unwrapped) and getattr(unwrapped, "__name__", "") == "<lambda>"

class FUNC(CALLABLE):
    """
    The metatype of functions.
    """
    def __isterm__(typ, trm):
        from typed.mods.func import unwrap
        from inspect import isfunction, ismethod, isbuiltin
        from typed.mods.typesystem import issub

        unwrapped = unwrap(trm)
        if issub(type(trm), typ) or issub(type(unwrapped), typ):
            return True

        return (
            isfunction(unwrapped)
            and getattr(unwrapped, "__name__", "") != "<lambda>"
            and not ismethod(unwrapped)
            and not isbuiltin(unwrapped)
        )

    def __call__(typ, *args, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.typesystem import issub
            if not issub(type(func), CALLABLE):
                from typed.mods.err import TypeErr
                raise TypeErr(
                    term=typ,
                    args=func,
                    received=type(func),
                    expected=typ
                )
            inst = type.__call__(typ)
            inst.__func__ = func
            return inst

        if args or kwargs:
            from typed.mods.err import FuncErr
            raise FuncErr(
                details="received unexpected number of arguments",
                func=typ
            )

        return typ

class PARTIAL(FUNC):
    def __isterm__(typ, trm):
        flags = getattr(trm, "__flags__", None)
        is_partial = getattr(flags, "is_partial", False) if flags else False
        return super().__isterm__(trm) and is_partial

    def __call__(typ, *args, **kwargs):
        if len(args) == 3 and callable(args[0]) and isinstance(args[1], (list, tuple)) and isinstance(args[2], dict) and not kwargs:
            func, bound_args, bound_kwargs = args
            from typed.mods.func import unwrap
            from typed.mods.typesystem import nameof
            from typed.mods.flags import Flags

            inst = type.__call__(typ)
            inst.__func__ = func
            inst.bound_args = list(bound_args)
            inst.bound_kwargs = dict(bound_kwargs)
            inst.__flags__ = Flags(is_func=True, is_partial=True)

            try:
                from typed.mods.general import _
                base = unwrap(func)

                def _fmt_arg(a):
                    if a is _:
                        return "_"
                    return repr(a)

                pos = ", ".join(_fmt_arg(a) for a in bound_args)
                kw  = ", ".join(
                    f"{k}={_fmt_arg(v)}" for k, v in bound_kwargs.items()
                )
                inside = ", ".join(p for p in (pos, kw) if p)
                inst.__display__ = f"{nameof(base)}({inside})"
            except Exception:
                inst.__display__ = nameof(func)

            if hasattr(func, '__name__'):
                inst.__name__ = f"{func.__name__}_partial"
            else:
                inst.__name__ = "partial"

            return inst

        return super().__call__(*args, **kwargs)

class DOM_FUNC(FUNC):
    """
    The metatype of domain-specified functions.
    """
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        from typed.mods.func import signature
        try:
            dom = signature(trm).dom
        except Exception:
            return False

        dom_type = getattr(typ, "__types__", None)
        if dom_type is None:
            return False

        try:
            actual = tuple(dom)
        except TypeError:
            actual = (dom,)

        return actual == dom_type

    def __call__(typ, *args, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if kwargs:
            from typed.mods.err import FuncErr
            raise FuncErr(
                details="function do not expect kwargs",
                func=typ
            )

        if not args: return typ

        if len(args) == 1 and callable(args[0]):
            inst = type.__call__(typ)
            inst.__func__ = args[0]
            return inst

        types = tuple(args)
        check.every.ismember(types, typesystem)

        class_name = f"DomFunc({typesystem.nameof(*types)})"
        from typed.mods.init import TYPESYSTEM

        class DomFunc(typ, metaclass=type(typ)):
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = class_name
            __types__ = types
            __flags__ = Flags(is_func=True, is_dom=True)

        DomFunc.__name__ = class_name
        return DomFunc

class COD_FUNC(FUNC):
    """
    The metatype of codomain-specified functions.
    """
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        from typed.mods.func import signature
        try:
            cod = signature(trm).cod
        except Exception:
            return False

        cod_type = getattr(typ, "__cod__", None)
        if cod_type is None:
            cod_type = getattr(typ, "__types__", None)

        if cod_type is None:
            return False

        try:
            if cod in tuple(cod_type):
                return True
        except TypeError:
            pass
        return cod is cod_type

    def __call__(typ, *args, cod=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            inst = type.__call__(typ)
            inst.__func__ = args[0]
            return inst

        if cod is None and len(args) == 1 and check.isterm(args[0], TYPE, explode=False):
            cod = args[0]
            args = ()

        if cod is None and not args and not kwargs:
            return typ

        if check.isterm(cod, TYPE, explode=False) and not args and not kwargs:
            check.ismember(cod, typesystem)

            class_name = f"CodFunc(cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM

            class CodFunc(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __cod__ = cod
                __flags__ = Flags(is_func=True, is_cod=True)

            CodFunc.__name__ = class_name
            return CodFunc

        raise TypeErr(message="CodFunc(X) expects a single TYPE argument")

class COMP_FUNC(DOM_FUNC, COD_FUNC):
    """
    The metatype of composable functions.
    """
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        dom_types = getattr(typ, "__types__", None)
        cod_type = getattr(typ, "__cod__", None)

        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False

        if dom_types is not None:
            dom = sig.dom
            try:
                actual_dom = tuple(dom)
            except TypeError:
                actual_dom = (dom,)
            if actual_dom != dom_types:
                return False

        if cod_type is not None:
            cod = sig.cod
            if cod is not cod_type:
                return False

        return True

    def __call__(typ, *args, cod=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            inst = type.__call__(typ)
            inst.__func__ = args[0]
            return inst

        if not args and cod is None and not kwargs:
            return typ

        if args and check.every.isterm(args, TYPE, explode=False) and check.isterm(cod, TYPE, explode=False) and not kwargs:
            types = tuple(args)
            check.every.ismember(types, typesystem)
            check.ismember(cod, typesystem)

            class_name = f"CompFunc({typesystem.nameof(*types)}, cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM

            class CompFunc(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = cod
                __flags__ = Flags(is_func=True, is_dom=True, is_cod=True)

            CompFunc.__name__ = class_name
            return CompFunc

        raise TypeErr(message="CompFunc(X, Y, ..., cod=Z) expects TYPE arguments only")

class DOM_HINTED(DOM_FUNC, PARTIAL):
    def __isterm__(typ, trm):
        if isinstance(trm, type) and issubclass(trm, typ):
            return True
        if not super().__isterm__(trm):
            return False

        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False

        expected = getattr(typ, "__types__", None)
        if expected is not None:
            return set(sig.dom) == set(expected)

        return True

    def __call__(typ, *args, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func, cod=False)

            inst = type.__call__(typ)
            inst.__func__ = func
            inst._dom = signature(func).dom
            return inst

        if not args and not kwargs:
            return typ

        if args and check.every.isterm(args, TYPE, explode=False) and not kwargs:
            types = tuple(args)
            check.every.ismember(types, typesystem)

            class_name = f"DomHinted({typesystem.nameof(*types)})"
            from typed.mods.init import TYPESYSTEM

            class DomHinted(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __flags__ = Flags(is_type=True, is_dom_hinted=True)

            DomHinted.__name__ = class_name
            return DomHinted

        raise TypeErr(message=f"{getattr(typ, '__name__', 'DOM_HINTED')}(): expected 0 args, or a callable, or TYPE arguments")

class COD_HINTED(COD_FUNC, PARTIAL):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import issub
        if issub(TYPE(trm), typ):
            return True
        if not super().__isterm__(trm):
            return False

        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False

        expected = getattr(typ, "__cod__", None)
        if expected is not None:
            return sig.cod == expected

        return True

    def __call__(typ, *args, cod=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func, dom=False)

            inst = type.__call__(typ)
            inst.__func__ = func
            inst._cod = signature(func).cod
            return inst

        if cod is None and len(args) == 1 and check.isterm(args[0], TYPE, explode=False):
            cod = args[0]
            args = ()

        if cod is None and not args and not kwargs:
            return typ

        if check.isterm(cod, TYPE, explode=False) and not args and not kwargs:
            check.ismember(cod, typesystem)

            class_name = f"CodHinted(cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM

            class CodHinted(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __cod__ = cod
                __flags__ = Flags(is_type=True, is_cod_hinted=True)

            CodHinted.__name__ = class_name
            return CodHinted

        raise TypeErr(message=f"{getattr(typ, '__name__', 'COD_HINTED')}(): expected 0 args, or a callable, or a single TYPE")

class HINTED(COMP_FUNC, COD_HINTED, DOM_HINTED):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False

        expected_types = getattr(typ, "__types__", None)
        expected_cod = getattr(typ, "__cod__", None)

        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False

        if expected_types is not None:
            if set(sig.dom) != set(expected_types):
                return False

        if expected_cod is not None:
            if sig.cod != expected_cod:
                return False

        return True

    def __call__(typ, *args, cod=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func)

            inst = type.__call__(typ)
            inst.__func__ = func

            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            return inst

        if not args and cod is None and not kwargs:
            return typ

        if args and check.every.isterm(args, TYPE, explode=False) and check.isterm(cod, TYPE, explode=False) and not kwargs:
            types = tuple(args)
            check.every.ismember(types, typesystem)
            check.ismember(cod, typesystem)

            class_name = f"Hinted({typesystem.nameof(*types)}; {typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM

            class Hinted(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = cod
                __flags__ = Flags(is_func=True, is_dom=True, is_cod=True, is_hinted=True)

            Hinted.__name__ = class_name
            return Hinted

        raise TypeErr(message=f"{getattr(typ, '__name__', 'HINTED')}(): expected 0 args, or a callable, or TYPE arguments plus cod=TYPE")

class DOM_TYPED(DOM_HINTED):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        expected = getattr(typ, "__types__", None)
        if expected is not None:
            from typed.mods.func import signature
            try:
                sig = signature(trm)
                return set(sig.dom) == set(expected)
            except Exception:
                return False
        return True

    def __call__(typ, *args, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func, cod=False)

            inst = type.__call__(typ)
            inst.__func__ = func
            inst._dom = signature(func).dom
            return inst

        if not args and not kwargs:
            return typ

        if args and check.every.isterm(args, TYPE, explode=False) and not kwargs:
            types = tuple(args)
            check.every.ismember(types, typesystem)

            class_name = f"DomTyped({typesystem.nameof(*types)})"
            from typed.mods.init import TYPESYSTEM

            class DomTyped(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __flags__ = Flags(is_type=True, is_dom_typed=True)

            DomTyped.__name__ = class_name
            return DomTyped

        raise TypeErr(message=f"{getattr(typ, '__name__', 'DOM_TYPED')}(): expected 0 args, or a callable, or TYPE arguments")


class COD_TYPED(COD_HINTED):
    def __isterm__(typ, trm):
        if not super().__isterm__(trm):
            return False
        expected = getattr(typ, "__cod__", None)
        if expected is not None:
            from typed.mods.func import signature
            try:
                sig = signature(trm)
                return sig.cod == expected
            except Exception:
                return False
        return True

    def __call__(typ, *args, cod=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func, dom=False)

            inst = type.__call__(typ)
            inst.__func__ = func
            inst._cod = signature(func).cod
            return inst

        if cod is None and len(args) == 1 and check.isterm(args[0], TYPE, explode=False):
            cod = args[0]
            args = ()

        if cod is None and not args and not kwargs:
            return typ

        if check.isterm(cod, TYPE, explode=False) and not args and not kwargs:
            check.ismember(cod, typesystem)

            class_name = f"CodTyped(cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM

            class CodTyped(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __cod__ = cod
                __flags__ = Flags(is_type=True, is_cod_typed=True)

            CodTyped.__name__ = class_name
            return CodTyped

        raise TypeErr(message=f"{getattr(typ, '__name__', 'COD_TYPED')}(): expected 0 args, or a callable, or a single TYPE")

class TYPED(HINTED, DOM_TYPED, COD_TYPED):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        flags = getattr(trm, "__flags__", None)
        is_partial = getattr(flags, "is_partial", False) if flags else False
        is_lazy = getattr(flags, "is_lazy", False) if flags else False

        if is_partial:
            orig = getattr(trm, '__func__', None)
            if orig is None:
                return False
            orig_flags = getattr(orig, "__flags__", None)
            orig_lazy = getattr(orig_flags, "is_lazy", False) if orig_flags else False
            if orig_lazy:
                return False
            return isterm(orig, typ)

        if is_lazy:
            return False

        if not super().__isterm__(trm):
            return False

        expected_types = getattr(typ, "__types__", None)
        expected_cod = getattr(typ, "__cod__", None)

        if expected_types is not None or expected_cod is not None:
            from typed.mods.types.atomic import Any
            from typed.mods.func import signature
            try:
                sig = signature(trm)
            except Exception:
                return False

            if expected_types is not None:
                if len(expected_types) == 1 and expected_types[0] is Any:
                    pass
                elif set(sig.dom) != set(expected_types):
                    return False

            if expected_cod is not None:
                if sig.cod != expected_cod:
                    return False

        return True

    def __call__(typ, *args, cod=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func)

            inst = type.__call__(typ)
            inst.__func__ = func

            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            return inst

        if not args and cod is None and not kwargs:
            return typ

        if cod is not None and check.every.isterm(args, TYPE, explode=False):
            types = tuple(args)
            check.every.ismember(types, typesystem)
            check.ismember(cod, typesystem)

            class_name = f"Typed({typesystem.nameof(*types)}, cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM

            class Typed(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = cod
                __flags__ = Flags(is_func=True, is_typed=True)

            Typed.__name__ = class_name
            return Typed

        raise TypeErr(message="Typed() expects a callable, or TYPE arguments plus cod=TYPE")

class CONDITION(TYPED):
    def __isterm__(typ, trm):
        from typed.mods.types.atomic import Bool
        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False
        return super().__isterm__(trm) and sig.cod is Bool

    def __call__(typ, *args, typesystem=None, **kwargs):
        from typed.mods.types.atomic import Type, Bool
        from typed.mods.resolve import resolve
        from typed.mods.check import check
        from typed.mods.err import TypeErr
        from typed.mods.flags import Flags

        typesystem = resolve.typesystem.entity(typesystem)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            check.ishinted(func)

            inst = type.__call__(typ)
            inst.__func__ = func

            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod

            if getattr(inst, "_cod", None) is not Bool:
                raise TypeErr(
                    message=f"Wrong type in codomain of '{typesystem.nameof(func)}':\n"
                    f" ==> '{typesystem.nameof(getattr(inst, '_cod', None))}' is not 'Bool'"
                )
            return inst

        if not args and not kwargs:
            return typ

        if args and check.every.isterm(args, Type, explode=False) and not kwargs:
            types = tuple(args)
            check.every.ismember(types, typesystem)

            class_name = f"Condition({typesystem.nameof(*types)})"
            from typed.mods.init import TYPESYSTEM

            class Condition(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = Bool
                __flags__ = Flags(is_type=True, is_condition=True)

            Condition.__name__ = class_name
            return Condition

        raise TypeErr(message="Condition() expects a Bool-returning callable, or TYPE arguments")

class FAMILY(TYPED):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import issub
        from typed.mods.meta.atomic import TYPE
        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False
        return super().__isterm__(trm) and issub(sig.cod, TYPE)

class CONSTRUCTOR(FAMILY):
    def __isterm__(typ, trm):
        from typed.mods.types.constructor import Tuple
        from typed.mods.typesystem import issub
        from typed.mods.meta.atomic import TYPE
        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False
        return super().__isterm__(trm) and issub(sig.dom, Tuple(TYPE))

class LAZY_TYPED(LAZY, HINTED):
    def __isterm__(typ, trm):
        flags = getattr(trm, "__flags__", None)
        is_partial = getattr(flags, "is_partial", False) if flags else False

        if is_partial:
            orig = getattr(trm, "__func__", None)
            if orig is not None:
                from typed.mods.typesystem import isterm
                return isterm(orig, typ)
            return False

        return super().__isterm__(trm)

    def __call__(typ, *args, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature

            inst = type.__call__(typ)
            inst.__func__ = func
            inst._wrapped = None

            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            return inst

        return super(LAZY_TYPED, typ).__call__(*args, typesystem=typesystem, **kwargs)
