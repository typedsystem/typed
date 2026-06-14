from typed.mods.loader import lazy, __typed__

__imports__ = {
    "typed.mods.init": [
        "TYPESYSTEM", "UNIVERSE", "ABSTRACT",
        "some", "every", "none", "only", "conf"
    ],
    "typed.mods.types": [
        "Type", "Meta", "Family", "Member",
        "Empty", "Any", "Nill",
        "Int", "Float", "Bool", "Str", "Byte",
        "Tuple", "List", "Set", "Dict",
        "Finite", "Enumerable", "Bounded",
        "Callable", "Func", "Typed",
        "Union", "Inter", "Prod", "Coprod",
        "Same", "Equiv", "Filtered"
    ],
    "typed.mods.err": [
        "NotDefined"
    ],
    "typed.mods.check": [
        "check", "true"
    ],
    "typed.mods.resolve": [
        "resolve"
    ],
    "typed.mods.func": [
        "func", "typed", "reduce", "compose"
    ],
    "typed.mods.flags": [
        "Flags", "flagged", "flag"
    ],
    "typed.mods.typesystem": [
        "new"
    ],
    "typed.mods.poly": [
        "prod", "coprod", "include", "join", "split"
    ],
    "typed.mods.prop": [
        "get", "set", "prop"
    ]
}

if lazy(__imports__):
    from typed.mods.init import (
        TYPESYSTEM, UNIVERSE, ABSTRACT,
        some, every, none, only, conf
    )
    from typed.mods.types import (
        Type, Meta, Family, Member, 
        Empty, Any, Nill,
        Int, Float, Bool, Str, Byte,
        Tuple, List, Set, Dict,
        Finite, Enumerable, Bounded,
        Callable, Func, Typed,
        Union, Inter, Prod, Coprod,
        Same, Equiv, Filtered
    )
    from typed.mods.err import (
        NotDefined
    )
    from typed.mods.check import (
        check, true
    )
    from typed.mods.resolve import (
        resolve
    )
    from typed.mods.func import (
        func, typed, reduce, compose
    )
    from typed.mods.flags import (
        Flags, flagged, flag
    )
    from typed.mods.typesystem import new
    from typed.mods.poly import (
        prod, coprod, include, join, split
    )
    from typed.mods.prop import get, set, has, prop
