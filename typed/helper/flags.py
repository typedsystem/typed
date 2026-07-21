class _FlagProxy:
    __slots__ = ('_f',)

    def __init__(self, f):
        self._f = f

    def __getattr__(self, name):
        if self._f is not None:
            return getattr(
                self._f,
                name,
                False
            )
        return False

EMPTY_FLAGS_PROXY = _FlagProxy(None)
