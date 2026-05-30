class Checker:
    def __init__(self, func: callable, name: str=None):
        self.func = func
        self.__name__ = name if name is not None else func.__name__
        self.__display__ = self.__name__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def checker(func: callable, name: str=None) -> staticmethod: 
    return staticmethod(Checker(func=func, name=name))

class check:
    @checker
    def isinstance(obj: object, cls: type) -> bool:
        from typed.mods.err import TypeErr
        if not isinstance(obj, cls):
            raise TypeErr(
                term=obj,
                expected=cls,
                received=type(obj)
            )
        return True

    @checker
    def isterm(term: object, type: type) -> bool:
        from typed.mods.err import TypeErr
        from typed.mods.typesystem import isterm, typeof
        if not isterm(term, type):
            raise TypeErr(
                term=term,
                expected=type,
                received=typeof(term)
            )
        return True
