from typed.mods.loader import lazy, __typed__

__imports__ = {
    "typed.mods.init": [
        "TYPESYSTEM", "UNIVERSE", "ABSTRACT",
        "some", "every", "none", "only", "conf"
    ],
    "typed.types": [
        "Type", "Meta", "Family", "Member",
        "Empty", "Any", "Nill",
        "Int", "Float", "Bool", "Str", "Byte",
        "Tuple", "List", "Set", "Dict",
        "Finite", "Enumerable", "Bounded",
        "Callable", "Func", "Typed",
        "Union", "Inter", "Prod", "Coprod",
        "Same", "Equiv", "Filtered",
        "Enriched"
    ],
    "typed.err": [
        "NotDefined"
    ],
    "typed.checker": [
        "check", "require"
    ],
    "typed.resolve": [
        "resolve"
    ],
    "typed.func": [
        "func", "typed", "reduce", "compose",
        "service", "action"
    ],
    "typed.typesystem": [
        "new", "term"
    ],
    "typed.prop": [
        "get", "set", "prop"
    ]
}

if lazy(__imports__):
    from typed.mods.init import (
        TYPESYSTEM, UNIVERSE, ABSTRACT,
        some, every, none, only, conf
    )
    from typed.types import (
        Type, Meta, Family, Member, 
        Empty, Any, Nill,
        Int, Float, Bool, Str, Byte,
        Tuple, List, Set, Dict,
        Finite, Enumerable, Bounded,
        Callable, Func, Typed,
        Union, Inter, Prod, Coprod,
        Same, Equiv, Filtered
    )
    from typed.err import (
        NotDefined
    )
    from typed.checker import (
        check, require
    )
    from typed.resolve import (
        resolve
    )
    from typed.func import (
        func, typed, reduce, compose
    )
    from typed.typesystem import new, term
    from typed.prop import get, set, prop
