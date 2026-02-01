#!/usr/bin/env python3


class Renderer(object):
    """..."""
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def image(self) -> None:
        """..."""
        pass

    def rect(self) -> None:
        """..."""
        pass

    def text(self) -> None:
        """..."""
        pass
