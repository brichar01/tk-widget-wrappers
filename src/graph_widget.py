from dataclasses import dataclass
from tkinter import ttk
from typing import List, Dict, Any, Tuple, TypeVar

from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui_events import TKEvent
from widget_wrapper import EventsMixin, WidgetWrapper

T = TypeVar("T")

class DataEvent(TKEvent[List[T]]):
    def __init__(self, data: List[T]):
        super().__init__(value=f'{data.__hash__ if data is not None else ""}')
        self.data = data

    def set(self, new_data: List[T]):
        super().set(value=f'{new_data.__hash__}')
        self.data = new_data

    def get(self) -> List[T]:
        return self.data


@dataclass
class DataPath:
    legend: str
    path: list[Any]

@dataclass
class DataPlot:
    paths: list[DataPath]
    xlabel: str
    ylabel: str

class GraphWidget(EventsMixin, WidgetWrapper):
    def __init__(self,
                 data: DataEvent,
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

    async def update_graph(self, plots: List[DataPlot]):
        for i, plot in enumerate(plots):
            self.axes[i].cla()
            self.axes[i].set_xlabel(plot.xlabel)
            self.axes[i].set_ylabel(plot.ylabel)
            p = self.axes[i].plot(*([path.path for path in plot.paths]))
            self.axes[i].legend(p, [path.legend for path in plot.paths])
        self.canvas.draw()

    def render(self, root):
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.draw()
        toolbar = NavigationToolbar2Tk(self.canvas, root, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(sticky='news', padx=10, row=2, column=0, columnspan=3)
        self.canvas.get_tk_widget().grid(*self.graph_args[0], **self.graph_args[1])
        super().render(root)
