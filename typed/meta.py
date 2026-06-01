from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.meta.base": [
        "TYPE", "META",
        "EMPTY", "ANY", "NILL",
        "PARAMETRIC",
        "INT", "FLOAT", "BOOL", "STR",
        "LIST", "TUPLE", "SET", "DICT"
    ]
}

if lazy(__imports__):
    from typed.mods.meta.base import (
        TYPE, META,
        EMPTY, ANY, NILL,
        PARAMETRIC,
        INT, FLOAT, BOOL, STR,
        LIST, TUPLE, SET, DICT        
    )
