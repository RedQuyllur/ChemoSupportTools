import numpy as np

from src.graphs.static.simple import GraphsSimple


class GraphsSpectral:

    @staticmethod
    def spectra(
            x_axis: np.ndarray or list,
            y_spectra: np.ndarray or list,
            label_x: str = "Pixels #",
            label_y: str = "Amplitude #",
            title: str = "Spectrum",
            line_width: float = 0.1,
            color: str = "k",
    ):
        return GraphsSimple.single(
            x_axis, y_spectra, label_x, label_y, title, line_width, color
        )

    @staticmethod
    def spectra_comparison(
            x1_axis: np.ndarray or list,
            x2_axis: np.ndarray or list or None,
            y1_spectra: np.ndarray or list,
            y2_spectra: np.ndarray or list,
            label_x: str = "Pixels #",
            label_y: str = "Amplitude #",
            title: str = "Spectra comparison",
            line_width: float = 0.1,
            color: str = "k",
    ):
        return GraphsSimple.comparison(
            x1_axis, x2_axis, y1_spectra, y2_spectra, label_x, label_y, title, line_width, color
        )
