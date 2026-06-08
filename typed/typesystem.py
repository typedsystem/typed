from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.typesystem": [
        "__SAMENESS__",
        "__ABSTRACT__",
        "__UNIVERSE__",
        "__TYPESYSTEM__",
        "isentity", "iscongruent", "iscognate",
        "isuniverse", "isabstract", "ismeta", "istype", "ismember",
        "isterm", "issub", "issup", "issame", "isequiv",
        "nameof", "typeof", "kindof", "trackof",
        "term", "typemap",
        "new"
    ]
}

if lazy(__imports__):
    from typed.mods.typesystem import (
        __SAMENESS__,
        __ABSTRACT__,
        __UNIVERSE__,
        __TYPESYSTEM__,
        isentity, iscongruent, iscognate,
        isuniverse, isabstract, ismeta, istype, ismember,
        isterm, issub, issup, issame, isequiv,
        nameof, typeof, kindof, trackof,
        term, typemap,
        new
    )
