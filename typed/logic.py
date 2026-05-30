from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.logic": [
        "__ENVALUATOR__", "Evaluator",
        "Reducer", "Quantifier"

    ]
}

if lazy(__imports__):
    from typed.mods.logic import (
        __EVALUATOR__, Evaluator,
        Reducer, Quantifier
    )
