import numpy as np

from src.graphs.static.simple import GraphsSimple


class GraphsTime:

    @staticmethod
    def fourier_spectra(
            x_frequency: np.ndarray or list,
            x_amp_spectra: np.ndarray or list,
            label_x: str = "Frequency [Hz]",
            label_y: str = "Amplitude #",
            title: str = "Fourier spectrum",
            line_width: float = 0.1,
            color: str = "k",
    ):
        return GraphsSimple.single(
            x_frequency, x_amp_spectra, label_x, label_y, title, line_width, color
        )

    @staticmethod
    def fourier_spectra_comparison(
            x1_frequency: np.ndarray or list,
            x2_frequency: np.ndarray or list or None,
            y1_amp_spectra: np.ndarray or list,
            y2_amp_spectra: np.ndarray or list,
            label_x: str = "Frequency [Hz]",
            label_y: str = "Amplitude #",
            title: str = "Fourier spectra comparison",
            line_width: float = 0.1,
            color: str = "k",
    ):
        return GraphsSimple.comparison(
            x1_frequency, x2_frequency, y1_amp_spectra, y2_amp_spectra, label_x, label_y, title, line_width, color
        )
