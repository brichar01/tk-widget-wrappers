from typing import List, Tuple, Any, Dict, Optional, TypeVar, Union, Callable
from tkinter import ttk

from async_tkinter_loop import async_handler

from ui_events import TKEvent

T = TypeVar("T")


class WidgetWrapper:
    def __init__(self,
                 widget_class: type[ttk.Widget],
                 *_args,
                 args:  Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]],
                 children=None,
                 **_kwargs):
        super(WidgetWrapper).__init__(*_args, **_kwargs)
        if children is None:
            children = []
        self.children: List[WidgetWrapper] = children
        self.widget = None
        self.widget_class = widget_class
        self.args = args
        self.grid_args = grid_args

    def apply_to_children(self, func_factory: Callable[[Any], Callable[[Any], None]], *args, **kwargs):
        for child in self.children:
            func_factory(child)(*args, **kwargs)

    def register_shortcuts(self):
        self.apply_to_children(lambda child: child.register_shortcuts)

    def unregister_shortcuts(self):
        self.apply_to_children(lambda child: child.unregister_shortcuts)


    def render(self, root: ttk.Widget) -> None:
        self.widget: ttk.Widget = self.widget_class(root, *self.args[0], **self.args[1])
        self.widget.grid(*self.grid_args[0], **self.grid_args[1])
        self.apply_to_children(lambda child: child.render, self.widget)

    def create_context(self, context: Dict[str, Any]):
        self.apply_to_children(lambda child: child.create_context, context)


class EventsMixin[T]:
    def __init__(self: Union[WidgetWrapper, 'EventsMixin'], *args, events: TKEvent[T], **kwargs):
        super().__init__(*args, **kwargs)

        async def wrapper(*_):
            await self.update(events.get())
        events.trace_add("write", async_handler(wrapper))

    async def update(self: Union[WidgetWrapper, 'EventsMixin'], var: T):
        raise NotImplementedError(f"Implement update message when using Events mixin for class {self.__class__}")


class ContextMixin[T]:
    _context = None
    key = ""

    def __init__(self, *args, use_context_key: str = "",  **kwargs):
        self.key = use_context_key
        super().__init__(*args, **kwargs)

    def create_context(self: Union[WidgetWrapper, 'ContextMixin'], context: dict[str, TKEvent[T]]):
        self._context = context
        self.apply_to_children(lambda child: child.create_context, context)

    def get_context(self: Union[WidgetWrapper, 'ContextMixin'], key=None) -> T:
        if key is None:
            key = self.key
        if self._context is not None and key in self._context.keys():
            return self._context[key].get()
        return None
