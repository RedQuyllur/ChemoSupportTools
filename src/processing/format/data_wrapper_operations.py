
import inspect

import numpy as np


class WrapperOperations:
    """ A collection class of methods intended to support wrappers.
    """

    @staticmethod
    def get_function_default_arguments(func) -> dict:
        """ Returns default argument sets from function declarations as kwargs format.

        Args:
            func: Function whose default arguments are to be returned.

        Returns:
            (dict): defaults <kwargs> (key-value arguments).
        """
        func_signature = inspect.signature(func)
        return {
            key: value.default
            for key, value in func_signature.parameters.items()
            if value.default is not inspect.Parameter.empty
        }

    @staticmethod
    def get_function_default_arguments_and_update(func, **kwargs) -> dict:
        """ Gets the default method arguments and updates them based on the kwargs passed.

        Args:
            func: Function whose default arguments are to be updated and returned.

        Returns:
            (dict): updated default <kwargs> (key-value arguments).
        """
        # Get default setting from function
        default_kwargs = WrapperOperations.get_function_default_arguments(func)
        # Update defaults by values in kwargs
        for key in default_kwargs.keys():
            if key in kwargs:
                default_kwargs.update({key: kwargs.get(key)})
        return default_kwargs

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

    @staticmethod
    def is_key_in_kwargs(default_kv: dict, **kwargs):
        # Check that the kwargs passed match the default settings
        for key in kwargs.keys():
            if key not in default_kv.keys():
                raise KeyError("Passed keys does not match with the function defaults.")
