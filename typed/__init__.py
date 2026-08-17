from typed.mods.loader import lazy, __typed__

__imports__ = {
    "typed.mods.init": [
        "TYPESYSTEM", "UNIVERSE", "ABSTRACT",
        "some", "every", "none", "only", "conf"
    ],
    "typed.types": [
        "Type", "Meta", "Family", "Member",
        "Empty", "Any", "Term", "Nill",
        "Int", "Float", "Bool", "Str", "Byte", "Pattern",
        "Tuple", "List", "Set", "Dict",
        "Finite", "Enumerable", "Bounded",
        "Null", "Maybe",
        "Callable", "Func", "Typed",
        "Union", "Inter", "Prod", "Coprod",
        "Same", "Equiv", "Filtered",
        "Values", "Enum", "Regex",
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
    "typed.wrap": [
        "func", "typed", "reduce", "compose",
        "service", "action", "enum"
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
        Empty, Any, Term, Nill,
        Int, Float, Bool, Str, Byte, Pattern,
        Tuple, List, Set, Dict,
        Finite, Enumerable, Bounded, Null, Maybe,
        Callable, Func, Typed,
        Union, Inter, Prod, Coprod, Values, Enum, Regex,
        Same, Equiv, Filtered, Enriched
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
    from typed.wrap import (
        func, typed, reduce, compose,
        service, action, enum
    )
    from typed.typesystem import new, term
    from typed.prop import prop
