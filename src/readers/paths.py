
from os import path
from definitions import ROOT_DIR
from src.readers.operations_structure import StructureOperations


class Paths:
    """ Class created for paths management.
    """

    DIR_ROOT = ROOT_DIR
    DIR_DATA = path.join(DIR_ROOT, "data")
    DIR_DATASETS = path.join(DIR_DATA, "datasets")
    DIR_RESULTS = path.join(DIR_DATA, "results")

    DATASETS = {
        "raw":  path.join(DIR_DATASETS, "raw"),
        "processed":    path.join(DIR_DATASETS, "processed"),
        "custom":   path.join(DIR_DATASETS, "custom")
    }

    @classmethod
    def create_project_dir(cls):
        """ Create data nested folder structure in project root.
        """
        for container_path in cls.DATASETS.values():
            StructureOperations.directory.create(container_path)
