
class JupyterWidgetsConstants:
    """ Class provided for collections used in interactive plotter.
    """
    INT_SLIDER = 0
    FLOAT_SLIDER = 1
    FLOAT_LOG_SLIDER = 2
    INT_RANGE_SLIDER = 3
    FLOAT_RANGE_SLIDER = 4
    DROPDOWN = 5
    CHECKBOX = 6

    WIDGET_CONFIGURATION = 0
    WIDGET_TYPE = -1

    _CONF_SLIDER_INT = {
        "value": None,
        "min": None,
        "max": None,
        "step": None,
        "description": None
    }

    _CONF_SLIDER_FLOAT = {
        "value": None,
        "min": None,
        "max": None,
        "step": None,
        "description": None
    }

    _CONF_SLIDER_FLOAT_LOG = {
        "value": None,
        "base": None,
        "min": None,
        "max": None,
        "step": None,
        "description": None
    }

    _CONF_RANGE_SLIDER_INT = {
        "value": None,
        "min": None,
        "max": None,
        "step": None,
        "description": None
    }

    _CONF_RANGE_SLIDER_FLOAT = {
        "value": None,
        "min": None,
        "max": None,
        "step": None,
        "description": None
    }

    _CONF_DROPDOWN = {
        "options": None,
        "value": None,
        "description": None
    }

    _CONF_CHECKBOX = {
        "value": True,
        "description": None
    }

    WIDGET_CONFIGURATION_ARGUMENTS: dict = {
        INT_SLIDER: _CONF_SLIDER_INT,
        FLOAT_SLIDER: _CONF_SLIDER_FLOAT,
        FLOAT_LOG_SLIDER: _CONF_SLIDER_FLOAT_LOG,
        INT_RANGE_SLIDER: _CONF_RANGE_SLIDER_INT,
        FLOAT_RANGE_SLIDER: _CONF_RANGE_SLIDER_FLOAT,
        DROPDOWN: _CONF_DROPDOWN,
        CHECKBOX: _CONF_CHECKBOX,
    }

    @classmethod
    def get_config_slider_int(
            cls,
            value: int,
            minimum: int,
            maximum: int,
            step: int,
            description: str
    ) -> list:
        method_configuration: dict = {
            "value": value,
            "min": minimum,
            "max": maximum,
            "step": step,
            "description": description
        }
        configuration: list = [method_configuration, cls.INT_SLIDER]
        return configuration

    @classmethod
    def get_config_slider_float(
            cls,
            value: float,
            minimum: float,
            maximum: float,
            step: float,
            description: str
    ) -> list:
        method_configuration: dict = {
            "value": value,
            "min": minimum,
            "max": maximum,
            "step": step,
            "description": description
        }
        configuration: list = [method_configuration, cls.FLOAT_SLIDER]
        return configuration

    @classmethod
    def get_config_slider_float_log(
            cls,
            value: float,
            base: int,
            minimum: float,
            maximum: float,
            step: float,
            description: str
    ) -> list:
        method_configuration: dict = {
            "value": value,
            "base": base,
            "min": minimum,
            "max": maximum,
            "step": step,
            "description": description
        }
        configuration: list = [method_configuration, cls.FLOAT_LOG_SLIDER]
        return configuration

    @classmethod
    def get_config_range_slider_int(
            cls,
            value: int,
            minimum: int,
            maximum: int,
            step: int,
            description: str
    ) -> list:
        method_configuration: dict = {
            "value": value,
            "min": minimum,
            "max": maximum,
            "step": step,
            "description": description
        }
        configuration: list = [method_configuration, cls.INT_RANGE_SLIDER]
        return configuration

    @classmethod
    def get_config_range_slider_float(
            cls,
            value: float,
            minimum: float,
            maximum: float,
            step: float,
            description: str
    ) -> list:
        method_configuration: dict = {
            "value": value,
            "min": minimum,
            "max": maximum,
            "step": step,
            "description": description
        }
        configuration: list = [method_configuration, cls.FLOAT_RANGE_SLIDER]
        return configuration

    @classmethod
    def get_config_dropdown(
            cls,
            options: list,
            value: int,
            description: str
    ) -> list:
        method_configuration: dict = {
            "options": options,
            "value": value,
            "description": description
        }
        configuration: list = [method_configuration, cls.DROPDOWN]
        return configuration

    @classmethod
    def get_config_checkbox(
            cls,
            value: bool,
            description: str
    ) -> list:
        method_configuration: dict = {
            "value": value,
            "description": description
        }
        configuration: list = [method_configuration, cls.CHECKBOX]
        return configuration
