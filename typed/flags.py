from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.flags": [
        "Flags",
        "flag",
        "flagged"
    ]
}


if lazy(__imports__):
    from typed.mods.flags import (
        Flags, flag, flagged
    )
