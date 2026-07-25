from typing import TYPE_CHECKING
from typed.mods.meta.atomic import TYPE
from typed.mods.flags import Flags
from typed.mods.meta.func import FUNC

class ACTION(FUNC):
    """
    The metatype of framework actions.
    Inherits from FUNC to allow partial hinting (e.g., unhinted 'self') 
    and forward references (like 'Path').
    """
    def __call__(typ, *args, **kwargs):
        if not args and not kwargs:
            return typ
        inst = super().__call__(*args, **kwargs)
        if hasattr(inst, '__flags__'):
            inst.__flags__.is_action = True
        else:
            inst.__flags__ = Flags(is_func=True, is_action=True)

        return inst


class SERVICE(TYPE):
    """
    The metatype of services.
    """
    def __call__(typ, *args, **kwargs):
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

            return Service

        from typed.mods.err import TypeErr
        raise TypeErr(
            message=f"{getattr(typ, '__name__', 'SERVICE')}() expects a single class argument."
        )

class ENRICHED(TYPE):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import isterm
        return isterm(trm, getattr(typ, "__pure_type__", None))

    if TYPE_CHECKING:
        from typing import Type, TypeVar,  Any
        T = TypeVar('T')
        S = TypeVar('S')
        def __call__(self, type: Type[T], service: Type[S], typesystem: Any=None) -> Type[S]:
            ...
    else:
        def __call__(met, type, service=None, typesystem=None):

            display_name = getattr(service, '__name__', 'Enriched')

            class Enriched(metaclass=ENRICHED):
                __display__ = display_name
                __pure_type__ = type
                __service__ = service
                __kind__ = "enriched"
                __flags__ = Flags(is_enriched=True)

            Enriched.__name__ = display_name
            return Enriched
