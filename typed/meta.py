from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.meta": [
        ""
    ]
}

if lazy(__imports__):
    from typed.mods.meta.base import (
        TYPE, META, 
        
        
    )
