
import numpy as np

from scipy import sparse
from scipy.sparse.linalg import spsolve

from BaselineRemoval import BaselineRemoval

from src.processing.format.data_wrapper import data_interface
from src.processing.format.data_wrapper_constants import DataFoldsConstants

from src.processing.methods.filter import Filter


class Baseline:
    """
    A preprocessor class dedicated to baseline processing methods.

    Provides baseline estimation for instrumental methods like:
        time-domain signal filtering:
            calorimetry,
            ECG/EKG signal,
            vibratory acceleration signal,

        spectroscopy, eg.:
            absorbance/reflectance infrared spectroscopy (IR),
            Fourier-transform IR spectroscopy (FTIR),
            mass spectroscopy),
            nuclear magnetic resonance,
            mid-infrared spectroscopy in astronomic context.
    """
    _OUTPUT_AVAILABLE = [
        "baseline",
        "removal",
        "both",
    ]
    _OUTPUT_DEFAULT = _OUTPUT_AVAILABLE[1]

    @staticmethod
    def _baseline_operation_output(
            y: np.ndarray,
            baseline: np.ndarray,
            output: str = _OUTPUT_DEFAULT
    ) -> np.ndarray or tuple:
        """  Defines output of the method.

        Args:
            y: Non-processed signal.
            baseline: Signal baseline.
            output: Defines final output:
                "baseline" -> returns baseline,
                "removal" -> returns signal without baseline,
                "both" -> returns results as a tuple (baseline, removal)

        Returns:
            (np.ndarray) or (np.ndarray, np.ndarray)
        """
        if output == Baseline._OUTPUT_AVAILABLE[0]:
            return baseline
        elif output == Baseline._OUTPUT_AVAILABLE[1]:
            y_removal = np.subtract(y, baseline)
            return y_removal
        elif output == Baseline._OUTPUT_AVAILABLE[2]:
            y_removal = np.subtract(y, baseline)
            return y_removal, baseline
        else:
            raise ValueError(f"Invalid baseline operation output format: {output}")

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_y)
    def als_optimized(
            output: str = _OUTPUT_DEFAULT,
            y: np.ndarray = None,
            lam=1000,
            p=0.1,
            iterations=10,
    ):
        """ Asymmetric least squares as baseline removal.
        Estimate baseline using optimized version of ALS (Asymmetric Least Squares).
        Based on article: "Baseline Correction with Asymmetric Least Squares Smoothing,
            2005.09.21, Paul H. C. Eilers, Hans F.M. Boelens"

        Args:
            output (str): Specifies output format.
            y (np.ndarray): Signal array.
            lam (float): Defines filter of baseline function. In range: [10^2:10^9]
            p (float): Defines asymmetry of baseline function. In range: [0.001:0.1]
            iterations (int): Number of algorithm iterations, >0.

        Returns:
            (np.ndarray) or (np.ndarray, np.ndarray)
        """
        length = len(y)
        difference_matrix = sparse.diags([1, -2, 1], [0, -1, -2], shape=(length, length - 2))
        # Precompute this term since it does not depend on "weights"
        difference_matrix = lam * difference_matrix.dot(difference_matrix.transpose())
        weights = np.ones(length)
        weights_diagonal = sparse.spdiags(weights, 0, length, length)

        for i in range(iterations):
            # Do not create a new matrix, just update diagonal values
            weights_diagonal.setdiag(weights)
            Z = weights_diagonal + difference_matrix
            baseline = spsolve(Z, weights * y)
            weights = p * (y > baseline) + (1 - p) * (y < baseline)

        return Baseline._baseline_operation_output(y=y, baseline=baseline, output=output)

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_y)
    def running_median_insort(
            output: str = _OUTPUT_DEFAULT,
            y: np.ndarray = None,
            window_size: int = 3
    ):
        """ Running median insort as baseline removal.
        Args:
            output (str): Specifies output format.
            y (np.ndarray): Signal array.
            window_size (int): The length of the filter window.

        Returns:
            (np.ndarray) or (np.ndarray, np.ndarray)
        """
        baseline = Filter.running_median_insort(y=y, window_size=window_size)
        return Baseline._baseline_operation_output(y=y, baseline=baseline, output=output)

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_y)
    def improved_mod_poly(
            output: str = _OUTPUT_DEFAULT,
            y: np.ndarray = None,
            polynomial_degree: int = 2,
            iterations: int = 100,
            gradient: float = 0.001

    ):
        """ Improved modified multi-polynomial fit as baseline removal.
        Source: https://pypi.org/project/BaselineRemoval/

        Args:
            output (str): Specifies output format.
            y (np.ndarray): Signal array.
            polynomial_degree (int): refers to polynomial degree.
            iterations (int): refers to how many iterations to run.
            gradient (float): refers to gradient for polynomial loss.
                It measures incremental gain over each iteration.
                If gain in any iteration is less than this, further improvement will stop.

        Returns:
            (np.ndarray) or (np.ndarray, np.ndarray)
        """
        base_obj = BaselineRemoval(y)
        baseline = base_obj.IModPoly(
            degree=polynomial_degree,
            repitition=iterations,
            gradient=gradient
        )
        return Baseline._baseline_operation_output(y=y, baseline=baseline, output=output)
