from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.types.base": [
        "Empty", "Any", "Nill",
        "Type", "Meta",
        "Enumerable", "Finite",
        "Bool", "Int", "Float",
        "Str", "Byte"
    ],
    "typed.mods.types.constructor": [
        "Tuple", "List", "Set", "Dict",
        "Extensional", "Union", "Inter", "NotIn",
        "Algebraic", "Prod", "Coprod"
    ],
    "typed.mods.types.dependent": [
        "Related", "Subs", "Sups", "Same", "Equiv", 
        "Filtered", "Bounded", "Has"
    ]
}

if lazy(__imports__):
    from typed.mods.types.base import ( 
        Empty, Any, Nill,
        Type, Meta,
        Enumerable, Finite,
        Bool, Int, Float,
        Str, Byte
    )
    from typed.mods.types.constructor import (
        Tuple, List, Set, Dict,
        Extensional, Union, Inter, NotIn,
        Algebraic, Prod, Coprod
    )
    from typed.mods.types.dependent import (
        Related, Subs, Sups, Same, Equiv,
        Filtered, Bounded, Has
    )
