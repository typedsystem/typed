from typed.mods.loader import lazy

__imports__ = {
    "typed.mods.typesystem": [


    ]
}

if lazy(__imports__):
    from typed.mods.typesystem
