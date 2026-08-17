from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.poly": [
        "Poly",
        "prod", "coprod",
        "join", "split"
    ]
}

if lazy(__imports__):
    from typed.mods.poly import (
        Poly,
        prod, coprod,
        include, join, split
    )
