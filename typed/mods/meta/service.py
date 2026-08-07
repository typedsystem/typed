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
            inst.__flags__ = Flags(
                is_func=True,
                is_action=True
            )
        return inst

    def term(typ, trm, type=None):
        from typed.mods.typesystem import term
        return term(
            value=trm,
            type=type
        )

class SERVICE(TYPE):
    def __getattr__(typ, name):
        target = getattr(typ, "__target__", None)
        if target is not None and hasattr(target, name):
            return getattr(target, name)
        raise AttributeError(f"type object '{getattr(typ, '__name__', 'Service')}' has no attribute '{name}'")

    def __call__(typ, *args, fallback=None, **kwargs):
        from typed.mods.types.atomic import Term
        from typed.mods.flags import flagged

        if fallback is None:
            fallback = Term

        if not args and not kwargs:
            return typ

        if len(args) == 1 and isinstance(args[0], type) and not kwargs:
            target_cls = args[0]
            for name, attr in target_cls.__dict__.items():
                if callable(attr) and not name.startswith('_'):
                    if not flagged(attr, 'is_action'):
                        from typed.mods.err import Err
                        raise Err(
                            message=f"Method '{name}' in service '{target_cls.__name__}' must be decorated with @action"
                        )

            class Service(metaclass=SERVICE):
                __target__ = target_cls
                __flags__ = Flags(is_service=True)
                __fallback__ = fallback

            Service.__name__ = getattr(target_cls, "__name__", "Service")
            Service.__display__ = Service.__name__
            return Service

        from typed.mods.err import Err
        raise Err(
            message=f"{getattr(typ, '__name__', 'SERVICE')}() expects a single class argument."
        )

class ENRICHED(TYPE):
    _meta_cache = {}

    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        return isterm(
            trm,
            getattr(
                typ,
                "__pure_type__",
                None
            )
        )

    def __issup__(typ, other):
        pure = getattr(
            typ,
            "__pure_type__",
            None
        )
        if pure is not None:
            from typed.mods.typesystem import issub
            return issub(other, pure)
        return False

    def __getattr__(typ, name):
        if name in ("__service__", "__pure_type__", "__kind__", "is_meta", "__flags__"):
            raise AttributeError(name)
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
            if _attr_flags and getattr(_attr_flags, "is_action", False):
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
                        setattr(
                            action,
                            "_fallback_ctx",
                            self._fallback
                        )
                        try:
                            return self._action_inst(*args, **kwargs)
                        finally:
                            setattr(
                                action,
                                "_fallback_ctx",
                                prev
                            )

                    def __getattr__(self, attr_name):
                        return getattr(self._action_inst, attr_name)

                return BoundAction(
                    action_inst=attr,
                    fallback=typ
                )
            return attr

        pure_type = getattr(
            typ,
            "__pure_type__",
            None
        )
        if pure_type is not None and hasattr(pure_type, name):
            return getattr(pure_type, name)

        display_name = getattr(
            typ,
            "__name__",
            "Enriched"
        )
        raise AttributeError(f"type object '{display_name}' has no attribute '{name}'")

    def __call__(met, type, service=None, typesystem=None):
        if getattr(type, "__kind__", None) == "enriched":
            type = getattr(
                type,
                "__pure_type__",
                type
            )
        display_name = getattr(
            service,
            '__name__',
            'Enriched'
        )
        if getattr(service, '__fallback__', None) is Ellipsis:
            setattr(
                service,
                '__fallback__',
                type
            )

        import builtins
        meta_of_met = builtins.type(met)
        pure_meta = builtins.type(type)

        if issubclass(meta_of_met, pure_meta):
            EnrichedMeta = meta_of_met
        elif issubclass(pure_meta, meta_of_met):
            EnrichedMeta = pure_meta
        else:
            meta_key = (meta_of_met, pure_meta)
            if meta_key not in ENRICHED._meta_cache:
                ENRICHED._meta_cache[meta_key] = builtins.type(
                    f"{meta_of_met.__name__}_{pure_meta.__name__}",
                    (meta_of_met, pure_meta),
                    {}
                )
            EnrichedMeta = ENRICHED._meta_cache[meta_key]

        from typed.mods.flags import Flags
        class Enriched(metaclass=EnrichedMeta):
            __display__ = display_name
            __pure_type__ = type
            __service__ = service
            __kind__ = "enriched"
            __flags__ = Flags(is_enriched=True)

        Enriched.__name__ = display_name

        if service is not None:
            setattr(
                service,
                '__fallback__',
                Enriched
            )
            target = getattr(
                service,
                "__target__",
                None
            )
            if target is not None:
                for name, attr in target.__dict__.items():
                    if callable(attr) and hasattr(attr, "__func__"):
                        annotations = getattr(
                            attr.__func__,
                            "__annotations__",
                            {}
                        )
                        if annotations.get("return") is Ellipsis:
                            annotations["return"] = Enriched
                    elif callable(attr):
                        annotations = getattr(
                            attr,
                            "__annotations__",
                            {}
                        )
                        if annotations.get("return") is Ellipsis:
                            annotations["return"] = Enriched

        return Enriched
