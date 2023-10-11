
import numpy as np

from src.processing.format.constants.constants_template import PreprocessorConstants
from src.processing.format.data_wrapper_format import DataFormat


@DataFormat
def data_pack(
        data_format: None,
        fold_data: dict,
        result: list
) -> dict:
    """ Default packing wrapper.

    This basic wrapper will pack data and update fold with processed data.

    Args:
        data_format: Information tag for switch-case wrapper cast.
        fold_data: Dataset that will be updated.
        result: Result of chosen operation.

    Returns: Updated data fold.

    """
    data = fold_data
    data["data"] = np.array(result)
    return data


@data_pack.format(PreprocessorConstants().PROCESS_DATA_AS_Y)
def _pack_wrapper_result_as_y(
        data_format: str,
        data: dict,
        instruction: dict,
        result: list
) -> dict:
    """ "Y" type packing wrapper.

    Args:
        data_format (int): Tag used for switch-case wrapper cast. Not used inside method.
        data (dict): Dataset that will be unpacked with method kwargs.
        instruction (dict): Defines what kind of data will be updated.
        result (list): Processed data.

    Returns:
        (dict)

    """
    data.update({instruction.get("y"): result})
    return data


@data_pack.format(PreprocessorConstants().PROCESS_DATA_AS_MULTIPLE_YX)
def _pack_wrapper_result_as_multiple_yx(
        data_format: str,
        data: dict,
        instruction: dict,
        result: list,
):
    """ "[Y0 ..., Yn, X0 ... Xn]" type packing wrapper.

    Args:
        data_format (int): Tag used for switch-case wrapper cast. Not used inside method.
        data (dict): Dataset that will be unpacked with method kwargs.
        instruction (dict): Defines what kind of data will be updated.
        result (list): Processed data.

    Returns: Updated data fold.

    """
    for label in instruction.get("y"):
        partial_result = [result.pop(0) for _ in range(len(data.get(label).tolist()))]
        data.update({label: partial_result})
    return data
