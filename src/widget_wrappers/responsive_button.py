import asyncio
from tkinter import ttk
from typing import Tuple, Dict, Any, Callable

from async_tkinter_loop import async_handler

from libs.widget_wrappers.src.widget_wrappers.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrappers.widget_wrapper import EventsMixin, WidgetWrapper


class ButtonStates:
    ACTIVE = "active"
    DISABLED = "disabled"


class ResponsiveButtonWidget(EventsMixin, WidgetWrapper):
    def __init__(self,
                 command: Callable,
                 args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]],
                 shortcut: str = None,
                 ):
        self.shortcut = shortcut
        self.command = command
        self.button_state = TKEvent[str](ButtonStates.ACTIVE)
        args[1]["command"] = async_handler(self.command_wrapper)
        super().__init__(ttk.Button,
                         events=self.button_state,
                         args=args,
                         grid_args=grid_args)

    async def command_wrapper(self, *args, **kwargs):
        if self.button_state.get() == ButtonStates.DISABLED:
            return
        self.button_state.set(ButtonStates.DISABLED)
        await asyncio.sleep(0)
        try:
            await self.command()
        finally:
            self.button_state.set(ButtonStates.ACTIVE)
            await asyncio.sleep(0)

    def unregister_shortcuts(self):
        if self.shortcut is not None:
            self.widget.unbind_all(self.shortcut)
        for child in self.children:
            child.unregister_shortcuts()

    def register_shortcuts(self):
        if self.shortcut is not None:
            self.widget.bind_all(self.shortcut, async_handler(self.command_wrapper))
        super().register_shortcuts()

    async def update(self, new_state: str):
        self.widget.configure({
            "state": new_state
        })
