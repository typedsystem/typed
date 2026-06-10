from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.check": [
        "Checker", "checker",
        "check", "true"
    ]
}

if lazy(__imports__):
    from typed.mods.check import (
        Checker, checker,
        check, true
    )
