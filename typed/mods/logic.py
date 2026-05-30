class __EVALUATOR__(type):
    """
    The metaclass of evaluator classes.
    """
    def __new__(mcls, name, bases, dct, **kwargs):
        if dct is None:
            dct = {}

        if not 'eval' in dct and not any(hasattr(base, 'eval') for base in bases):
            from typed.mods.err import MissingErr
            raise MissingErr(
                details="method not found",
                where=name,
                what='eval'
            )

        ops = {
            '__eq__': lambda v, other: v == other,
            '__ne__': lambda v, other: v != other,
            '__lt__': lambda v, other: v < other,
            '__le__': lambda v, other: v <= other,
            '__gt__': lambda v, other: v > other,
            '__ge__': lambda v, other: v >= other,
        }

        for magic, op in ops.items():
            if magic not in dct and not any(hasattr(base, magic) for base in bases):
                def __op__(op):
                    return lambda self, other: self.eval(lambda v: op(v, other))
                dct[magic] = __op__(op)

        if '__contains__' not in dct and not any(hasattr(b, '__contains__') for b in bases):
            dct['__contains__'] = lambda self, item: self.eval(lambda v: item in v)

        if '__getattr__' not in dct and not any(hasattr(b, '__getattr__') for b in bases):
            def __getattr__(self, attr_name):
                def proxy(*args, **kwargs):
                    return self.eval(lambda v: getattr(v, attr_name)(*args, **kwargs))
                return proxy

            dct['__getattr__'] = __getattr__

        dct['is_evaluator'] = True

        return super().__new__(mcls, name, bases, dct, **kwargs)

class Reducer:
    """
    The class of reducers.
    """
    __display__ = "Reducer"
    is_reducer = True

    def __init__(self, func):
        if not callable(func):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=self,
                arg=func,
                expected=callable,
                received=type(func)
            )
        self.func = func

    def __call__(self, iterable):
        from collections.abc import Iterable

        if not isinstance(iterable, Iterable):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=self.fn,
                arg=iterable,
                expected=Iterable,
                received=type(iterable)
            )
        return self.func(iterable)

class Evaluator(metaclass=__EVALUATOR__):
    __display__ = "Evaluator"

    def __init__(self, values, reducer):
        if not isinstance(reducer, Reducer):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=self,
                arg=reducer,
                expected=Reducer,
                received=type(reducer)
            )
        self.values = values
        self.reducer = reducer

    def eval(self, op):
        def __eval__():
            yielded_count = 0
            first_error = None
            for value in self.values:
                try:
                    res = op(value)
                    yielded_count += 1
                    yield res
                except Exception as e:
                    if first_error is None:
                        first_error = e

            if yielded_count == 0 and first_error is not None:
                raise first_error

        return self.reducer(__eval__())

class Quantifier:
    __display__ = "Quantifier"
    is_quantifier = True

    def __init__(self, reducer: Reducer, evaluator: __EVALUATOR__=None):
        if not isinstance(reducer, Reducer):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=self,
                arg=reducer,
                expected=Reducer,
                received=type(reducer)
            )

        if evaluator is None: evaluator = Evaluator

        if not issubclass(type(evaluator), __EVALUATOR__):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=self,
                arg=evaluator,
                expected=__EVALUATOR__,
                received=type(evaluator)
            )

        self.reducer = reducer
        self.evaluator = evaluator

    def __call__(self, *args):
        def __flatten__(items):
            for item in items:
                if hasattr(item, '__iter__') and not isinstance(item, (str, bytes)):
                    yield from __flatten__(item)
                else:
                    yield item

        values = tuple(__flatten__(args))

        if all(isinstance(v, bool) for v in values):
            return self.reducer(values)

        return self.evaluator(values, self.reducer)

    def __contains__(self, instance):
        return isinstance(instance, type(self))
