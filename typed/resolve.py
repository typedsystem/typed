from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.resolve": [
        "Resolver",
        "resolver",
        "resolve",
        "resolved"
    ]
}

if lazy(__imports__):
    from typed.mods.resolve import (
        Resolver, resolver, resolve, resolved
    )
