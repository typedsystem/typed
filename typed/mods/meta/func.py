import weakref
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
            from typed.mods.check import require
            func = args[0]
            require.iscallable(func)
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

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            if chk:
                from typed.mods.check import require
                require.isterm(
                    func,
                    typ,
                    typesystem=typesystem
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        if args or kwargs:
            from typed.mods.err import FuncErr
            raise FuncErr(
                details="received unexpected number of arguments",
                func=typ
            )

        return typ

class DOM_FUNC(FUNC):
    """
    The metatype of domain-specified functions.
    """
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if kwargs:
            from typed.mods.err import FuncErr
            raise FuncErr(
                details="function do not expect kwargs",
                func=typ
            )

        if not args:
            return typ

        if len(args) == 1 and callable(args[0]):
            func = args[0]
            if chk:
                from typed.mods.check import require
                require.isterm(
                    func,
                    typ,
                    typesystem=typesystem
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        types = tuple(args)
        cache_key = (typ, types, id(typesystem))
        if cache_key in typ._type_cache:
            return typ._type_cache[cache_key]

        from typed.mods.check import require
        require.every.ismember(types, typesystem)
        class_name = f"DomFunc({typesystem.nameof(*types)})"
        from typed.mods.init import TYPESYSTEM
        from typed.mods.flags import Flags

        class DomFunc(typ, metaclass=type(typ)):
            __typesystems__ = {TYPESYSTEM, typesystem}
            __display__ = class_name
            __types__ = types
            __flags__ = Flags(
                is_func=True,
                is_dom=True
            )

        DomFunc.__name__ = class_name
        typ._type_cache[cache_key] = DomFunc
        return DomFunc

class COD_FUNC(FUNC):
    """
    The metatype of codomain-specified functions.
    """
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, cod=None, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            if chk:
                from typed.mods.check import require
                require.isterm(
                    func,
                    typ,
                    typesystem=typesystem
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        from typed.mods.check import require
        if cod is None and len(args) == 1 and require.isterm(
            args[0],
            TYPE,
            explode=False
        ):
            cod = args[0]
            args = ()

        if cod is None and not args and not kwargs:
            return typ

        if require.isterm(
            cod,
            TYPE,
            explode=False
        ) and not args and not kwargs:
            cache_key = (typ, cod, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.ismember(cod, typesystem)
            class_name = f"CodFunc(cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class CodFunc(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __cod__ = cod
                __flags__ = Flags(
                    is_func=True,
                    is_cod=True
                )

            CodFunc.__name__ = class_name
            typ._type_cache[cache_key] = CodFunc
            return CodFunc

        raise TypeErr(
            message="CodFunc(X) expects a single TYPE argument"
        )

class COMP_FUNC(DOM_FUNC, COD_FUNC):
    """
    The metatype of composable functions.
    """
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, cod=None, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            if chk:
                from typed.mods.check import require
                require.isterm(
                    func,
                    typ,
                    typesystem=typesystem
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        if not args and cod is None and not kwargs:
            return typ

        from typed.mods.check import require
        if args and require.every.isterm(
            args,
            TYPE,
            explode=False
        ) and require.isterm(
            cod,
            TYPE,
            explode=False
        ) and not kwargs:
            types = tuple(args)
            cache_key = (typ, types, cod, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.every.ismember(types, typesystem)
            require.ismember(cod, typesystem)
            class_name = f"CompFunc({typesystem.nameof(*types)}, cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class CompFunc(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = cod
                __flags__ = Flags(
                    is_func=True,
                    is_dom=True,
                    is_cod=True
                )

            CompFunc.__name__ = class_name
            typ._type_cache[cache_key] = CompFunc
            return CompFunc

        raise TypeErr(
            message="CompFunc(X, Y, ..., cod=Z) expects TYPE arguments only"
        )

class DOM_HINTED(DOM_FUNC):
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(
                    func,
                    cod=False
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._dom = signature(func).dom
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        if not args and not kwargs:
            return typ

        from typed.mods.check import require
        if args and require.every.isterm(
            args,
            TYPE,
            explode=False
        ) and not kwargs:
            types = tuple(args)
            cache_key = (typ, types, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.every.ismember(types, typesystem)
            class_name = f"DomHinted({typesystem.nameof(*types)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class DomHinted(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __flags__ = Flags(
                    is_type=True,
                    is_dom_hinted=True
                )

            DomHinted.__name__ = class_name
            typ._type_cache[cache_key] = DomHinted
            return DomHinted

        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'DOM_HINTED')}(): expected 0 args, or a callable, or TYPE arguments"
        )

class COD_HINTED(COD_FUNC):
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, cod=None, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(
                    func,
                    dom=False
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._cod = signature(func).cod
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        from typed.mods.check import require
        if cod is None and len(args) == 1 and require.isterm(
            args[0],
            TYPE,
            explode=False
        ):
            cod = args[0]
            args = ()

        if cod is None and not args and not kwargs:
            return typ

        if require.isterm(
            cod,
            TYPE,
            explode=False
        ) and not args and not kwargs:
            cache_key = (typ, cod, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.ismember(cod, typesystem)
            class_name = f"CodHinted(cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class CodHinted(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __cod__ = cod
                __flags__ = Flags(
                    is_type=True,
                    is_cod_hinted=True
                )

            CodHinted.__name__ = class_name
            typ._type_cache[cache_key] = CodHinted
            return CodHinted

        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'COD_HINTED')}(): expected 0 args, or a callable, or a single TYPE"
        )

class HINTED(COMP_FUNC, COD_HINTED, DOM_HINTED):
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, cod=None, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(func)
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        if not args and cod is None and not kwargs:
            return typ

        from typed.mods.check import require
        if args and require.every.isterm(
            args,
            TYPE,
            explode=False
        ) and require.isterm(
            cod,
            TYPE,
            explode=False
        ) and not kwargs:
            types = tuple(args)
            cache_key = (typ, types, cod, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.every.ismember(types, typesystem)
            require.ismember(cod, typesystem)
            class_name = f"Hinted({typesystem.nameof(*types)}; {typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class Hinted(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = cod
                __flags__ = Flags(
                    is_func=True,
                    is_dom=True,
                    is_cod=True,
                    is_hinted=True
                )

            Hinted.__name__ = class_name
            typ._type_cache[cache_key] = Hinted
            return Hinted

        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'HINTED')}(): expected 0 args, or a callable, or TYPE arguments plus cod=TYPE"
        )

class DOM_TYPED(DOM_HINTED):
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(
                    func,
                    cod=False
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._dom = signature(func).dom
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        if not args and not kwargs:
            return typ

        from typed.mods.check import require
        if args and require.every.isterm(
            args,
            TYPE,
            explode=False
        ) and not kwargs:
            types = tuple(args)
            cache_key = (typ, types, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.every.ismember(types, typesystem)
            class_name = f"DomTyped({typesystem.nameof(*types)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class DomTyped(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __flags__ = Flags(
                    is_type=True,
                    is_dom_typed=True
                )

            DomTyped.__name__ = class_name
            typ._type_cache[cache_key] = DomTyped
            return DomTyped

        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'DOM_TYPED')}(): expected 0 args, or a callable, or TYPE arguments"
        )

