from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.func": [
        "Arg", "Signature",
        "args", "signature",
        "compose", "reduce", "hints"
    ]
}

if lazy(__imports__):
    from typed.mods.func import (
        Arg, Signature,
        args, signature,
        compose, reduce, hints
    )
