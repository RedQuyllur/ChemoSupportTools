import numpy as np
import matplotlib.pyplot as plt

from src.readers.operations_variable import VariableOperations

PLOT_SIZE_SINGLE = (8, 4)
PLOT_SIZE_DOUBLE = (8, 6)
PLOT_SIZE_RECT = (8, 8)


class GraphsSimple:

    @staticmethod
    def single(
            x: np.ndarray or list,
            y: np.ndarray or list,
            label_x: str = "#",
            label_y: str = "#",
            title: str = None,
            line_width: float = 0.1,
            color: str = "k",
    ):
        """
        #TODO Complete docstring
        """
        fig, ax = plt.subplots(figsize=PLOT_SIZE_SINGLE)
        if VariableOperations.is_matrix_1d(x):
            for line in y:
                ax.plot(x, line, "-", color=color, linewidth=line_width)
        else:
            for idx, line in enumerate(y):
                ax.plot(x[idx], line, "-", color=color, linewidth=line_width)
        ax.set(xlabel=label_x, ylabel=label_y, title=title)
        ax.margins(x=0)
        ax.grid()
        fig.tight_layout()
        return fig, ax

    @staticmethod
    def comparison(
            x1: np.ndarray or list,
            x2: np.ndarray or list or None,
            y1: np.ndarray or list,
            y2: np.ndarray or list,
            label_x: str = "#",
            label_y: str = "#",
            title: str = "Result comparison",
            line_width: float = 0.1,
            color: str = "k",
    ):
        """
        #TODO Complete docstring
        """
        if x2 is None:
            x2 = x1

        fig, ax = plt.subplots(2, figsize=PLOT_SIZE_DOUBLE)

        if VariableOperations.is_matrix_1d(x1):
            for line in y1:
                ax[0].plot(x1, line, "-", color=color, linewidth=line_width)
        else:
            for idx, line in enumerate(y1):
                ax[0].plot(x1[idx], line, "-", color=color, linewidth=line_width)

        if VariableOperations.is_matrix_1d(x2):
            for line in y2:
                ax[1].plot(x2, line, "-", color=color, linewidth=line_width)
        else:
            for idx, line in enumerate(y2):
                ax[1].plot(x2[idx], line, "-", color=color, linewidth=line_width)

        ax[0].set(
            ylabel=label_y,
            title=title
        )
        ax[1].set(
            xlabel=label_x,
            ylabel=label_y
        )
        for ax_idx in range(0, 2):
            ax[ax_idx].grid()
            ax[ax_idx].margins(x=0)

        fig.tight_layout()
        return fig, ax
