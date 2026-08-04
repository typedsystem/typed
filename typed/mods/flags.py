class __FLAGS__(type):
    pass

class Flags(metaclass=__FLAGS__):
    def __init__(
        self,
        is_discourse:   bool=False,
        is_reducer:     bool=False,
        is_predicate:   bool=False,
        is_evaluator:   bool=False,
        is_quantifier:  bool=False,
        is_parametric:  bool=False,
        is_expression:  bool=False,
        is_constructor: bool=False,
        is_dependent:   bool=False,
        is_algebraic:   bool=False,
        is_enumerable:  bool=False,
        is_finite:      bool=False,
        is_bounded:     bool=False,
        is_extensional: bool=False,
        is_prod:        bool=False,
        is_coprod:      bool=False,
        is_related:     bool=False,
        is_filtered:    bool=False,
        is_service:     bool=False,
        is_action:      bool=False,
        is_enriched:    bool=False,
        is_func:        bool=False,
        is_typed:       bool=False,
        is_hinted:      bool=False,
    
    ):
        self.is_discourse   = is_discourse
        self.is_reducer     = is_reducer
        self.is_predicate   = is_predicate
        self.is_parametric  = is_parametric
        self.is_evaluator   = is_evaluator
        self.is_expression  = is_expression
        self.is_quantifier  = is_quantifier
        self.is_constructor = is_constructor
        self.is_dependent   = is_dependent
        self.is_algebraic   = is_algebraic
        self.is_enumerable  = is_enumerable
        self.is_finite      = is_finite
        self.is_bounded     = is_bounded
        self.is_extensional = is_extensional
        self.is_prod        = is_prod
        self.is_coprod      = is_coprod
        self.is_related     = is_related
        self.is_filtered    = is_filtered
        self.is_service     = is_service
        self.is_action      = is_action
        self.is_enriched    = is_enriched
        self.is_func        = is_func
        self.is_hinted      = is_hinted
        self.is_typed       = is_typed

def flags(obj):
    d = getattr(
        obj,
        "__dict__",
        None
    )
    if d is not None and "__flags__" in d:
        f = d["__flags__"]
    else:
        f = getattr(
            obj,
            "__flags__",
            None
        )
    if f is None:
        from typed.helper.flags import EMPTY_FLAGS_PROXY
        return EMPTY_FLAGS_PROXY
    from typed.helper.flags import _FlagProxy
    return _FlagProxy(f)

def flagged(obj: object, *args: tuple[str]) -> bool:
    proxy = flags(obj)
    return all(getattr(proxy, arg) for arg in args)
