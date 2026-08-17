from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.meta.atomic": [
        "TYPE", "META",
        "EMPTY", "ANY", "TERM", "NILL",
        "INT", "FLOAT", "BOOL", "STR",
        "BYTE", "PATTERN",
        "ENUMERABLE", "FINITE",
        "MEMBER", "DOM", "COD"
    ],
    "typed.mods.meta.constructor": [
        "LIST", "TUPLE", "SET", "DICT",
        "EXTENSIONAL", "UNION", "INTER", "NOT_IN",
        "ALGEBRAIC", "PROD", "COPROD",
        "NULL", "MAYBE"
    ],
    "typed.mods.meta.dependent": [
        "RELATED", "SUBS", "SUPS", "SAME", "EQUIV",
        "BOUNDED", "HAS",
        "VALUES", "ENUM",
        "REGEX", 
        "FILTERED"
    ],
    "typed.mods.meta.func": [
        "CALLABLE", "CLASS", "METHOD", "LAMBDA",
        "FUNC", "DOM_FUNC", "COD_FUNC", "COMP_FUNC",
        "DOM_HINTED", "COD_HINTED", "HINTED",
        "COD_TYPED", "DOM_TYPED", "TYPED",
        "CONDITION", "FAMILY", "CONSTRUCTOR",
        "LAZY_TYPED", "LAZY_FUNC", "LAZY_HINTED",
        "LAZY_CONDITION", "LAZY_FAMILY", "LAZY_CONSTRUCTOR"
    ],
    "typed.mods.meta.service": [
        "ACTION", "SERVICE", "ENRICHED"
    ]
}

if lazy(__imports__):
    from typed.mods.meta.atomic import (
        TYPE, META,
        EMPTY, ANY, TERM, NILL,
        BYTE, PATTERN,
        INT, FLOAT, BOOL, STR,
        ENUMERABLE, FINITE,
        MEMBER, DOM, COD,
        LAZY
    )
    from typed.mods.meta.constructor import (
        LIST, TUPLE, SET, DICT,
        EXTENSIONAL, UNION, INTER, NOT_IN,
        ALGEBRAIC, PROD, COPROD,
        NULL, MAYBE
    )
    from typed.mods.meta.dependent import (
        RELATED, SUBS, SUPS, SAME, EQUIV,
        BOUNDED, HAS,
        VALUES, ENUM,
        REGEX,
        FILTERED
    )
    from typed.mods.meta.func import (
        CALLABLE, CLASS, METHOD, LAMBDA,
        FUNC, DOM_FUNC, COD_FUNC, COMP_FUNC,
        DOM_HINTED, COD_HINTED, HINTED,
        COD_TYPED, DOM_TYPED, TYPED,
        CONDITION, FAMILY, CONSTRUCTOR,
        LAZY_TYPED, LAZY_FUNC, LAZY_HINTED, 
        LAZY_CONDITION, LAZY_FAMILY, LAZY_CONSTRUCTOR
    )
    from typed.mods.meta.service import (
        ACTION, SERVICE, ENRICHED
    )
