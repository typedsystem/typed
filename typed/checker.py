from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.check": [
        "__CHECKER__",
        "Checker", "TypedChecker",
        "check", "require",
        "typecheck"
    ]
}

if lazy(__imports__):
    from typed.mods.check import (
        __CHECKER__, 
        Checker, TypedChecker,
        check, require,
        typecheck
    )
