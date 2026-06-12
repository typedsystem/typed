
def _reduce_args(sig_args, *args, **kwargs):
    from typed.mods.err import NotDefined
    arguments = {}
    for i, arg in enumerate(sig_args):
        if i < len(args):
            arguments[arg.name] = args[i]
        elif arg.name in kwargs:
            arguments[arg.name] = kwargs[arg.name]
        elif arg.default is not NotDefined:
            arguments[arg.name] = arg.default
    return arguments

def _repr_arg(x):
    if x is Ellipsis: return "..."
    return repr(x)
