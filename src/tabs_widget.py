from functools import reduce
from tkinter import ttk
from typing import Tuple, Dict, Any

from hideable_widget import HideableWidget, VisibilityStates
from ui_events import TKEvent
from widget_wrapper import EventsMixin, WidgetWrapper


def flatten_dict(list_of_dict: list[dict]):
    return reduce(lambda a, b: {**a, **b}, list_of_dict, {})


class TabsWidget(EventsMixin, WidgetWrapper):
    def __init__(self,
                 tabs: dict[str, WidgetWrapper],
                 args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]]):
        self.active_tab = TKEvent[str](value=list(tabs.keys())[0])
        self.tab_mapper: dict[str, TKEvent[str]] = flatten_dict([
            {key: TKEvent[str](value=val)} for key, val in tabs.items()
        ])
        super().__init__(ttk.Frame,
                         args=args,
                         grid_args=grid_args,
                         events=self.active_tab,
                         children=[
                             WidgetWrapper(ttk.OptionMenu,
                                           args=((self.active_tab.var,
                                                  None,
                                                  *tabs.keys()), {}),
                                           grid_args=((), {
                                               "sticky": 'e'
                                           })),
                             *[HideableWidget(ttk.Frame,
                                              children=[tab],
                                              args=((), {}),
                                              grid_args=((), {}),
                                              visibility_events=self.tab_mapper[name])
                               for name, tab in tabs.items()]
                         ])

    async def update(self, var: str):
        self._update(var)

    def _update(self, var: str):
        for name, tab in self.tab_mapper.items():
            if name == var:
                tab.set(VisibilityStates.VISIBLE)
            else:
                tab.set(VisibilityStates.HIDDEN)

    def render(self, root) -> None:
        super().render(root)
        self._update(self.active_tab.get())
