import shiny.express as _se


class _InputProxy:
    """Resolve to the current session's input at call time, not import time."""

    def __getattr__(self, name: str):
        return getattr(_se.input, name)


input = _InputProxy()
