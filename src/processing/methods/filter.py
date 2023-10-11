
import numpy as np

from scipy.signal import savgol_filter
from scipy.signal.windows import general_gaussian

from collections import deque
from bisect import insort, bisect_left
from itertools import islice

from src.processing.format.data_wrapper import data_interface
from src.processing.format.data_wrapper_constants import DataFoldsConstants


class Filter:
    """
    A preprocessor class dedicated to spectrum processing methods.
    """

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_y)
    def sav_gol(
            y: np.ndarray = None,
            window_size: int = 151,
            polyorder: int = 5,
            derivative: int = 0,
    ) -> np.ndarray:
        """ Apply a Savitzky-Golay filter to an array.
        Example Method source:
        https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.savgol_filter.html

        Args:
            y (np.ndarray): The data to be filtered.
            window_size (int): The samples number affected by filter in one iteration.
            polyorder (int): The order of the polynomial used to fit the
                samples. Polyorder must be smaller than size of window.
            derivative (int): The order of the derivative applied to filtered signal, pass >1 to get effect.

        Returns:
            (np.ndarray): The filtered data.
        """
        return savgol_filter(
            x=y,
            window_length=window_size,
            polyorder=polyorder,
            deriv=derivative
        )

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_y)
    def running_median_insort(
            y: np.ndarray = None,
            window_size: int = 3
    ):
        """ Apply a running median insort to an array.
        Contributed by Peter Otten.

        Args:
            y (np.ndarray): The data to be filtered.
            window_size (int): The samples number affected by filter in one iteration.

        Returns:
            (np.ndarray): The filtered data. Same shape as spectrum.
        """

        y = iter(y)
        d = deque()
        s = []
        result = []
        for item in islice(y, window_size):
            d.append(item)
            insort(s, item)
            result.append(s[len(d) // 2])
        m = window_size // 2
        for item in y:
            old = d.popleft()
            d.append(item)
            del s[bisect_left(s, old)]
            insort(s, item)
            result.append(s[m])
        return result

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_y)
    def fourier(
            y: np.ndarray = None,
            sigma: int = 40,
            m: int = 1,
            derivative: bool = False
    ):
        """ Fourier-transform based filtering.

        Args:
            y (np.ndarray): The data to be filtered.
            sigma (int): standard deviation of windows (in pixels).
            m (int): General gaussian power level,
                for 1 is conventional Gaussian,
                for larger values of m gaussian tends to a flat-top function.
            derivative (bool): Apply a derivative.
                False - Derivative is not computed.
                True - Compute derivative of passed signal.

        Returns:
            (np.ndarray): The filtered data or its derivative.
        """

        X = np.array(y).T
        XX = np.hstack((X, np.flip(X)))
        win = np.roll(general_gaussian(XX.shape[0], m, sigma), XX.shape[0] // 2)
        fXX = np.fft.fft(XX)
        XXf = np.real(np.fft.ifft(fXX * win))[:X.shape[0]]

        if derivative:
            qq = 2 * np.pi * np.arange(-XX.shape[0] // 2, XX.shape[0] // 2, 1) / XX.shape[0]
            # Define a new window
            win_derivative = np.roll(general_gaussian(XX.shape[0], m, 0.5 * sigma), XX.shape[0] // 2)
            # Calculate FFT and multiply by -q^2
            f2XX = np.roll(np.roll(fXX, -XX.shape[0] // 2) * (-qq ** 2), XX.shape[0] // 2)
            # Multiply by the window and inverse FFT
            XXf2 = np.real(np.fft.ifft(f2XX * win_derivative))[:X.shape[0]]
            return XXf2
        else:
            return XXf
