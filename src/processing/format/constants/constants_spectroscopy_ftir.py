
from src.processing.format.constants.constants_template import *


class ConstantsSpectroscopyFourierTransformIR(PreprocessorConstants):

    Y_SPECTRUM: str
    X_WAVENUMBER: str

    def __init__(self):
        super().__init__()

        self.Y_SPECTRUM = "spectra"
        self.X_WAVENUMBER = "axis_wavenumber"

        self.DATA_FORMAT_AVAILABLE_Y = [
            self.Y_SPECTRUM
        ]

        self.DATA_FORMAT_AVAILABLE_X = [
            self.X_WAVENUMBER
        ]


_CONST: ConstantsSpectroscopyFourierTransformIR = ConstantsSpectroscopyFourierTransformIR()

DefaultConfigY = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_Y,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_Y,
    instruction_unpack={"y": _CONST.Y_SPECTRUM},
    instruction_pack={"y": _CONST.Y_SPECTRUM},
    parent_class=ConstantsSpectroscopyFourierTransformIR
)

DefaultConfigMultipleY = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_MULTIPLE_YX,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_MULTIPLE_YX,
    instruction_unpack={"y": [_CONST.Y_SPECTRUM, _CONST.X_WAVENUMBER]},
    instruction_pack={"y": [_CONST.Y_SPECTRUM, _CONST.X_WAVENUMBER]},
    parent_class=ConstantsSpectroscopyFourierTransformIR
)


class ConstantsFTIR:
    constants: ConstantsSpectroscopyFourierTransformIR = ConstantsSpectroscopyFourierTransformIR()
    config_y: DefaultConfigY = DefaultConfigY
    config_multi_y: DefaultConfigMultipleY = DefaultConfigMultipleY
