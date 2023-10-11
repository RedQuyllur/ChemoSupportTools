
from src.processing.format.constants.constants_template import *


class ConstantsSpectroscopyNuclearMagneticResonance(PreprocessorConstants):

    Y_SPECTRUM: str
    X_CHEM_SHIFT: str

    def __init__(self):
        super().__init__()
        self.Y_SPECTRUM = "spectra"
        self.X_CHEM_SHIFT = "axis_chem_shift"

        self.DATA_FORMAT_AVAILABLE_Y = [
            self.Y_SPECTRUM
        ]

        self.DATA_FORMAT_AVAILABLE_X = [
            self.X_CHEM_SHIFT
        ]


_CONST: ConstantsSpectroscopyNuclearMagneticResonance = ConstantsSpectroscopyNuclearMagneticResonance()

DefaultConfigY = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_Y,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_Y,
    instruction_unpack={"y": _CONST.Y_SPECTRUM},
    instruction_pack={"y": _CONST.Y_SPECTRUM},
    parent_class=ConstantsSpectroscopyNuclearMagneticResonance
)

DefaultConfigMultipleY = PreprocessorConfiguration(
    instruction_type_unpack=_CONST.PROCESS_DATA_AS_MULTIPLE_YX,
    instruction_type_pack=_CONST.PROCESS_DATA_AS_MULTIPLE_YX,
    instruction_unpack={"y": [_CONST.Y_SPECTRUM, _CONST.X_CHEM_SHIFT]},
    instruction_pack={"y": [_CONST.Y_SPECTRUM, _CONST.X_CHEM_SHIFT]},
    parent_class=ConstantsSpectroscopyNuclearMagneticResonance
)


class ConstantsNMR:
    constants: ConstantsSpectroscopyNuclearMagneticResonance = ConstantsSpectroscopyNuclearMagneticResonance()
    config_y: DefaultConfigY = DefaultConfigY
    config_multi_y: DefaultConfigMultipleY = DefaultConfigMultipleY
