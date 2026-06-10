from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.init": [
        "TYPESYSTEM", "UNIVERSE", "ABSTRACT",
        "conf", "some", "every", "none", "true", "false"
    ]
}

if lazy(__imports__):
    from typed.mods.init import (
        SAMENESS, STATEFUL, MAGIC,
        TYPESYSTEM, UNIVERSE, ABSTRACT,
        conf,
        some, every, none, true, false
    )
