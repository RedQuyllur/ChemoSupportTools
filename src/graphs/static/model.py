import numpy as np
import matplotlib.pyplot as plt

PLOT_SIZE_SINGLE = (8, 4)
PLOT_SIZE_DOUBLE = (8, 6)
PLOT_SIZE_RECT = (8, 8)


class GraphsModel:

    @staticmethod
    def prediction_timeline(
            x_time: np.ndarray or list,
            y_predictions: np.ndarray or list,
            y_references: np.ndarray or list,
            label_x: str = "Time [unix]",
            label_y: str = "#",
            title: str = "Prediction to reference timeline"
    ):
        fig, ax = plt.subplots(figsize=PLOT_SIZE_SINGLE)
        ax.plot(x_time, y_predictions, "-+", color="red", )
        ax.plot(x_time, y_references, "-+", color="blue", )
        ax.set(xlabel=label_x, ylabel=label_y, title=title)
        ax.grid()
        ax.margins(x=0)
        fig.tight_layout()
        return fig, ax

    @staticmethod
    def calibration_curve(
            x_iterations: np.ndarray or list or None,
            y_rmse: np.ndarray or list,
            label_x: str = "Iteration #",
            label_y: str = "RMSECV",
            title: str = "Calibration curve RMSECV"
    ):
        fig, ax = plt.subplots(figsize=PLOT_SIZE_SINGLE)
        if not x_iterations:
            x_iterations = [idx+1 for idx, _ in enumerate(y_rmse)]
        ax.semilogx(x_iterations, y_rmse)
        ax.set(xlabel=label_x, ylabel=label_y, title=title)
        ax.margins(x=0)
        fig.tight_layout()
        return fig, ax
