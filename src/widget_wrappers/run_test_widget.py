import asyncio
from tkinter import ttk
from typing import Tuple, Any, Dict, Callable, Coroutine, List

from async_tkinter_loop import async_handler

from libs.widget_wrappers.src.widget_wrappers.responsive_button import ResponsiveButtonWidget, ButtonStates
from libs.widget_wrappers.src.widget_wrappers.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrappers.widget_wrapper import WidgetWrapper, EventsMixin
from tests.tests_base import TestResult, TestState


class TestRunSummaryWidget(EventsMixin, WidgetWrapper):
    def __init__(self,
                 events: TKEvent[str],
                 grid_args: Tuple[Tuple, Dict[str, Any]]
                 ):
        super().__init__(ttk.Label,
                         events=events,
                         args=((), {
                             "textvariable": events.var,
                             "font": ("default", 25),
                             "background": ""
                         }),
                         grid_args=grid_args)

    async def update(self, update):
        self.widget.configure({
            "background": ("green" if update == TestResult.PASS.value else
                           "red" if update == TestResult.FAIL.value else
                           "")})


class TestStopWidget(EventsMixin, WidgetWrapper):
    def __init__(self, stop_signal: TKEvent[str], grid_args):
        self.stop_signal = stop_signal
        super().__init__(
            ttk.Button,
            events=self.stop_signal,
            args=((), {
                'command': async_handler(self.stop_tests),
                'text': "Stop",
                'state': ButtonStates.DISABLED
            }),
            grid_args=grid_args,

        )

    async def stop_tests(self, *args, **kwargs):
        self.stop_signal.set("stop")

    async def update(self, new_state: str):
        self.widget.configure({"state": ButtonStates.ACTIVE if new_state == 'running' else ButtonStates.DISABLED})


class RunTestWidget(WidgetWrapper):
    def __init__(self,
                 run_tests: Callable[..., Coroutine[Any, Any, List[TestState[TKEvent[str]]]]],
                 stop_signal: TKEvent[str],
                 args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]]):
        test_result = TKEvent[str](value=TestResult.NOT_TESTED.value)
        self.stop_signal = stop_signal

        async def run_tests_wrapper(*args, **kwargs):
            self.stop_signal.set("running")
            res = await run_tests()
            test_result.set(
                TestResult.PASS.value if not any([
                    te.result.get() == TestResult.FAIL.value for te in res])
                else TestResult.FAIL.value)
            self.stop_signal.set("stop")
            await asyncio.sleep(0)

        super().__init__(ttk.Frame,
                         args=args,
                         grid_args=grid_args,
                         children=[
                             TestRunSummaryWidget(events=test_result,
                                                  grid_args=((), {
                                                      "column": 0,
                                                      "row": 0,
                                                      "padx": 100,
                                                      "sticky": 'n'
                                                  })),
                             ResponsiveButtonWidget(command=run_tests_wrapper,
                                                    args=((), {
                                                        "text": "Run tests"
                                                    }),
                                                    grid_args=((), {
                                                        "column": 1,
                                                        "row": 0
                                                    }),
                                                    shortcut="<Return>"),

                             TestStopWidget(stop_signal,
                                            grid_args=((), {
                                                "column": 2,
                                                "row": 0
                                            }))
                         ])
