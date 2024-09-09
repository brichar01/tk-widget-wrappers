from tkinter import ttk, Canvas
from typing import Tuple, Dict, Any

from libs.widget_wrappers.src.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrapper import WidgetWrapper, EventsMixin


class IndicatorState:
    ON = "green"
    OFF = "red"


class LightIndicatorWidget(EventsMixin, WidgetWrapper):
    def __init__(self, state_events: TKEvent[IndicatorState], args: Tuple[Tuple, Dict[str, Any]], grid_args: Tuple[Tuple, Dict[str, Any]]):
        super().__init__(ttk.Frame, events=state_events, args=args, grid_args=grid_args)
        self.indicator = None
        self.canvas = None

    async def update(self, state: str):
        self.canvas.itemconfig(self.indicator, fill=state)

    def render(self, root: ttk.Widget, context: dict) -> None:
        super().render(root, context)
        self.canvas = Canvas(self.widget, width=70, height=70)
        self.canvas.grid(row=0, column=0, sticky="e")
        self.indicator = self.canvas.create_oval(10, 10, 60, 60, fill="red")
