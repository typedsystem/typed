from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.conf": [
        "__CONF__",
        "Conf", "ErrConf", "LogicConf",
        "TypeSystemConf", "TypeCheckConf"
    ]
}

if lazy(__imports__):
    from typed.mods.conf import (
        __CONF__, 
        Conf, ErrConf, LogicConf,
        TypeSystemConf, TypeCheckConf
    )
