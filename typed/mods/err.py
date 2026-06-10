def notify(message, __notifier__=None, __multiline__=False, **kwargs) -> None:
    full_message = str(message)

    filtered_kwargs = {k: str(v) for k, v in kwargs.items() if v is not NotDefined}

    if filtered_kwargs:
        full_message = full_message.rstrip(":") + ":"

        if __multiline__:
            parts = [f"\n    {k}: {v}" for k, v in filtered_kwargs.items()]
            full_message += "".join(parts)
        else:
            parts = [f"{k}={v!r}" for k, v in filtered_kwargs.items()]
            full_message += " " + ", ".join(parts) + "."

    if __notifier__ is None:
        return full_message

    __notifier__(full_message)
    return None


class ERR(type):
    def __isterm__(typ, trm):
        from typed.mods.typesystem import issub, typeof
        return issub(typeof(trm), ERR) and issub(trm, Err)


class Err(BaseException, metaclass=ERR):
    __display__ = "Err"

    def __init__(self, message, **kwargs):
        __message__ = notify(message=message,  **kwargs)
        super().__init__(__message__)


def iserr(*errs: tuple, quantifier=None) -> bool:
    if quantifier is None:
        from typed.mods.init import some
        quantifier = some
    from typed.mods.logic import Quantifier
    if not isinstance(quantifier, Quantifier):
        raise TypeErr(
            term=quantifier,
            expected=Quantifier,
        )
    from typed.mods.typesystem import isterm
    return quantifier(isterm(err, ERR) for err in errs)


class NotDefined(Err, metaclass=ERR):
    __display__ = "NotDefined"


def explode(err: ERR, message=NotDefined, **kwargs: dict) -> None:
    return notify(message=message, __notifier__=err, **kwargs)


