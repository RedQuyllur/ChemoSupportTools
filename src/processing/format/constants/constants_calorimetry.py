
from src.processing.format.constants.constants_template import *


class ConstantsIsothermalCalorimetry(PreprocessorConstants):

    Y_HEAT_FLOW: str
    X_TIMESTAMP: str

    def __init__(self):
        super().__init__()

        self.Y_HEAT_FLOW = "heat_flow"
        self.X_TIMESTAMP = "axis_timestamp"

        self.DATA_FORMAT_AVAILABLE_Y = [
            self.Y_HEAT_FLOW
        ]

        self.DATA_FORMAT_AVAILABLE_X = [
            self.X_TIMESTAMP
        ]


_CONST: ConstantsIsothermalCalorimetry = ConstantsIsothermalCalorimetry()

DefaultConfigY = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_Y,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_Y,
    instruction_unpack={"y": _CONST.Y_HEAT_FLOW},
    instruction_pack={"y": _CONST.Y_HEAT_FLOW},
    parent_class=ConstantsIsothermalCalorimetry
)

DefaultConfigMultipleY = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_MULTIPLE_YX,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_MULTIPLE_YX,
    instruction_unpack={"y": [_CONST.Y_HEAT_FLOW, _CONST.X_TIMESTAMP]},
    instruction_pack={"y": [_CONST.Y_HEAT_FLOW, _CONST.X_TIMESTAMP]},
    parent_class=ConstantsIsothermalCalorimetry
)

DefaultConfigYofX = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_Y_OF_X,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_Y,
    instruction_unpack={"y": _CONST.Y_HEAT_FLOW, "x": _CONST.X_TIMESTAMP},
    instruction_pack={"y": _CONST.Y_HEAT_FLOW, "x": _CONST.X_TIMESTAMP},
    parent_class=ConstantsIsothermalCalorimetry
)


class ConstantsCalorimetry:
    constants: ConstantsIsothermalCalorimetry = ConstantsIsothermalCalorimetry()
    config_y: DefaultConfigY = DefaultConfigY
    config_multi_y: DefaultConfigMultipleY = DefaultConfigMultipleY
    config_y_of_x: DefaultConfigYofX = DefaultConfigYofX
