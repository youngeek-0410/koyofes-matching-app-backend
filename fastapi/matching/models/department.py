from enum import Enum


class Department(Enum):
    M = "M"
    E = "E"
    I = "I"
    C = "C"
    A = "A"

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
