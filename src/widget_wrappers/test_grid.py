from tkinter import ttk, Variable
from typing import List, Tuple, Any, Dict, Callable

from libs.widget_wrappers.src.widget_wrappers.run_test_widget import RunTestWidget
from libs.widget_wrappers.src.widget_wrappers.test_step_row import TestStepRow
from libs.widget_wrappers.src.widget_wrappers.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrappers.widget_wrapper import WidgetWrapper
from tests.tests_base import TestActive, TestState


class TestToggleButton(WidgetWrapper):
    def __init__(self,
                 test_active: Variable,
                 args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]]):
        args[1]["command"] = self.toggle
        args[1]["textvariable"] = test_active
        super().__init__(ttk.Button, args=args, grid_args=grid_args)
        self.test_active = test_active

    def toggle(self):
        self.test_active.set(
            TestActive.NO.value if self.test_active.get() == TestActive.YES.value else
            TestActive.YES.value
        )


class TestStepGridWidget(WidgetWrapper):
    def __init__(self,
                 run_tests: Callable,
                 frame_args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]],
                 test_events: List[TestState[TKEvent[str]]],
                 stop_signal: TKEvent[str]):
        super().__init__(ttk.Frame, frame_args, grid_args, children=[
            WidgetWrapper(ttk.Frame,
                          args=((), {}),
                          grid_args=((), {
                              "sticky": "news"
                          }),
                          children=[
                              *[TestStepRow(test_event) for test_event in test_events],
                              RunTestWidget(
                                  run_tests=run_tests,
                                  stop_signal=stop_signal,
                                  args=((), {}),
                                  grid_args=((), {
                                      "sticky": "news"
                                  })
                              )
                          ]
                          ),
        ])


