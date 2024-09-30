from datetime import datetime
from enum import Enum


class IdInt(int):
    pass


class DateValue(datetime):
    pass


class Title(str):
    pass


class JSONDict(dict):
    pass


class FullName(str):
    pass


class Description(str):
    pass


class _Enum(Enum):
    def __str__(self):
        return str(self.value).lower()


class AgeRating(_Enum):
    R = "R"
    PG = "PG"
    PG_13 = "PG-13"
    G = "G"

    PASSED = "PASSED"
    NOT = "NOT"
    RATED = "RATED"
    APPROVED = "APPROVED"
    UNRATED = "UNRATED"

    TV_MA = "TV-MA"
    TV_14 = "TV-14"
    TV_Y7 = "TV-Y7"
    TV_G = "TV-G"
    TV_PG = "TV-PG"

    NC_17 = "NC-17"


class Genre(str):
    pass


class Language(str):
    pass


class Country(str):
    pass


class IMDbId(str):
    pass


class MovieType(_Enum):
    MOVIE = "MOVIE"
    SERIES = "SERIES"


class DollarsFull(int):
    pass


class Company(str):
    pass


class Score(int):
    pass

