import argparse
import asyncio
from tkinter import Tk, ttk
import asynctkinter as aiotk
from async_tkinter_loop import async_mainloop, async_handler


def test_step_row(tk_root):
    async def update_row(update: TestStateVar):
        update.update(active=TestActive.YES,
                      title="Mock test",
                      result=TestResult.FAIL,
                      desc="Failed test!")
        await asyncio.sleep(5)
        update.update(active=TestActive.YES,
                      title="Mock test",
                      result=TestResult.PASS,
                      desc="Passed test!")

    var = TestStateVar(active=TestActive.YES, title="Mock test", result=TestResult.NOT_TESTED, desc="Mock test desc")

    app = WidgetWrapper(ttk.Frame,
                        children=[TestStepRow(0, var),
                                  WidgetWrapper(ttk.Button,
                                                args=((), {
                                                    "text": "Run tests",
                                                    "command": async_handler(update_row, var)
                                                }),
                                                grid_args=((), {
                                                    "column": 1,
                                                    "row": 0
                                                }))],
                        args=((), {}),
                        grid_args=((), {})
                        )
    app.render(tk_root)


tests = {
    "test_step_row": test_step_row
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-t",
                        "--test",
                        type=str,
                        choices=[test for test in tests.keys()],
                        help="name of test to use")

    args = parser.parse_args()
    root = Tk()
    aiotk.patch_unbind()
    tests[args.test](root)
    async_mainloop(root)
