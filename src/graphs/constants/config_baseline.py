
from src.graphs.constants.constants import JupyterWidgetsConstants


class ConfigBaseline:
    """
    A class that stores of hyperparameters of baseline processing methods for widget generation.
    """
    CW: JupyterWidgetsConstants = JupyterWidgetsConstants()
    _OUTPUT_AVAILABLE = [
        "baseline",
        "removal"
    ]

    _ALS_OPTIMIZED = {
        "output": CW.get_config_dropdown(
            description="output", options=_OUTPUT_AVAILABLE, value=1),
        "lam": CW.get_config_slider_float_log(
            description="filter lam", value=2, base=10, minimum=2, maximum=9, step=0.2),
        "p": CW.get_config_slider_float_log(
            description="asymmetry p", value=-3, base=10, minimum=-5, maximum=0, step=0.2),
        "iterations": CW.get_config_slider_int(
            description="iterations", value=10, minimum=1, maximum=100, step=1)
    }

    _RUNNING_MEDIAN_INSORT = {
        "output": CW.get_config_dropdown(
            description="output", options=_OUTPUT_AVAILABLE, value=1),
        "window_size": CW.get_config_slider_int(
            description="window", value=1, minimum=1, maximum=151, step=2)
    }

    _IMPROVED_MOD_POLY = {
        "output": CW.get_config_dropdown(
            description="output", options=_OUTPUT_AVAILABLE, value=1),
        "polynomial_degree": CW.get_config_slider_int(
            description="poly degree", value=2, minimum=1, maximum=15, step=1),
        "gradient": CW.get_config_slider_float_log(
            description="gradient", value=0, base=10, minimum=-5, maximum=0, step=0.2),
        "iterations": CW.get_config_slider_int(
            description="iterations", value=10, minimum=1, maximum=100, step=1)
    }

    # Summary dictionary that stores references to the processing methods widget constants.py.
    CONFIGURATIONS = {
        "als_optimized": _ALS_OPTIMIZED,
        "running_median_insort": _RUNNING_MEDIAN_INSORT,
        "improved_mod_poly": _IMPROVED_MOD_POLY,
    }
