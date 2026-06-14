from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.prop": [
        "set", "get", "prop"
    ]
}


if lazy(__imports__):
    from typed.mods.prop import (
        set, get, prop
    )
