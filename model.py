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

    @for_pipeline
    def to_lower_case(s: str) -> str:
        return s.lower()

    @for_pipeline
    def drop_char(s: str, chars: str = r".,()0123456789«»", replace: str = "") -> str:
        for c in chars:
            s = s.replace(c, replace)
        return s

    @for_pipeline
    def drop_words(s: str, words: list[str]) -> str:
        s = " " + s + " "
        for w in words:
            s = s.replace(" " + w + " ", " ")
        return s.strip()

    @for_pipeline
    def drop_whitespaces(s: str) -> str:
        return " ".join(s.strip().split())

    @for_pipeline
    def transliterate(string: str) -> str:
        capital_letters = {
            "А": "A",
            "Б": "B",
            "В": "V",
            "Г": "G",
            "Д": "D",
            "Е": "E",
            "Ё": "E",
            "З": "Z",
            "И": "I",
            "Й": "Y",
            "К": "K",
            "Л": "L",
            "М": "M",
            "Н": "N",
            "О": "O",
            "П": "P",
            "Р": "R",
            "С": "S",
            "Т": "T",
            "У": "U",
            "Ф": "F",
            "Х": "H",
            "Ъ": "",
            "Ы": "Y",
            "Ь": "",
            "Э": "E",
            "Ä": "A",
            "Ö": "O",
            "Ü": "U",
        }
        capital_letters_transliterated_to_multiple_letters = {
            "Ж": "Zh",
            "Ц": "Ts",
            "Ч": "Ch",
            "Ш": "Sh",
            "Щ": "Sch",
            "Ю": "Yu",
            "Я": "Ya",
        }
        lower_case_letters = {
            "а": "a",
            "б": "b",
            "в": "v",
            "г": "g",
            "д": "d",
            "е": "e",
            "ё": "e",
            "ж": "zh",
            "з": "z",
            "и": "i",
            "й": "y",
            "к": "k",
            "л": "l",
            "м": "m",
            "н": "n",
            "о": "o",
            "п": "p",
            "р": "r",
            "с": "s",
            "т": "t",
            "у": "u",
            "ф": "f",
            "х": "h",
            "ц": "ts",
            "ч": "ch",
            "ш": "sh",
            "щ": "sch",
            "ъ": "",
            "ы": "y",
            "ь": "",
            "э": "e",
            "ю": "yu",
            "я": "ya",
            "ä": "a",
            "ö": "o",
            "ü": "u",
            "ß": "ss",
            "ç": "c",
            "ş": "s",
        }
        capital_and_lower_case_letter_pairs = {}
        for (
            capital_letter,
            capital_letter_translit,
        ) in capital_letters_transliterated_to_multiple_letters.items():
            for (
                lowercase_letter,
                lowercase_letter_translit,
            ) in lower_case_letters.items():
                capital_and_lower_case_letter_pairs[
                    "%s%s" % (capital_letter, lowercase_letter)
                ] = "%s%s" % (capital_letter_translit, lowercase_letter_translit)
        for dictionary in (
            capital_and_lower_case_letter_pairs,
            capital_letters,
            lower_case_letters,
        ):
            for cyrillic_string, latin_string in dictionary.items():
                string = string.replace(cyrillic_string, latin_string)
        for (
            cyrillic_string,
            latin_string,
        ) in capital_letters_transliterated_to_multiple_letters.items():
            string = string.replace(cyrillic_string, latin_string.upper())
        return string


class Pipe:
    """

    Data pipeline class.

    Create pipelines for data preparing.

    """

    sequence: List[TextTransform]

    @staticmethod
    def ndarray_map(data: np.ndarray, func: Callable, args, kwargs):
        return np.vectorize(func)(data, *args, **kwargs)

    @staticmethod
    def series_map(data: pd.Series, func: Callable, args, kwargs):
        return data.apply(func, args=args, **kwargs)

    @staticmethod
    def dataframe_map(data: pd.DataFrame, func: Callable, args, kwargs):
        for c in data.columns:
            data[c] = data[c].apply(func, args=args, **kwargs)
        return data

    def __init__(self, *sequence):
        self.sequence = sequence

    def __call__(self, data: pd.Series, inline: bool = False) -> pd.Series:
        if type(data) != str:
            d = data if inline else data.copy()
        else:
            d = data
        if type(d) == np.ndarray:
            for s in self.sequence:
                d = Pipe.ndarray_map(d, s[0], s[1], s[2])
        elif type(d) == pd.Series:
            for s in self.sequence:
                d = Pipe.series_map(d, s[0], s[1], s[2])
        elif type(d) == str:
            for s in self.sequence:
                d = s[0](d, *s[1], **s[2])
        elif type(d) == pd.DataFrame:
            for s in self.sequence:
                d = Pipe.dataframe_map(d, s[0], s[1], s[2])
        return d

    def __repr__(self) -> str:
        r = [s[0].__name__ for s in self.sequence]
        return " -> ".join(r)

    def add2pipe(self, func: Callable, *args, **kwargs):
        return self.sequence.append(func, args, kwargs)
