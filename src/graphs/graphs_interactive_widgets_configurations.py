
from src.processing.format.data_wrapper_operations import WrapperOperations
from src.graphs.constants.config_smooth import ConfigFilter
from src.graphs.constants.config_baseline import ConfigBaseline


def get_func_configuration(your_class, your_func):
    """ Returns interactive widget initialization instructions by class and method passed.
    Args:
        your_class: Class to which the chosen method belongs.
        your_func: Chosen processing method.

    Returns:

    """

    func_defaults = WrapperOperations.get_function_default_arguments(your_func)
    if your_class.__name__ == "Baseline":
        configuration_class = ConfigBaseline
    elif your_func.__name__ == "Filter":
        configuration_class = ConfigFilter
    else:
        raise NotImplementedError("Add your configuration class")
    func_configuration = configuration_class.CONFIGURATIONS.get(your_func.__name__)
    return your_class.__name__, your_func.__name__, func_defaults, func_configuration
