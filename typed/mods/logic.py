class __DISCOURSE__(type):
    def __instancecheck__(cls, instance):
        try:
            iter(instance)
            return True
        except TypeError:
            return False

    def __contains__(cls, instance):
        return cls.__instancecheck__(instance)

class Discourse(metaclass=__DISCOURSE__):
    __display__ = "Discourse"

    def __init__(self, individuals):
        from typed.mods.flags import Flags
        self.__flags__ = Flags(is_discourse=True)

        if type(individuals) is Discourse:
            self.individuals = individuals.individuals
        else:
            try:
                iter(individuals)
                self.individuals = individuals
            except TypeError:
                from typed.mods.err import TypeErr
                raise TypeErr(term=self, arg=individuals, expected="Iterable", received=type(individuals))

    def __iter__(self):
        return iter(self.individuals)

    def slice(self, start=None, stop=None, step=None):
        from itertools import islice
        return Discourse(islice(self.individuals, start, stop, step))

    def __getitem__(self, item):
        if isinstance(item, slice):
            return self.slice(item.start, item.stop, item.step)
        elif isinstance(item, int):
            from itertools import islice
            try:
                return next(islice(self.individuals, item, item + 1))
            except StopIteration:
                raise IndexError("Discourse index out of range.")
        else:
            raise TypeError("Discourse indices must be integers or slices.")

    def __len__(self):
        from typed.mods.err import NotDefined
        if hasattr(self.individuals, "__len__"):
            return len(self.individuals)
        return NotDefined

    def prod(self, *discourses, limit: int=-1):
        return prod(self, *discourses, limit=limit)

    def diag(self, *discourses, limit: int=-1):
        return diag(self, *discourses, limit=limit)

    def coprod(self, *discourses, limit: int=-1):
        return coprod(self, *discourses, limit=limit)

def prod(*discourses, limit: int = -1):
    from typed.mods.logic import Discourse
    from typed.mods.check import require
    from itertools import islice

    require.every.isinstance(discourses, Discourse)

    zipped_iterator = zip(*discourses, strict=True)

    if limit > 0:
        yield from islice(zipped_iterator, limit)
    else:
        yield from zipped_iterator

def diag(*discourses, limit: int = -1):
    from typed.mods.logic import Discourse
    from typed.mods.check import require
    from itertools import islice

    require.every.isinstance(discourses, Discourse)
    yielded_count = 0

    for i, discourse in enumerate(discourses):
        if 0 < limit <= yielded_count:
            break
        iterator = iter(discourse)
        diagonal_element = list(islice(iterator, i, i + 1))

        if not diagonal_element:
            raise ValueError(f"Discourse at index {i} is too short to form a complete diagonal.")

        yield diagonal_element[0]
        yielded_count += 1

def coprod(*discourses, limit: int = -1):
    from typed.mods.logic import Discourse
    from typed.mods.check import require
    from itertools import islice

    require.every.isinstance(discourses, Discourse)

    def __coprod__():
        for i, discourse in enumerate(discourses):
            for x in discourse:
                yield (i, x)

    if limit > 0:
        yield from islice(__coprod__(), limit)
    else:
        yield from __coprod__()

def codiag(trm, discourse):
    try:
        i, x = trm
        if isinstance(i, int) and 0 <= i < len(discourse):
            yield (x, discourse[i])
    except (TypeError, ValueError):
        pass

class Reducer:
    """
    The class of reducers.
    """
    __display__ = "Reducer"

    def __init__(self, func):
        if not callable(func):
            from typed.mods.err import TypeErr
            raise TypeErr(term=func, expected=("callable",), received=(type(func),))

        self.func = func

        from typed.mods.flags import Flags
        self.__flags__ = Flags(is_reducer=True)

    def __call__(self, discourse):
        if not isinstance(discourse, Discourse):
            from typed.mods.err import TypeErr
            raise TypeErr(term=discourse, expected=(Discourse,), received=(type(discourse),))

        return self.func(discourse)

