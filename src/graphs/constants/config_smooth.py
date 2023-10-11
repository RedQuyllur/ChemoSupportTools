
from src.graphs.constants.constants import JupyterWidgetsConstants


class ConfigFilter:
    """
    A class that stores of hyperparameters of smoothing methods for widget generation.
    """
    CW: JupyterWidgetsConstants = JupyterWidgetsConstants()

    _SAV_GOL = {
        "polyorder": CW.get_config_slider_int(
            description="poly degree", value=2, minimum=0, maximum=15, step=1),
        "window_size": CW.get_config_slider_int(
            description="window", value=1, minimum=1, maximum=151, step=2),
        "derivative": CW.get_config_slider_int(
            description="derivative", value=0, minimum=1, maximum=5, step=1)
    }

    _RUNNING_MEDIAN_INSORT = {
        "window_size": CW.get_config_slider_int(
            description="window", value=1, minimum=1, maximum=151, step=2)
    }

    _FOURIER = {
        "sigma": CW.get_config_slider_int(
            description="std dev sigma", value=40, minimum=0, maximum=100, step=1),
        "m": CW.get_config_slider_int(
            description="flattening m", value=1, minimum=0, maximum=30, step=1),
        "derivative": CW.get_config_checkbox(description="derivative (1st)", value=False)
    }

    # Summary dictionary that stores references to the processing methods widget constants.py.
    CONFIGURATIONS = {
        "sav_gol": _SAV_GOL,
        "running_median_insort": _RUNNING_MEDIAN_INSORT,
        "fourier": _FOURIER
    }
