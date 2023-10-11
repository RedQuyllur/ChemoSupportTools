
from src.processing.format.data_wrapper_constants import DataFoldsConstants

from src.processing.methods.filter import Filter
from src.processing.methods.baseline import Baseline
from src.processing.methods.dimmensions import Dimensions


class Preprocessor:
    """ Class for containing various processing methods.
    """
    CONST: DataFoldsConstants = DataFoldsConstants()
    filter: Filter = Filter()
    baseline: Baseline = Baseline()
    dimensions: Dimensions = Dimensions()
