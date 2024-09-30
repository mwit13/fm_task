from enum import Enum


class State(Enum):
    FAIL = 'FAIL'
    SUCCESS = 'SUCCESS'

    def __str__(self):
        return str(self.value)
