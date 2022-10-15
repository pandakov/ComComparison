"""
VIN team's project.

Main module for preparing data
"""

from typing import Callable, List

import numpy as np
import pandas as pd


class TextTransform:
    """

    Text transformation functions.

    Text transformation module with basic functions which
    used for building pipeline (class Pipe from this module).

    """

    @staticmethod
    def for_pipeline(func):
        def wrapper(*args, **kwargs):
            return func, args, kwargs

        return wrapper

    @staticmethod
    @for_pipeline
    def to_lower_case(s: str) -> str:
        return s.lower()

    @staticmethod
    @for_pipeline
    def drop_char(s: str, chars: str = ".,-", replace: str = "") -> str:
        for c in chars:
            s = s.replace(c, replace)
        return s

    @staticmethod
    @for_pipeline
    def drop_words(s: str, words: list[str]) -> str:
        s = " " + s + " "
        for w in words:
            s = s.replace(" " + w + " ", " ")
        return s.strip()

    @staticmethod
    @for_pipeline
    def drop_whitespaces(s: str) -> str:
        return " ".join(s.strip().split())


class Pipe:
    """

    Data pipeline class.

    Create pipelines for data preparing.

    """

    sequence: List[TextTransform]

    def __init__(self, *sequence):
        self.sequence = sequence

    def __call__(self, data: pd.Series, inline: bool = False) -> pd.Series:
        d = data if inline else data.copy()
        for s in self.sequence:
            # d = np.vectorize(s[0])(d, *s[1], **s[2])
            d = d.apply(s[0], *s[1], **s[2])
        return d

    def __repr__(self) -> str:
        r = [s[0].__name__ for s in self.sequence]
        return " -> ".join(r)

    def add2pipe(self, func: Callable, *args, **kwargs):
        return self.sequence.append(func, args, kwargs)


if __name__ == "__main__":
    data = np.eye(5)
    print(data)
