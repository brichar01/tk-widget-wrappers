from typing import List, Tuple, Any, Dict, Optional, TypeVar
from tkinter import ttk, Tk

from async_tkinter_loop import async_handler

from libs.widget_wrappers.src.ui_events import TKEvent


T = TypeVar("T")


class EventsMixin:
    def __init__(self, *args, events: TKEvent, **kwargs):
        super().__init__(*args, **kwargs)

        async def wrapper(*_):
            await self.update(events.get())
        events.trace_add("write", async_handler(wrapper))

    async def update(self, var: Any):
        raise NotImplementedError(f"Implement update message when using Events mixin for class {self.__class__}")


class ContextMixin[T]:
    _context = None
    key = ""

    def render(self, root: ttk.Widget, context: dict[str, TKEvent[T]]):
        super().render(root, context)
        self._context = context

    def get_context(self, key=None) -> T:
        if key is None:
            key = self.key
        if self._context is not None and key in self._context.keys():
            return self._context[key].get()
        return None


class WidgetWrapper:
    def __init__(self,
                 widget_class: type[ttk.Widget],
                 args:  Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]],
                 children=None):
        if children is None:
            children = []
        self.widget = None
        self.widget_class = widget_class
        self.args = args
        self.children: List[WidgetWrapper] = children
        self.grid_args = grid_args
        self._context: Optional[dict] = None

    def register_shortcuts(self):
        for child in self.children:
            child.register_shortcuts()

    def unregister_shortcuts(self):
        for child in self.children:
            child.unregister_shortcuts()

    def render(self, root: ttk.Widget, context: dict) -> None:
        self.widget: ttk.Widget = self.widget_class(root, *self.args[0], **self.args[1])
        self.widget.grid(*self.grid_args[0], **self.grid_args[1])
        for child in self.children:
            child.render(self.widget, context)
