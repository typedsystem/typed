from typing import TYPE_CHECKING
from typed.mods.types.func import Func
from typed.mods.meta.service import SERVICE, ACTION, ENRICHED

class Service(metaclass=SERVICE):
    if TYPE_CHECKING:
        def __new__(cls, target_cls, **kwargs):
            ...

    def __getattr__(self, name):
        if name in ('__flags__', '__target__', 'is_service'):
            return super().__getattribute__(name)
        return getattr(self.__target__, name)

class Action(Func, metaclass=ACTION):
    if TYPE_CHECKING:
        def __new__(cls, *args, typesystem=None, check=None, defaults=None, envs=None, **kwargs):
            ...

from typing import TypeVar, Type
if TYPE_CHECKING:
    T = TypeVar('T')
    S = TypeVar('S')

class Enriched(metaclass=ENRICHED):
    if TYPE_CHECKING:
        def __new__(cls, type: Type[T], service: Type[S], **kwargs) -> Type[S]:
            ...

    def __getattr__(self, name):
        if name in ('__pure__', '__service__', '__flags__'):
            return super().__getattribute__(name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
