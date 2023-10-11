from os import path
import pandas as pd

from src.readers.basic_reader import BasicReader
from src.processing.processing_methods import *
from src.processing.format.data_wrapper_constants import DataFoldsConstants
from src.helpers.paths import Paths


def main():
    CONSTANTS = DataFoldsConstants.spectro.nmr
    config_local = {
        "root_dir_load": path.join(Paths.DATASETS.get("processed"), "nmr_spectra"),
        "root_dir_save": path.join(Paths.DATASETS.get("processed"), "nmr_spectra"),
        "file_name": "coffee_survey_spectra_prepared",
        "file_format": ".pkl",
    }
    reader = BasicReader(
        load_data_on_init=True,
        load_data_on_init_source="local",
        configuration_local=config_local
    )
    dataset_pkl = reader.data
    dataset = pd.DataFrame(dataset_pkl.get("fold0"))

    axis_chem_shift_range = [3.1, 3.7]
    axis_chem_shift = dataset.get("axis_chem_shift")[0]

    def closest(lst, value):
        return min(range(len(lst)), key=lambda i: abs(lst[i] - value))

    axis_chem_shift_range = tuple([closest(axis_chem_shift, shift) for shift in axis_chem_shift_range])

    data_format = {
        "unpack": {
            CONSTANTS.PROCESS_DATA_AS_MULTIPLE_YX: {
                "y": [CONSTANTS.Y_SPECTRUM, CONSTANTS.X_CHEM_SHIFT]
            }},
        "pack": {
            CONSTANTS.PROCESS_DATA_AS_MULTIPLE_YX: {
                "y": [CONSTANTS.Y_SPECTRUM, CONSTANTS.X_CHEM_SHIFT]
            }}
    }

    closeup_region = Preprocessor.dimensions.cut_off_the_range(
        data=dataset_pkl, class_constants=CONSTANTS, data_format=data_format, cut_range = axis_chem_shift_range)
    print("end")

if __name__ == "__main__":
    main()
