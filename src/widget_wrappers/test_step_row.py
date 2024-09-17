import asyncio
from tkinter import ttk

from libs.widget_wrappers.src.widget_wrappers.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrappers.widget_wrapper import WidgetWrapper, EventsMixin
from tests.tests_base import TestState, TestResult


class TestResultWidget(EventsMixin, WidgetWrapper):
    async def update(self, result_event: str):
        self.widget.configure({
            "background": ("green" if result_event == TestResult.PASS.value else
                           "red" if result_event == TestResult.FAIL.value else
                           "")
        })
        await asyncio.sleep(0)


class TestStepRow(WidgetWrapper):
    def __init__(self, test_events: TestState[TKEvent[str]]):
        super().__init__(ttk.Frame,
                         args=((), {}),
                         grid_args=((), {"sticky": "news", "pady": 1}),
                         children=[
                             WidgetWrapper(ttk.Label,
                                           args=((), {
                                               "textvariable": test_events.title.var,
                                               "font": ("", 12),
                                               "justify": "left",
                                               "anchor": "w",
                                               "width": 20
                                           }),
                                           grid_args=((), {"column": 0, "row": 0, "sticky": "w"}),
                                           ),
                             WidgetWrapper(ttk.Label,
                                           args=((), {
                                               "textvariable": test_events.desc.var,
                                               "font": ("", 8),
                                               "anchor": "center",
                                               "justify": "center",
                                               "width": 30
                                           }),
                                           grid_args=((), {"column": 1, "row": 0, "sticky": "w"})
                                           ),
                             TestResultWidget(ttk.Label,
                                              events=test_events.result,
                                              args=((), {
                                                  "textvariable": test_events.result.var,
                                                  "font": ("", 12),
                                                  "justify": "right",
                                                  "anchor": "e",
                                                  "width": 10,
                                                  "background": ""
                                              }),
                                              grid_args=((), {"column": 2, "row": 0, "sticky": "e"})
                                              )
                         ]
                         )