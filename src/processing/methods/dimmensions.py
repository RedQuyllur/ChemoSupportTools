
import numpy as np

from src.processing.format.data_wrapper import data_interface
from src.processing.format.data_wrapper_constants import DataFoldsConstants


class Dimensions:

    @staticmethod
    @data_interface(instruction=DataFoldsConstants.spectro.ftir.config_multi_y)
    def cut_in_range(
            y: np.ndarray or list = None,
            cut_range: (int, int) = (200, -100),
            return_middle: bool = True
    ) -> np.ndarray or list:
        """ Get region or its outer areas from the passed array.

        Args:
            y (np.ndarray): The data to be cut off.
            cut_range (int, int): Cut off range.
                If expressed as negative, refer to the distance from the end.
            return_middle: Return middle or outer areas of the passed region.
                True - returns middle region,
                False - outer areas region (inversion).

        Returns:
            (np.ndarray) | (list)

        """
        position_left = cut_range[0] 
        position_right = cut_range[-1]

        if position_left <= 0:
            position_left = len(y) + position_left
        if position_right <= 0:
            position_right = len(y) + position_right
        if position_left >= position_right:
            position_left, position_right = position_right, position_left
        if position_left > len(y) or position_right > len(y):
            raise ValueError(f"One of values ({position_left},{position_right}) is out of array dim. [{len(y)}].")

        if return_middle:
            return y[position_left:position_right]
        else:
            if position_left == 0:
                return y[position_right:]
            elif position_right == 0:
                return y[:position_left]
            else:
                return np.concatenate([y[:position_left], y[position_right:]])
