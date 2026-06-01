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

class __QUANTIFIER__(type):
    """
    The independent metaclass for Quantifiers.
    """
    def __new__(mcls, name, bases, dct, order=None, count=None, **kwargs):
        cls = super().__new__(mcls, name, bases, dct, **kwargs)
        cls.__order__ = order
        cls.__count__ = count
        cls.is_quantifier_type = True
        return cls

    def __instancecheck__(cls, instance):
        if not getattr(instance, 'is_quantifier', False):
            return False

        expected_order = getattr(cls, "__order__", None)
        expected_count = getattr(cls, "__count__", None)

        if expected_order is not None and getattr(instance, "order", 1) != expected_order:
            return False
        if expected_count is not None and getattr(instance, "count", None) != expected_count:
            return False

        return True

    def __call__(cls, *args, **kwargs):
        is_parametric_call = (
            cls.__name__ == "Quantifier" and 
            not args and 
            ("order" in kwargs or "count" in kwargs) and
            "reducer" not in kwargs
        )

        if is_parametric_call:
            order = kwargs.get("order", 1)
            count = kwargs.get("count", None)

            name_parts = [f"order={order}"]
            if count is not None:
                name_parts.append(f"count={count}")

            name = f"Quantifier({', '.join(name_parts)})"

            return __QUANTIFIER__(name, (cls,), {
                "__display__": name,
            }, order=order, count=count)

        return super().__call__(*args, **kwargs)


class Quantifier(metaclass=__QUANTIFIER__):
    __display__ = "Quantifier"
    is_quantifier = True

    def __init__(self, reducer: 'Reducer', evaluator=None, order: int = None, count: int = None):
        from typed.mods.logic import Reducer, Evaluator
        if not isinstance(reducer, Reducer):
            from typed.mods.err import TypeErr
            raise TypeErr(
                term=self,
                arg=reducer,
                expected=Reducer,
                received=type(reducer)
            )

        if evaluator is None:
            evaluator = Evaluator

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
        self.order = order if order is not None else getattr(type(self), "__order__", 1)
        self.count = count if count is not None else getattr(type(self), "__count__", None)

    def __call__(self, *args):
        if len(args) == 1 and isinstance(args[0], int) and not isinstance(args[0], bool):
            n = args[0]
            try:
                res = self.reducer.func(n)
                if callable(res):
                    return type(self)(
                        reducer=type(self.reducer)(res),
                        order=self.order,
                        count=n
                    )
            except Exception:
                pass

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
