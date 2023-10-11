
from src.processing.format.constants.constants_template import PreprocessorConstants
from src.processing.format.data_wrapper_operations import WrapperOperations
from src.processing.format.data_wrapper_format import DataFormat


@DataFormat
def data_unpack(
        data_format: None,
        data: dict,
        **kwargs
) -> list:
    """ Default unpacking wrapper. Produces output:

    [{"y":data[0], method_kwargs}, ..., {"y":data[n], method_kwargs}]

    Args:
        data_format: Information tag for switch-case wrapper cast.
        data: Dataset that will be unpacked.
        **kwargs: Processing method settings.

    Returns:
        (list)

    """

    Y = data.get("data").tolist()
    return [{**kwargs, **{"y": y}} for y in Y]


@data_unpack.format(PreprocessorConstants().PROCESS_DATA_AS_Y)
def _unpack_wrapper_data_as_y(
        data_format: int,
        data: dict,
        instruction: dict,
        **kwargs
) -> list:
    """ "Y(None)" type unpacking wrapper. On passed instruction:

    instruction["y"] == "signal"

    Produces output:

    [{"y":signal[0], method_kwargs}, ..., {"y":signal[n], method_kwargs}]

    Args:
        data_format (int): Tag used for switch-case wrapper cast. Not used inside method.
        data (dict): Dataset that will be unpacked with method kwargs.
        instruction (dict): Defines what kind of data will be unpacked.
        **kwargs: Processing method settings.

    Returns:
        (list)
    """

    Y = data.get(instruction.get("y")).tolist()
    if WrapperOperations.is_matrix_1d(Y):
        return [{**kwargs, **{"y": Y}}]
    else:
        return [{**kwargs, **{"y": y}} for y in Y]


@data_unpack.format(PreprocessorConstants().PROCESS_DATA_AS_Y_OF_X)
def _unpack_wrapper_data_as_y_of_x(
        data_format: int,
        data: dict,
        instruction: dict,
        **kwargs
) -> list:
    """ "Y(X)" type unpacking wrapper. On passed instruction:

    instruction["y"] = "signal"
    instruction["x"] = "x_axis"

    Produces output:

    [{"y": signal[0], "x": x_axis[0], **processing_method_settings}, ...,
     {"y": signal[n], "x": x_axis[n], **processing_method_settings}]

    Args:
        data_format (int): Tag used for switch-case wrapper cast. Not used inside method.
        data (dict): Dataset that will be unpacked with method kwargs.
        instruction (dict): Defines what kind of data will be unpacked.
        **kwargs: Processing method settings.

    Returns:
        (list)

    """

    X = data.get(instruction.get("x")).tolist()
    Y = data.get(instruction.get("y")).tolist()

    if WrapperOperations.is_matrix_1d(X):
        return [{**kwargs, **{"y": y}, **{"x": X}} for y in Y]
    else:
        return [{**kwargs, **{"y": y}, **{"x": X[idx]}} for idx, y in enumerate(Y)]


@data_unpack.format(PreprocessorConstants().PROCESS_DATA_AS_MULTIPLE_YX)
def _unpack_wrapper_data_as_multiple_yx(
        data_format: int,
        data: dict,
        instruction: dict,
        **kwargs
) -> list:
    """ "[Y0 ... Yn, X0 ... Xn]" type unpacking wrapper. On passed instruction:

    instruction["y"] = ["signal", "x_axis"]

    Will produce output bellow:

    [{"y": signal[0], method_kwargs}, ..., {"y": signal[n], method_kwargs},
     {"y": x_axis[0], method_kwargs}, ..., {"y": x_axis[n], method_kwargs}]

    Args:
        data_format (int): Tag used for switch-case wrapper cast. Not used inside method.
        data (dict): Dataset that will be unpacked with method kwargs.
        instruction (dict): Defines what kind of data will be unpacked.
        **kwargs: Processing method settings.

    Returns: Unpacked data with key-values processing method settings.

    """

    dataset = []
    for label in instruction.get("y"):
        dataset.extend(_unpack_wrapper_data_as_y(
            data_format=data_format,
            instruction={"y": label},
            data=data,
            **kwargs
        ))
    return dataset
