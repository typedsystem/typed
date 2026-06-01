from typed.mods.loader import lazy, __typed__

__imports__ = {
    "typed.typesystem": None,
    "typed.meta":       None,
    "typed.types":      None,
    "typed.decorator":  None,
    "typed.check":      None,
    "typed.poly":       None
}

if lazy(__imports__):
    from typed.typesystem import *
    from typed.meta       import *
    from typed.types      import *
    from typed.decorator  import *
    from typed.check      import *
    from typed.poly       import *
