from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.poly": [
        "Poly", "poly",
        "prod", "coprod",
        "join", "split",
        "flatten", "unflatten",
        "include", "remove",
        "parse", "serialize"
    ]
}

if lazy(__imports__):
    from typed.mods.poly import (
        Poly, poly,
        prod, coprod,
        join, split,
        flatten, unflatten,
        include, remove,
        parse, serialize
    )
