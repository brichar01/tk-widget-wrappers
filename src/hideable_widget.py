from tkinter import ttk
from typing import Tuple, Dict, Any

from libs.widget_wrappers.src.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrapper import WidgetWrapper, EventsMixin


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

    def render(self, root: ttk.Widget, context: dict) -> None:
        context["visibility"] = self.visible
        super().render(root, context)
