from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.err": [
        "notify", "iserr", "explode",
        "ERR", "Err",
        "NotDefined",
        "MissingErr",
        "FuncErr", "HintErr",
        "TypeErr", "CodErr", "DomErr",
        "ConfErr",
        "TypeSystemErr" 
    ]
}

if lazy(__imports__):
    from typed.mods.err import (
        notify, iserr, explode,
        ERR, Err,
        NotDefined,
        MissingErr,
        FuncErr, HintErr,
        TypeErr, CodErr, DomErr,
        ConfErr,
        TypeSystemErr
    )
