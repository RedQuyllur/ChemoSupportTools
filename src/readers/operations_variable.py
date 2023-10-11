
import numpy as np


class VariableOperations:
    """ Class collecting the basic data/format conversions.
    """

    @staticmethod
    def list_to_string(list_to_convert: list) -> str:
        return "".join(list_to_convert)

    @staticmethod
    def is_matrix_1d(matrix: np.ndarray) -> bool:
        if isinstance(matrix, list):
            if isinstance(matrix[0], (int, float)):
                return True
            else:
                return False
        elif isinstance(matrix, np.ndarray):
            if matrix.ndim == 1:
                return True
            else:
                return False
