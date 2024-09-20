from tkinter import ttk
from typing import Tuple, Dict, Any, TypeVar

from ui_events import TKEvent
from widget_wrapper import EventsMixin, WidgetWrapper

T = TypeVar("T")

class VisibilityStates:
    VISIBLE = "visible"
    HIDDEN = "hidden"


class HideableWidget(EventsMixin, WidgetWrapper):
    def __init__(self,
                 widget_class: type[ttk.Widget],
                 visibility_events: TKEvent[str],
                 args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]],
                 children=None):
        if children is None:
            children = []
        self.visible = visibility_events
        super().__init__(widget_class,
                         events=visibility_events,
                         args=args,
                         grid_args=grid_args,
                         children=children)

    async def update(self, visible: str):
        if visible == VisibilityStates.HIDDEN:
            self.unregister_shortcuts()
            self.widget.grid_forget()
        else:
            self.register_shortcuts()
            self.widget.grid(*self.grid_args[0], **self.grid_args[1])

    def render(self, root: ttk.Widget) -> None:
        super().render(root)

    def create_context(self, context: dict[str, TKEvent[T]]):
        context["visibility"] = self.visible
