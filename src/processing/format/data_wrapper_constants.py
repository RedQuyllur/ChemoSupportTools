
from src.processing.format.constants.constants_spectroscopy_ftir import ConstantsFTIR
from src.processing.format.constants.constants_spectroscopy_nmr import ConstantsNMR
from src.processing.format.constants.constants_calorimetry import ConstantsCalorimetry


class DataFoldsConstantsSpectroscopy:
    nmr: ConstantsNMR = ConstantsNMR()
    ftir: ConstantsFTIR = ConstantsFTIR()


class DataFoldsConstants:
    spectro: DataFoldsConstantsSpectroscopy = DataFoldsConstantsSpectroscopy()
    calorimetry: ConstantsCalorimetry = ConstantsCalorimetry()
