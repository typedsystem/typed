from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.logic": [
        "__DISCOURSE__", "Discourse",
        "__QUANTIFIER__", "Quantifier",
        "__EXPRESSION__", "Expression", "expression",
        "__EVALUATOR__", "Evaluator",
        "Predicate", "Reducer",
        "prod", "diag",
        "coprod", "codiag"
    ]
}

if lazy(__imports__):
    from typed.mods.logic import (
        __DISCOURSE__, Discourse,
        __QUANTIFIER__, Quantifier,
        __EXPRESSION__, Expression, expression,
        __EVALUATOR__, Evaluator,
        Predicate, Reducer,
        prod, diag,
        coprod, codiag
    )
