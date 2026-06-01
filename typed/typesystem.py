from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.typesystem": [
        "__TYPESYSTEM__", "__ABSTRACT__", "__UNIVERSE__",
        "isterm", "issub", "issup",
        "nameof", "typeof", "typemap",
        "term", "trackof"

    ]
}

if lazy(__imports__):
    from typed.mods.typesystem import (
        __TYPESYSTEM__, __ABSTRACT__, __UNIVERSE__,
        isterm, issub, issup,
        nameof, typeof, typemap,
        term, trackof
    )