class MissingErr(Err, metaclass=ERR):
    __display__ = "MissingErr"

    def __init__(
        self,
        message='Missing something',
        details=NotDefined,
        where=NotDefined,
        what=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if where is NotDefined:
            raise MissingErr("Missing 'where' in 'MissingErr'.", where="MissingErr", what="where")

        if what is NotDefined:
            raise MissingErr("Missing 'what' in 'MissingErr'.", where="MissingErr", what="what")

        from typed.mods.typesystem import nameof

        if isinstance(what, (tuple, list, set)):
            what = tuple(nameof(x) for x in what)
        else:
            what = nameof(what)

        super().__init__(
            message=message,
            details=details,
            where=nameof(where),
            what=what,
            __multiline__=__multiline__,
            **kwargs
        )


class NotSatisfied(Err, metaclass=ERR):
    __display__ = "NotSatisfied"

    def __init__(
        self,
        message="Condition not safiesfied",
        details=NotDefined,
        condition=NotDefined,
        args=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if condition is NotDefined:
            raise MissingErr("Missing 'condition' in 'MissingErr'.")

        if args is NotDefined:
            raise MissingErr("Missing 'args' in 'MissingErr'.")

        from typed.mods.typesystem import nameof

        super().__init__(
            message=message,
            details=details,
            condition=nameof(condition),
            args=tuple(nameof(arg) for arg in args) if isinstance(args, tuple) else nameof(args),
            __multiline__=__multiline__,
            **kwargs
        )


class FuncErr(Err, metaclass=ERR):
    __display__ = "FuncErr"

    def __init__(
        self,
        message="Error in function",
        details=NotDefined,
        func=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if func is NotDefined:
            raise MissingErr(
                where=FuncErr,
                what=func
            )

        from typed.mods.typesystem import nameof

        super().__init__(
            message=message,
            details=details,
            func=nameof(func),
            __multiline__=__multiline__,
            **kwargs
        )


class HintErr(Err, metaclass=ERR):
    __display__ = "HintErr"

    def __init__(
        self,
        message="Missing type hint",
        details=NotDefined,
        func=NotDefined,
        term=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if all(x is NotDefined for x in (term, func)):
            raise MissingErr(
                where=HintErr,
                what=(term, func)
            )

        from typed.mods.typesystem import nameof

        if term is not NotDefined:
            term = nameof(term)

        if func is not NotDefined:
            func = nameof(func)

        if args is not NotDefined:
            if isinstance(args, tuple):
                args = tuple(nameof(a) for a in args)
            else:
                args = nameof(args)
            kwargs["args"] = args
        else:
            args = []

        if arg is not NotDefined:
            args.append(arg)

        super().__init__(
            message=message,
            details=details,
            func=func,
            term=term,
            args=args,
            __multiline__=__multiline__,
            **kwargs
        )


class TypeErr(Err, metaclass=ERR):
    __display__ = "TypeErr"

    def __init__(
        self,
        message="Wrong term type identified",
        details=NotDefined,
        func=NotDefined,
        term=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        quantifier=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if term is NotDefined:
            raise MissingErr(where=TypeErr, what="term")
        if expected is NotDefined:
            raise MissingErr(where=TypeErr, what="expected")

        from typed.mods.typesystem import nameof, typeof

        if func is not NotDefined:
            func = nameof(func)

        term_type = typeof(term)
        term_typesystems = getattr(term_type, "__typesystems__", [])

        if received is NotDefined:
            received = term_type

        if not term_typesystems:
            raise MissingErr(where=term_type, what="__typesystems__")

        if args is not NotDefined or arg is not NotDefined:
            message = "Wrong argument type identified"

            if args is not NotDefined:
                args = [nameof(x) for x in args]
            else:
                args = []

            if arg is not NotDefined:
                args.append(nameof(arg))

            if not isinstance(received, (tuple, set, list)) or len(received) != len(args):
                raise ValueError("'received' must be an iterable of the same length as 'args'.")
            if not isinstance(expected, (tuple, set, list)) or len(expected) != len(args):
                raise ValueError("'expected' must be an iterable of the same length as 'args'.")

            received = tuple(nameof(r) for r in received)
            expected = tuple(nameof(e) for e in expected)

            if len(args) == 1:
                args = args[0]
                received = received[0]
                expected = expected[0]
        else:
            if isinstance(received, (tuple, set, list)):
                received = tuple(nameof(r) for r in received)
                if len(received) == 1:
                    received = received[0]
            elif received is not NotDefined:
                received = nameof(received)

            if isinstance(expected, (tuple, set, list)):
                expected = tuple(nameof(e) for e in expected)
                if len(expected) == 1:
                    expected = expected[0]
            elif expected is not NotDefined:
                expected = nameof(expected)

        if quantifier is None:
            quantifier = NotDefined
        elif quantifier is not NotDefined:
            quantifier = nameof(quantifier)

        term = nameof(term)
        typesystems = ", ".join(nameof(t) for t in term_typesystems)

        super().__init__(
            message=message,
            details=details,
            func=func,
            term=term,
            args=args,
            received=received,
            expected=expected,
            quantifier=quantifier,
            __multiline__=__multiline__,
            **kwargs
        )

class DomErr(FuncErr, metaclass=ERR):
    __display__ = "DomErr"

    def __init__(
        self,
        message="Wrong domain type identified",
        details=NotDefined,
        func=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        quantifier=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        from typed.mods.typesystem import nameof
        if quantifier is None:
            quantifier = NotDefined
        elif quantifier is not NotDefined:
            quantifier = nameof(quantifier)

        super().__init__(
            message=message,
            details=details,
            func=func,
            arg=arg,
            args=args,
            received=received,
            expected=expected,
            quantifier=quantifier,
            __multiline__=__multiline__,
            **kwargs
        )


class CodErr(FuncErr, metaclass=ERR):
    __display__ = "CodErr"

    def __init__(
        self,
        message="Wrong codomain type identified",
        details=NotDefined,
        func=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        quantifier=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        from typed.mods.typesystem import nameof
        if quantifier is None:
            quantifier = NotDefined
        elif quantifier is not NotDefined:
            quantifier = nameof(quantifier)

        super().__init__(
            message=message, 
            details=details,
            func=func, 
            arg=arg,
            args=args, 
            received=received, 
            expected=expected,
            quantifier=quantifier,
            __multiline__=__multiline__,
            **kwargs
        )


class TypeSystemErr(Err, metaclass=ERR):
    __display__ = "TypeSystemErr"

    def __init__(
        self,
        message="Type is not in typesystem",
        details=NotDefined,
        type=NotDefined,
        types=NotDefined,
        typesystem=NotDefined,
        typesystems=NotDefined,
        quantifier=NotDefined,
        __multiline__=None,
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if all(x is NotDefined for x in (typesystem, typesystems)):
            raise MissingErr(
                where=TypeSystemErr,
                what=(typesystem, typesystems)
            )

        if all(x is NotDefined for x in (type, types)):
            raise MissingErr(
                where=TypeSystemErr,
                what=(type, types)
            )

        from typed.mods.typesystem import nameof

        if quantifier is None:
            quantifier = NotDefined
        elif quantifier is not NotDefined:
            quantifier = nameof(quantifier)

        if types is not NotDefined:
            if not isinstance(types, (tuple, list, set)):
                raise ValueError("'types' must be an iterable.")
            types = [nameof(t) for t in types]
        else:
            types = []

        if type is not NotDefined:
            types.append(nameof(type))

        super().__init__(
            message=message,
            details=details,
            types=types,
            typesystems=typesystems,
            quantifier=quantifier,
            __multiline__=__multiline__
        )


class ConfErr(Err, metaclass=ERR):
    __display__ = "ConfErr"

    def __init__(
        self,
        message='Wrong type in config',
        details=NotDefined,
        conf=NotDefined,
        arg=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        __multiline__=None,
        **kwargs
    ):
        from typed.mods.resolve import resolve
        __multiline__ = resolve.err.multiline(__multiline__)

        if conf is NotDefined:
            raise ValueError("Missing 'conf' in 'ConfErr'.")
        if arg is NotDefined:
            raise ValueError("Missing 'arg' in 'ConfErr'.")
        if received is NotDefined:
            raise ValueError("Missing 'received' in 'ConfErr'")
        if expected is NotDefined:
            raise ValueError("Missing 'expected' in 'ConfErr'")

        super().__init__(
            message=message,
            details=details,
            conf=conf,
            arg=arg,
            received=received,
            expected=expected,
            __multiline__=__multiline__,
            **kwargs
        )
