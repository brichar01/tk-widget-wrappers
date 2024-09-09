from tkinter import ttk
from typing import List, Dict, Any, Tuple

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.util.spinner_model import OvalSpinner, NoSpinner
from libs.widget_wrappers.src.ui_events import TKEvent
from libs.widget_wrappers.src.widget_wrapper import EventsMixin, WidgetWrapper
from tests.utils.commands import SpinData


class SpinDataEvent(TKEvent[List[SpinData]]):
    def __init__(self, spin_data: List[SpinData]):
        super().__init__(value=f'{spin_data.__hash__ if spin_data is not None else ""}')
        self.data = spin_data

    def set(self, new_data: List[SpinData]):
        super().set(value=f'{new_data.__hash__}')
        self.data = new_data

    def get(self) -> List[SpinData]:
        return self.data


class SpinDataGraphWidget(EventsMixin, WidgetWrapper):
    def __init__(self,
                 data: SpinDataEvent,
                 args: Tuple[Tuple, Dict[str, Any]],
                 grid_args: Tuple[Tuple, Dict[str, Any]],
                 graph_args: Tuple[Tuple, Dict[str, Any]]):
        super().__init__(ttk.Frame,
                         events=data,
                         args=args,
                         grid_args=grid_args)
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.axes = [self.fig.add_subplot(211), self.fig.add_subplot(212)]
        self.canvas = None
        self.graph_args = graph_args

    async def update(self, new_data: List[SpinData]):
        print(f"Updating Graph, {new_data[0].duty}")
        no_spinner_model = NoSpinner()
        no_spinner = [{
            "rpm": no_spinner_model.get_expected_rpm(point.duty, point.input_mv),
            "spinner_i": no_spinner_model.get_expected_current(point.rpm, point.input_mv)
        } for point in new_data]
        empty_model = OvalSpinner()
        no_food = [{
            "rpm": empty_model.get_expected_rpm(point.duty, point.input_mv),
            "spinner_i": empty_model.get_expected_current(point.rpm, point.input_mv)
        } for point in new_data]
        self.axes[0].cla()
        self.axes[0].set_xlabel('Time')
        self.axes[0].set_ylabel('Current mA')
        time = [step / 50 for step in range(len(new_data))]
        paths = (
            self.axes[0].plot(time, [data.spinner_i for data in new_data],
                              time, [exp_data["spinner_i"] for exp_data in no_food],
                              time, [exp_data["spinner_i"] for exp_data in no_spinner])
        )
        self.axes[0].legend(paths, ('Actual', 'Modelled', 'No Spinner'))
        self.axes[1].cla()
        self.axes[1].set_xlabel('Time')
        self.axes[1].set_ylabel('RPM')
        time = [step / 50 for step in range(len(new_data))]
        paths = (
            self.axes[1].plot(time, [data.rpm for data in new_data],
                              time, [exp_data["rpm"] for exp_data in no_food],
                              time, [exp_data["rpm"] for exp_data in no_spinner])
        )
        self.axes[1].legend(paths, ('Actual', 'Modelled', 'No Spinner'))
        self.canvas.draw()

    def render(self, root, context: dict):
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, root, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(sticky='news', padx=10, row=2, column=0, columnspan=3)
        self.canvas.get_tk_widget().grid(*self.graph_args[0], **self.graph_args[1])
        super().render(root, context)
