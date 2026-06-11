from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.types.atomic": [
        "Type", "Meta",
        "Empty", "Any", "Nill",
        "Int", "Float", "Boll", "Str",
        "Enumerable", "Finite",
        "Member", "Dom", "Cod"
    ],
    "typed.mods.types.constructor": [
        "List", "Tuple", "Set", "Dict",
        "Extensional", "Union", "Inter", "NotIn",
        "Algebraic", "Prod", "Coprod"
    ],
    "typed.mods.types.dependent": [
        "Related", "Subs", "Sups", "Same", "Equiv",
        "Bounded", "Has",
        "Filtered"
    ],
    "typed.mods.types.func": [
        "Callable", "Class", "Method", "Lambda",
        "Func", "DomFunc", "CodFunc", "CompFunc",
        "DomHinted", "CodHinted", "Hinted",
        "DomTyped", "CodTyped", "Typed",
        "Condition", "Family", "Constructor",
        "LazyTyped"
    ]
}

if lazy(__imports__):
    from typed.mods.types.atomic import (
        Type, Meta,
        Empty, Any, Nill,
        Int, Float, Boll, Str,
        Enumerable, Finite,
        Member, Dom, Cod 
    )
    from typed.mods.types.constructor import (
        List, Tuple, Set, Dict,
        Extensional, Union, Inter, NotIn,
        Algebraic, Prod, Coprod 
    )
    from typed.mods.types.dependent import (
        Related, Subs, Sups, Same, Equiv,
        Bounded, Has,
        Filtered 
    )
    from typed.mods.types.func import (
        Callable, Class, Method, Lambda,
        Func, DomFunc, CodFunc, CompFunc,
        DomHinted, CodHinted, Hinted,
        DomTyped, CodTyped, Typed,
        Condition, Family, Constructor,
        LazyTyped 
    )
