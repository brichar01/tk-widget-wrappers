from tkinter import StringVar, IntVar, Variable
from typing import TypeVar

from tests.tests_base import IBaseEvent

T = TypeVar("T")


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
