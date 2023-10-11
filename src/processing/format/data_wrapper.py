
import copy

from functools import wraps

from src.processing.format.data_wrapper_operations import WrapperOperations
from src.processing.format.constants.constants_template import PreprocessorConstants, PreprocessorConfiguration
from src.processing.format.data_wrapper_folds import *


def data_interface(
        original_function=None,
        *,
        data: dict = None,
        instruction: PreprocessorConfiguration = None
):
    """ Preprocessor wrapper.

    This wrapper determines how the data is calculated and passed on decorated function.

    Args:
        original_function: Chosen processing method.
        data (dict): Passing this key as argument will run data_interface decorator. To run method independently just
            set this key as None. In this case only key vocabulary will be checked before function call.
        instruction (object): Wrapper argument. Specifies how data is unpacked/packed inside a wrapper.


    Returns: Processed dataset or call function without decorator.

    """

    def _decorate(function):
        @wraps(function)
        def call_func(**kwargs):
            # Get the default method settings
            default_kwargs = WrapperOperations.get_function_default_arguments(function)
            # Check whether data has been included in the provided kwargs
            # If not, execute without wrapper:
            if ("data" not in kwargs) or (kwargs["data"] is None):
                WrapperOperations.is_key_in_kwargs(default_kv=default_kwargs, **kwargs)
                result = function(**kwargs)
                return result
            # If the data kv has been passed, execute:
            else:
                # Separate data from method arguments
                _data = copy.deepcopy(kwargs.pop("data"))

                if "instruction" in kwargs:
                    _instruction = kwargs.pop("instruction")
                else:
                    _instruction = instruction

                WrapperOperations.is_key_in_kwargs(default_kv=default_kwargs, **kwargs)

                # Update default settings
                updated_kwargs = default_kwargs
                updated_kwargs.update(kwargs)

                return process_fold_by_fold(
                    function=function,
                    instruction=_instruction,
                    data=_data,
                    updated_kwargs=updated_kwargs
                )

        return call_func

    if original_function:
        return _decorate(original_function)

    return _decorate
