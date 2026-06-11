from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.meta.atomic": [
        "TYPE", "META",
        "EMPTY", "ANY", "NILL",
        "INT", "FLOAT", "BOOL", "STR",
        "ENUMERABLE", "FINITE",
        "MEMBER", "DOM", "COD"
    ],
    "typed.mods.meta.constructor": [
        "LIST", "TUPLE", "SET", "DICT",
        "EXTENSIONAL", "UNION", "INTER", "NOT_IN",
        "ALGEBRAIC", "PROD", "COPROD"
    ],
    "typed.mods.meta.dependent": [
        "RELATED", "SUBS", "SUPS", "SAME", "EQUIV",
        "BOUNDED", "HAS",
        "FILTERED"
    ],
    "typed.mods.meta.func": [
        "CALLABLE", "CLASS", "METHOD", "LAMBDA",
        "FUNC", "DOM_FUNC", "COD_FUNC", "COMP_FUNC",
        "DOM_HINTED", "COD_HINTED", "HINTED",
        "COD_TYPED", "DOM_TYPED", "TYPED",
        "CONDITION", "FAMILY", "CONSTRUCTOR",
        "LAZY_TYPED"
    ]
}

if lazy(__imports__):
    from typed.mods.meta.atomic import (
        TYPE, META,
        EMPTY, ANY, NILL,
        INT, FLOAT, BOOL, STR,
        ENUMERABLE, FINITE,
        MEMBER, DOM, COD
    )
    from typed.mods.meta.constructor import (
        LIST, TUPLE, SET, DICT,
        EXTENSIONAL, UNION, INTER, NOT_IN,
        ALGEBRAIC, PROD, COPROD,
    )
    from typed.mods.meta.dependent import (
        RELATED, SUBS, SUPS, SAME, EQUIV,
        BOUNDED, HAS,
        FILTERED
    )
    from typed.mods.meta.func import (
        CALLABLE, CLASS, METHOD, LAMBDA,
        FUNC, DOM_FUNC, COD_FUNC, COMP_FUNC,
        DOM_HINTED, COD_HINTED, HINTED,
        COD_TYPED, DOM_TYPED, TYPED,
        CONDITION, FAMILY, CONSTRUCTOR,
        LAZY_TYPED
    )
