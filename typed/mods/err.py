def notify(message, notifier=None, __multiline__=False, **kwargs):
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

    if notifier is NotDefined:
        return full_message

    if isinstance(notifier, type) and issubclass(notifier, BaseException):
        raise notifier(full_message)

    notifier(full_message)
    return None

class Err(BaseException):
    __display__ = "Err"

    def __init__(self, message, **kwargs):
        __message__ = notify(message=message, **kwargs)
        super().__init__(__message__)

class NotDefined(Err):
    __display__ = "NotDefined"

class Anonymous(Err):
    __display__ = "Anonymous"

class MissingErr(Err):
    __display__ = "MissingErr"

    def __init__(
        self,
        message='Missing something.',
        where=NotDefined,
        what=NotDefined,
        __multiline__=True,
        **kwargs
    ):
        if where is NotDefined:
            raise MissingErr("Missing 'where' in 'MissingErr'.")

        if what is NotDefined:
            raise MissingErr("Missing 'what' in 'MissingErr'.")

        from typed.mods.core import name

        if isinstance(what, (tuple, list, set)):
            what = tuple(name(x) for x in what)
        else:
            what = name(what)

        super().__init__(
            message=message,
            where=name(where),
            what=what,
            **kwargs
        )

class FuncErr(Err):

    __display__ = "FuncErr"

    def __init__(
        self,
        message="Error in function",
        details=NotDefined,
        func=NotDefined,
        __multiline__=True,
        **kwargs
    ):
        if func is NotDefined:
            raise MissingErr(
                where=FuncErr,
                what=func
            )

        from typed.mods.core import name
        func = name(func)

        super().__init__(
            message=message,
            details=details,
            func=func,
            **kwargs
        )

class HintErr(Err):
    __display__ = "HintErr"

    def __init__(
        self,
        message="Missing type hint",
        details=NotDefined,
        func=NotDefined,
        term=NotDefined,
        args=NotDefined,
        __multiline__=True,
        **kwargs
    ):
        if term is NotDefined:
            raise ValueError("Missing 'term' in 'HintErr'.")

        from typed.mods.core import name
        term = name(term)

        if args is not NotDefined:
            if isinstance(args, tuple):
                args = tuple(name(a) for a in args)
            else:
                args = name(args)
            kwargs["args"] = args

        super().__init__(
            message=message,
            details=details,
            func=func,
            term=term,
            args=args,
            __multiline__=__multiline__,
            **kwargs
        )

class TypeErr(Err):
    __display__ = "TypeErr"

    def __init__(
        self,
        message="Wrong term type identified",
        details=NotDefined,
        term=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        **kwargs
    ):
        if term is NotDefined:
            raise ValueError("Missing 'term' in 'TypeErr'.")
        if received is NotDefined:
            raise ValueError("Missing 'received' in 'TypeErr'")
        if expected is NotDefined:
            raise ValueError("Missing 'expected' in 'TypeErr'")

        from typed.mods.core import name, type

        term_type = type(term)
        term_typesystems = getattr(term_type, "__typesystems__", [])

        if not term_typesystems:
            raise AttributeError(f"The term '{name(term)}' has a type '{name(term_type)}' with no defined typesystem.")

        if args or arg is not NotDefined:
            message = "Wrong argument type identified"
            args = [name(x) for x in args]
            if arg is not NotDefined:
                args.extend(name(arg))

            if not isinstance(received, (tuple, set, list)) or len(received) != len(args):
                raise ValueError("'received' must be an iterable of the same length as 'args'.")
            if not isinstance(expected, (tuple, set, list)) or len(expected) != len(args):
                raise ValueError("'expected' must be an iterable of the same length as 'args'.")

            received = tuple(name(r) for r in received)
            expected = tuple(name(e) for e in expected)

            if len(args) == 1:
                args = args[0]
                received = received[0]
                expected = expected[0]

        term = name(term)
        typesystems = ", ".join(name(t) for t in term_typesystems)

        kwargs.setdefault("__multiline__", True)

        super().__init__(
            message=message,
            term=term,
            args=args,
            received=received,
            expected=expected,
            **kwargs
        )

class DomErr(TypeErr):
    __display__ = "DomErr"

    def __init__(
        self,
        message="Wrong domain type identified",
        term=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        **kwargs
    ):
        super().__init__(
            message=message,
            term=term,
            arg=arg,
            args=args,
            received=received,
            expected=expected,
            **kwargs
        )

class CodErr(TypeErr):
    __display__ = "CodErr"
    def __init__(
        self,
        message="Wrong codomain type identified",
        term=NotDefined,
        arg=NotDefined,
        args=NotDefined,
        received=NotDefined,
        expected=NotDefined,
        **kwargs
    ):
        super().__init__(
            message=message, 
            term=term, 
            arg=arg,
            args=args, 
            received=received, 
            expected=expected, 
            **kwargs
        )

class TypeSystemErr(Err):
    __display__ = "TypeSystemErr"

    def __init__(
        self,
        message="Type is not in typesystem",
        type=NotDefined,
        types=NotDefined,
        typesystem=NotDefined
    ):
        if typesystem is NotDefined:
            from typed.mods.init import TYPESYSTEM
            typesystem = TYPESYSTEM

        if type is NotDefined and types is NotDefined:
            raise ValueError("Missing 'type' in 'TypeSystemErr'.")

        from typed.mods.core import name
        if types is not NotDefined:
            if not isinstance(types, (tuple, list, set)):
                raise ValueError("'types' must be an iterable.")

            types = [name(t) for t in types]
        else:
            types = []

        if type is not NotDefined:
            types.append(name(type))

        super().__init__(
            message=message,
            types=types,
            typesystem=typesystem            
        )

class ConfErr(Err):
    __display__ = "ConfErr"
    def __init__(
        self,
        message='Wrong type in config',
        conf=NotDefined,
        arg=NotDefined,
        received=NotDefined,
        expected=NotDefined
    ):
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
            conf=conf,
            arg=arg,
            received=received,
            expected=expected
        )
