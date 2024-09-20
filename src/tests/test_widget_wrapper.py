import argparse
from tkinter import Tk, ttk, StringVar
import asynctkinter as aiotk
from async_tkinter_loop import async_mainloop

from src.widget_wrapper import EventsMixin, WidgetWrapper


def test_widget_wrapper(tkroot):
    app = WidgetWrapper(ttk.Label, args=((), {'text': "Test Widget wrapper"}), grid_args=((), {}))
    app.render(tkroot)


def test_events(tkroot):
    class EventTest(EventsMixin, WidgetWrapper):
        def update(self, string_to_print: str):
            print(string_to_print)

    var = StringVar(tkroot, value="Don't say it!")
    app = EventTest(ttk.Label, events=var, args=((), {"text": "I'm saying it!"}), grid_args=((), {}))
    app.render(tkroot)
    var.set("Hello World!")


tests = {
    "test_widget_wrapper": test_widget_wrapper,
    "test_events": test_events
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




