class __FLAGS__(type):
    pass

class Flags(metaclass=__FLAGS__):
    def __init__(
        self,
        is_discourse:  bool=False,
        is_reducer:    bool=False,
        is_predicate:  bool=False,
        is_evaluator:  bool=False,
        is_quantifier: bool=False,
        is_parametric: bool=False,
        is_expression: bool=False,
        is_dependent:  bool=False,
        is_algebraic:  bool=False,
        is_enumerable: bool=False,
        is_prod:       bool=False,
        is_coprod:     bool=False
    ):
        self.is_discourse  = is_discourse
        self.is_reduecer   = is_reducer
        self.is_predicate  = is_predicate
        self.is_parametric = is_parametric
        self.is_evaluator  = is_evaluator
        self.is_expression = is_expression
        self.is_quantifier = is_quantifier
        self.is_dependent  = is_dependent
        self.is_algebraic  = is_algebraic
        self.is_enumerable = is_enumerable
        self.is_prod       = is_prod
        self.is_coprod     = is_coprod

class flag:
    is_discourse  = "is_discourse"
    is_reducer    = "is_reducer"
    is_predicate  = "is_predicate"
    is_evaluator  = "is_evaluator"
    is_quantifier = "is_quantifier"
    is_parametric = "is_parametric"
    is_expression = "is_expression"
    is_dependent  = "is_dependent"
    is_enumerable = "is_enumerable"
    is_prod       = "is_prod"
    is_coprod     = "is_coprod"

def flagged(obj: object, *flags: tuple[str]) -> bool:
    return all(getattr(obj, f, False) for f in flags)