class COD_TYPED(COD_HINTED):
    _type_cache = weakref.WeakValueDictionary()

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

    def __call__(typ, *args, cod=None, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(
                    func,
                    dom=False
                )
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._cod = signature(func).cod
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        from typed.mods.check import check as __check, require
        if cod is None and len(args) == 1 and __check.isterm(
            args[0],
            TYPE
        ):
            cod = args[0]
            args = ()

        if cod is None and not args and not kwargs:
            return typ

        if __check.isterm(
            cod,
            TYPE
        ) and not args and not kwargs:
            cache_key = (typ, cod, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.ismember(cod, typesystem)
            class_name = f"CodTyped(cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class CodTyped(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __cod__ = cod
                __flags__ = Flags(
                    is_type=True,
                    is_cod_typed=True
                )

            CodTyped.__name__ = class_name
            typ._type_cache[cache_key] = CodTyped
            return CodTyped

        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'COD_TYPED')}(): expected 0 args, or a callable, or a single TYPE"
        )

class TYPED(HINTED, DOM_TYPED, COD_TYPED):
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        flags = getattr(trm, "__flags__", None)
        is_lazy = getattr(flags, "is_lazy", False) if flags else False
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

    def __call__(typ, *args, cod=None, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if "cod" in kwargs:
            cod = kwargs.pop("cod")

        if len(args) == 1 and callable(args[0]) and cod is None and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(func)
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            return inst

        if not args and cod is None and not kwargs:
            return typ

        from typed.mods.check import check as __check, require
        if cod is not None and __check.every.isterm(
            args,
            TYPE
        ):
            types = tuple(args)
            cache_key = (typ, types, cod, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.every.ismember(types, typesystem)
            require.ismember(cod, typesystem)
            class_name = f"Typed({typesystem.nameof(*types)}, cod={typesystem.nameof(cod)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class Typed(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = cod
                __flags__ = Flags(
                    is_func=True,
                    is_typed=True
                )

            Typed.__name__ = class_name
            typ._type_cache[cache_key] = Typed
            return Typed

        raise TypeErr(
            message="Typed() expects a callable, or TYPE arguments plus cod=TYPE"
        )

class CONDITION(TYPED):
    _type_cache = weakref.WeakValueDictionary()

    def __isterm__(typ, trm):
        from typed.mods.types.atomic import Bool
        from typed.mods.func import signature
        try:
            sig = signature(trm)
        except Exception:
            return False
        return super().__isterm__(trm) and sig.cod is Bool

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.types.atomic import Type, Bool
        from typed.mods.resolve import resolve
        from typed.mods.err import TypeErr
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(func)
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            if getattr(inst, "_cod", None) is not Bool:
                raise TypeErr(
                    message=f"Wrong type in codomain of '{typesystem.nameof(func)}':\n"
                    f" ==> '{typesystem.nameof(getattr(inst, '_cod', None))}' is not 'Bool'"
                )
            return inst

        if not args and not kwargs:
            return typ

        from typed.mods.check import check as __check, require
        if args and __check.every.isterm(
            args,
            Type,
            explode=False
        ) and not kwargs:
            types = tuple(args)
            cache_key = (typ, types, id(typesystem))
            if cache_key in typ._type_cache:
                return typ._type_cache[cache_key]
            require.every.ismember(types, typesystem)
            class_name = f"Condition({typesystem.nameof(*types)})"
            from typed.mods.init import TYPESYSTEM
            from typed.mods.flags import Flags

            class Condition(typ, metaclass=type(typ)):
                __typesystems__ = {TYPESYSTEM, typesystem}
                __display__ = class_name
                __types__ = types
                __cod__ = Bool
                __flags__ = Flags(
                    is_type=True,
                    is_condition=True
                )

            Condition.__name__ = class_name
            typ._type_cache[cache_key] = Condition
            return Condition

        raise TypeErr(
            message="Condition() expects a Bool-returning callable, or TYPE arguments"
        )

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

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(func)
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            return inst
        return super().__call__(
            *args,
            typesystem=typesystem,
            check=check,
            defaults=defaults,
            envs=envs,
            **kwargs
        )

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

    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        chk = resolve.typecheck.check(check, envs)
        defs = resolve.typecheck.defaults(defaults)

        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            if chk:
                from typed.mods.check import require
                require.ishinted(func)
            if defs:
                from typed.mods.check import require
                require.defaults(func)
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._check = chk
            inst._defaults = defs
            inst._envs = envs
            sig = signature(func)
            inst._dom = sig.dom
            inst._cod = sig.cod
            return inst
        return super().__call__(
            *args,
            typesystem=typesystem,
            check=check,
            defaults=defaults,
            envs=envs,
            **kwargs
        )

class LAZY_FUNC(LAZY, CALLABLE):
    def __isterm__(typ, trm):
        return super().__isterm__(trm)

    def __call__(typ, *args, target_type=None, check=None, defaults=None, envs=None, typesystem=None, **kwargs):
        from typed.mods.resolve import resolve
        typesystem = resolve.typesystem.entity(typesystem)
        if len(args) == 1 and callable(args[0]) and not kwargs:
            func = args[0]
            from typed.mods.func import signature
            inst = type.__call__(typ)
            inst.__func__ = func
            inst._wrapped = None
            inst._target_type = target_type
            inst._check = check
            inst._defaults = defaults
            inst._envs = envs
            try:
                sig = signature(func)
                inst._lazy_dom = sig.dom
                inst._lazy_cod = sig.cod
            except Exception:
                pass
            return inst
        return super(LAZY_FUNC, typ).__call__(
            *args,
            typesystem=typesystem,
            **kwargs
        )

class LAZY_HINTED(LAZY_FUNC, HINTED):
    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.types.func import Hinted
        return super().__call__(
            *args,
            target_type=Hinted,
            check=check,
            defaults=defaults,
            envs=envs,
            typesystem=typesystem,
            **kwargs
        )

class LAZY_TYPED(LAZY_FUNC, TYPED):
    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.types.func import Typed
        return super().__call__(
            *args,
            target_type=Typed,
            check=check,
            defaults=defaults,
            envs=envs,
            typesystem=typesystem,
            **kwargs
        )

class LAZY_CONDITION(LAZY_FUNC, CONDITION):
    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.types.func import Condition
        return super().__call__(
            *args,
            target_type=Condition,
            check=check,
            defaults=defaults,
            envs=envs,
            typesystem=typesystem,
            **kwargs
        )

class LAZY_FAMILY(LAZY_FUNC, FAMILY):
    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.types.func import Family
        return super().__call__(
            *args,
            target_type=Family,
            check=check,
            defaults=defaults,
            envs=envs,
            typesystem=typesystem,
            **kwargs
        )

class LAZY_CONSTRUCTOR(LAZY_FUNC, CONSTRUCTOR):
    def __call__(typ, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
        from typed.mods.types.func import Constructor
        return super().__call__(
            *args,
            target_type=Constructor,
            check=check,
            defaults=defaults,
            envs=envs,
            typesystem=typesystem,
            **kwargs
        )
