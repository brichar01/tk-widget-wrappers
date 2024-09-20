from tkinter import StringVar, IntVar, Variable
from typing import TypeVar


T = TypeVar("T")


class IBaseEvent[T]:
    def __init__(self, value: T):
        self._value = value

    def get(self) -> T:
        return self._value

    def set(self, value: T):
        self._value = value

    def __str__(self):
        return self.get().__str__()


class TKEvent[T](IBaseEvent[T]):
    def __init__(self, value: T):
        super().__init__(Variable(value=value))

    def get(self) -> T:
        return self._value.get()

    def set(self, value: T):
        self._value.set(value)

    def trace_add(self, mode, callback):
        return self._value.trace_add(mode, callback)

    @property
    def var(self):
        return self._value
