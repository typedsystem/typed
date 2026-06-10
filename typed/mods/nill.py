from functools import lru_cache as cache
from typed.mods.types.atomic import Nill, Bool, Type

@cache
class nill:
    def func():
        return None

    class cls:
        def nill(self):
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

    def family(x: Nill) -> Type:
        return Nill

    def constructor(x: Type) -> Type:
        return Nill
