from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.flags": [
        "__FLAGS__",
        "Flags",
        "flag",
        "flagged",
        "flags"
    ]
}


if lazy(__imports__):
    from typed.mods.flags import (
        __FLAGS__, Flags, flag, flags, flagged
    )