class __QUANTIFIER__(type):
    """
    The metaclass of quantifier classes.
    """
    def __new__(mcls, name, bases, dct, order=None, count=None, **kwargs):
        cls = super().__new__(mcls, name, bases, dct, **kwargs)
        cls.__order__ = order
        cls.__count__ = count
        return cls

    def __instancecheck__(cls, instance):
        flags = getattr(instance, '__flags__', None)
        if flags is None or not flags.is_quantifier:
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

    def __init__(self: __QUANTIFIER__, reducer: Reducer, evaluator: '__EVALUATOR__'=None, order: int=None, count: int=None):
        if not isinstance(reducer, Reducer):
            from typed.mods.err import TypeErr
            raise TypeErr(term=reducer, expected=(Reducer,), received=(type(reducer),))

        if evaluator is None:
            evaluator = Evaluator

        if not isinstance(evaluator, type):
            from typed.mods.err import TypeErr
            raise TypeErr(term=evaluator, expected=(type,), received=(type(evaluator),))

        if not isinstance(evaluator, __EVALUATOR__):
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

        from typed.mods.flags import Flags
        self.__flags__ = Flags(is_quantifier=True)

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

        if all(isinstance(v, bool) or getattr(v, '__name__', '') == 'NotDefined' or v is None for v in values):
            bool_values = tuple(v if isinstance(v, bool) else False for v in values)
            return self.reducer(Discourse(bool_values))

        return self.evaluator(values, self.reducer, quantifier=self)

    def __contains__(self, instance):
        return isinstance(instance, type(self))

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
                def __op__(op_func):
                    def method(self, other):
                        from typed.mods.logic import Expression
                        return Expression(
                            discourse=self.values,
                            predicate=lambda v: op_func(v, other),
                            quantifier=self.quantifier
                        )
                    return method
                dct[magic] = __op__(op)

        if '__contains__' not in dct and not any(hasattr(b, '__contains__') for b in bases):
            def __contains__(self, item):
                from typed.mods.logic import Expression
                return Expression(
                    discourse=self.values,
                    predicate=lambda v: item in v,
                    quantifier=self.quantifier
                )
            dct['__contains__'] = __contains__

        if '__getattr__' not in dct and not any(hasattr(b, '__getattr__') for b in bases):
            def __getattr__(self, attr_name):
                def proxy(*args, **kwargs):
                    from typed.mods.logic import Expression
                    return Expression(
                        discourse=self.values,
                        predicate=lambda v: getattr(v, attr_name)(*args, **kwargs),
                        quantifier=self.quantifier
                    )
                return proxy
            dct['__getattr__'] = __getattr__

        dct['is_evaluator'] = True

        return super().__new__(mcls, name, bases, dct, **kwargs)


class Evaluator(metaclass=__EVALUATOR__):
    __display__ = "Evaluator"

    def __init__(self, values, reducer, quantifier=None):
        if not isinstance(reducer, Reducer):
            from typed.mods.err import TypeErr
            raise TypeErr(term=reducer, expected=(Reducer,), received=(type(reducer),))

        self.values = values
        self.reducer = reducer
        self.quantifier = quantifier

        from typed.mods.flags import Flags
        self.__flags__ = Flags(is_evaluator=True)

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

        return self.reducer(Discourse(__eval__()))

    def __bool__(self) -> bool:
        return bool(self.eval(bool))

class Predicate:
    __display__ = "Predicate"

    def __init__(self, func: callable):
        flags = getattr(func, '__flags__', None)
        if flags is not None and flags.is_predicate:
            self.func = getattr(func, 'func', func)
            self.__name__ = getattr(func, '__name__', 'predicate')
        else:
            if not callable(func):
                from typed.mods.err import TypeErr
                raise TypeErr(term=func, expected=("callable",), received=(type(func),))

            self.func = func
            self.__name__ = getattr(func, '__name__', 'predicate')

            from typed.mods.flags import Flags
            self.__flags__ = Flags(is_predicate=True)

    def __call__(self, *args, **kwargs) -> bool:
        return bool(self.func(*args, **kwargs))

class __EXPRESSION__(type):
    """
    The metaclass for logical expressions.
    """
    def __instancecheck__(cls, instance):
        return issubclass(type(type(instance)), __EXPRESSION__)

class Expression(metaclass=__EXPRESSION__):
    __display__ = "Expression"

    def __init__(
        self,
        discourse:  Discourse, 
        predicate:  Predicate, 
        quantifier: Quantifier,
        func:       callable=None,
        evaluator:  __EVALUATOR__=None
    ):
        if not isinstance(discourse, Discourse):
            discourse = Discourse(discourse)

        if not isinstance(predicate, Predicate):
            predicate = Predicate(predicate)

        from typed.mods.resolve import resolve
        quantifier = resolve.logic.quantifier(quantifier)

        if func is None:
            func = lambda *args: args

        if not callable(func):
            from typed.mods.err import TypeErr
            raise TypeErr(term=func, expected=("callable",), received=(type(func),))

        if evaluator is None:
            evaluator = quantifier.evaluator

        if not isinstance(evaluator, __EVALUATOR__):
            from typed.mods.err import TypeErr
            raise TypeErr(term=evaluator, expected=__EVALUATOR__, received=type(evaluator)) 

        self.discourse = discourse
        self.predicate = predicate
        self.quantifier = quantifier
        self.func = func
        self.evaluator = evaluator
        self.__name__ = getattr(func, '__name__', 'expression') if func else 'expression'

        from typed.mods.flags import Flags
        self.__flags__ = Flags(is_expression=True)

    def __call__(self) -> bool:
        if self.evaluator is not None:
            q_type = type(self.quantifier)
            engine = q_type(
                reducer=self.quantifier.reducer,
                evaluator=self.evaluator,
                order=self.quantifier.order,
                count=self.quantifier.count
            )(*self.discourse)
        else:
            engine = self.quantifier(*self.discourse)

        if isinstance(engine, bool):
            return engine

        if self.func is not None:
            op = lambda x: self.predicate(self.func(x))
        else:
            op = self.predicate

        return bool(engine.eval(op))

    def __bool__(self) -> bool:
        return self()

def expression(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.__name__ = getattr(func, '__name__', 'expression')
    wrapper.__qualname__ = getattr(func, '__qualname__', 'expression')
    wrapper.__doc__ = getattr(func, '__doc__', None)
    wrapper.__module__ = getattr(func, '__module__', None)

    from typed.mods.flags import Flags
    wrapper.__flags__ = Flags(is_expression=True)
    return wrapper
