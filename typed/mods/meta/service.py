from typing import TYPE_CHECKING
from typed.mods.meta.atomic import TYPE
from typed.mods.flags import Flags
from typed.mods.meta.func import FUNC

class ACTION(FUNC):
    def __call__(typ, *args, **kwargs):
        if not args and not kwargs:
            return typ
        inst = super().__call__(*args, **kwargs)
        if hasattr(inst, '__flags__'):
            inst.__flags__.is_action = True
        else:
            inst.__flags__ = Flags(is_func=True, is_action=True)
        return inst

    def term(typ, trm, type=None):
        from typed.mods.typesystem import term
        return term(value=trm, type=type)

class SERVICE(TYPE):
    def __getattr__(typ, name):
        target = getattr(typ, "__target__", None)
        if target is not None and hasattr(target, name):
            return getattr(target, name)
        raise AttributeError(f"type object '{getattr(typ, '__name__', 'Service')}' has no attribute '{name}'")

    def __call__(typ, *args, fallback=None, **kwargs):
        from typed.mods.types.atomic import Term
        if fallback is None:
            fallback = Term

        if not args and not kwargs:
            return typ
        if len(args) == 1 and isinstance(args[0], type) and not kwargs:
            target_cls = args[0]
            for name, attr in target_cls.__dict__.items():
                if callable(attr) and not name.startswith('_'):
                    if not getattr(attr, '__flags__', Flags()).is_action:
                        from typed.mods.err import TypeErr
                        raise TypeErr(
                            message=f"Method '{name}' in service '{target_cls.__name__}' must be decorated with @action"
                        )
            class Service(metaclass=SERVICE):
                __target__ = target_cls
                __flags__ = Flags(is_service=True)
                __fallback__ = fallback
            return Service
        from typed.mods.err import TypeErr
        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'SERVICE')}() expects a single class argument."
        )

class ENRICHED(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        return isterm(
            trm,
            getattr(typ, "__pure_type__", None)
        )

    def __getattr__(typ, name):
        service = getattr(
            typ,
            "__service__",
            None
        )
        if service is not None and hasattr(service, name):
            attr = getattr(service, name)
            _attr_flags = getattr(
                attr,
                "__flags__",
                None
            )
            if _attr_flags and getattr(
                _attr_flags,
                "is_action",
                False
            ):
                class BoundAction:
                    def __init__(self, action_inst, fallback):
                        self._action_inst = action_inst
                        self._fallback = fallback

                    def __call__(self, *args, **kwargs):
                        from typed.mods.func import action
                        prev = getattr(
                            action,
                            "_fallback_ctx",
                            None
                        )
                        action._fallback_ctx = self._fallback
                        try:
                            return self._action_inst(*args, **kwargs)
                        finally:
                            action._fallback_ctx = prev

                    def __getattr__(self, attr_name):
                        return getattr(self._action_inst, attr_name)

                pure_type = getattr(
                    typ,
                    "__pure_type__",
                    typ
                )
                return BoundAction(attr, pure_type)
            return attr

        display_name = getattr(
            typ,
            "__name__",
            "Enriched"
        )
        raise AttributeError(f"type object '{display_name}' has no attribute '{name}'")

    if TYPE_CHECKING:
        from typing import Type, TypeVar, Any
        T = TypeVar('T')
        S = TypeVar('S')
        def __call__(self, type: Type[T], service: Type[S], typesystem: Any=None) -> Type[S]:
            ...
    else:
        def __call__(met, type, service=None, typesystem=None):
            display_name = getattr(service, '__name__', 'Enriched')

            if getattr(service, '__fallback__', None) is Ellipsis:
                setattr(service, '__fallback__', type)

            class Enriched(metaclass=ENRICHED):
                __display__ = display_name
                __pure_type__ = type
                __service__ = service
                __kind__ = "enriched"
                __flags__ = Flags(is_enriched=True)
            Enriched.__name__ = display_name
            return Enriched
