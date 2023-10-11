
import os.path

import pandas as pd
import json

from src.readers.paths import Paths
from src.readers.operations_structure import StructureOperations


class BasicReader:
    """
    #TODO Complete Docstring
    """

    """ PROJECT DIRECTORIES HINTS
    """
    DIRECTORIES: Paths = Paths()

    """ CONFIGURATIONS TEMPLATES
    """

    _file_formats_load: list = [".pkl", ".json", ".csv"]
    _file_formats_save: list = [".pkl", ".json"]
    _url_formats: list = [".json", ".csv"]

    """ CONFIGURATIONS: LOAD
    """
    _configuration_load_local: dict = {
        "source": "local",
        "dir": DIRECTORIES.DATASETS.get("raw"),
        "file_name": "",
        "file_format": ".pkl"
    }

    _configuration_load_url: dict = {
        "source": "url",
        "url": "",
        "file_format": ".json"
    }

    _available_sources: dict = {
        "file": _file_formats_load,
        "url": _url_formats,
    }

    """ CONFIGURATIONS: SAVE
    """

    _configuration_save_local: dict = {
        "source": "local",
        "dir": DIRECTORIES.DATASETS.get("custom"),
        "file_name": "tmp.pkl",
        "file_format": ".pkl"
    }

    """ FORMAT TEMPLATES
    """
    _DATA_DESCRIPTOR: dict = {
        "dataset_type": "",
        "release_date": "",
        "source": "",
        "comment": ""
    }

    _FORMAT_SAVE: dict = {
        "data": dict,
        "data_descriptor": _DATA_DESCRIPTOR,
    }

    """ CONTAINERS
    """
    _configuration_load: dict = _configuration_load_local
    _configuration_save: dict = _configuration_save_local
    _data_descriptor: dict
    _data: pd.DataFrame or dict or list or str

    def __init__(
            self,
            load_data_on_init: bool = True,
            configuration_load: dict = None,
            configuration_save: dict = None,
    ):
        self.data_descriptor = self._DATA_DESCRIPTOR
        if configuration_load:
            self.configuration_load = configuration_load
            if load_data_on_init:
                self.load_data()
        if configuration_save:
            self.configuration_save = configuration_save

    """ CONFIGURATIONS Decorators/Accessors
    """

    @property
    def data(self) -> dict:
        """ Configuration accessor.

        Returns:
            (dict): Returns data dictionary.
        """
        return self._data

    @data.setter
    def data(self, data: dict) -> None:
        self._data = data

    @property
    def data_descriptor(self) -> dict:
        """
        #TODO Complete docstring property
        """
        return self._data_descriptor.copy()

    @data_descriptor.setter
    def data_descriptor(self, data_descriptor: dict) -> None:
        self._data_descriptor = data_descriptor.copy()

    @property
    def configuration_load(self) -> dict:
        """
        #TODO Complete docstring property
        """
        return self._configuration_load.copy()

    @configuration_load.setter
    def configuration_load(self, configuration: dict) -> None:
        if "source" in configuration.keys():
            source = configuration.get("source")
        else:
            source = self._recognize_source_by_configuration_keys(configuration=configuration)
            if not source:
                raise ValueError(f"Source not recognized.")
        if source in self._available_sources:
            # Rebase configuration dictionary if source is changed
            if source != self._configuration_load.get("source"):
                if source == "file":
                    self._configuration_load = self._configuration_load_local
                elif source == "url":
                    self._configuration_load = self._configuration_load_url
            # Passing configuration keys check
            for key, _ in configuration.items():
                if key not in self._configuration_load.keys():
                    raise ValueError(f"Invalid key: <{key}>")

            self._configuration_load.update(configuration)
        else:
            raise ValueError(f"<{source}> not supported.")

    @property
    def configuration_save(self) -> dict:
        return self._configuration_save.copy()

    @configuration_save.setter
    def configuration_save(self, configuration: dict) -> None:
        for key, _ in configuration.items():
            if key not in self._configuration_save.keys():
                raise ValueError(f"Invalid key: <{key}>")
        self._configuration_save.update(configuration)

    """ Class/instance methods
    """

    def load_data(self):
        source = self._configuration_load.get("source")
        if source in self._available_sources:
            if source == "file":
                self.data_load_from_file()
            elif source == "url":
                self.data_load_from_url()
            elif source == "database":
                raise NotImplementedError()
        else:
            raise ValueError(f"<{source}> not supported.")

    def data_load_from_file(self):

        directory: str = self._configuration_load.get("dir")
        file_name: str = self._configuration_load.get("file_name")
        file_format: str = self._configuration_load.get("file_format")

        if not file_format:
            file_format = self._get_format_from_str(
                file_name, self._file_formats_load)
            if file_format:
                self._configuration_load.update("file_format")
            else:
                raise ValueError("File format must be specified!")

        load_directory = os.path.join(directory, file_name)
        if not file_name.endswith(file_format):
            load_directory += file_format

        if not os.path.exists(load_directory):
            raise FileNotFoundError(f"Passed directory does not exist:\n {load_directory}")
        else:
            if ".pkl" in file_format:
                data_loaded = self._file_open_pkl(directory=load_directory)
                self._update_containers(data_loaded)
            elif ".json" in file_format:
                data_loaded = self._file_open_json(directory=load_directory)
                self._update_containers(data_loaded)
            else:
                raise ValueError(f"Passed format <{file_format}>is not supported.")

    def data_load_from_url(self):
        file_format = self.configuration_load.get("file_type")
        url = self.configuration_load.get("url")

        if not file_format:
            file_format = self._get_format_from_str(
                url, self._file_formats_load)
            if file_format:
                self._configuration_load.update({"file_format": file_format})
            else:
                raise ValueError("Save format must be specified!")

        if file_format == ".csv":
            self.data = pd.read_csv(url)
            descriptor = self._DATA_DESCRIPTOR
            descriptor.update({
                "source": {"url": url},
                "comment": "Data pulled from url."
            })
            self._data_descriptor = descriptor
        elif file_format == ".json":
            self.data = pd.read_json(url)
            descriptor = self._DATA_DESCRIPTOR
            descriptor.update({
                "source": {"url": url},
                "comment": "Data pulled from url."
            })
            self._data_descriptor = descriptor
        else:
            raise ValueError(f"File type <{file_format}> not supported.")

    def data_save(self):

        directory: str = self._configuration_save.get("dir")
        file_name: str = self._configuration_save.get("file_name")
        file_format: str = self._configuration_save.get("file_format")

        if not file_format:
            file_format = self._get_format_from_str(
                file_name, self._file_formats_save)
            if file_format:
                self._configuration_save.update("file_format")
            else:
                raise ValueError("Save format must be specified!")

        save_directory = os.path.join(directory, file_name)
        if not file_name.endswith(file_format):
            save_directory += file_format

        if self._overwrite_protection(save_dir=save_directory):
            data_to_save = {
                "data": self.data,
                "data_descriptor": self.data_descriptor
            }
            if ".pkl" in file_format:
                self._file_save_pkl(
                    directory=save_directory,
                    data=data_to_save
                )
            elif ".json" in file_format:
                self._file_save_json(
                    directory=save_directory,
                    data=data_to_save
                )
            else:
                raise ValueError("Passed format is not supported.")

    """ Static methods/partials
    """

    @staticmethod
    def _file_open_json(directory: str) -> dict:
        # Opening JSON file
        with open(directory, 'r') as openfile:
            return json.load(openfile)

    @staticmethod
    def _file_save_json(data: dict, directory: str) -> None:
        StructureOperations.directory.create(directory)
        with open(directory, "w") as outfile:
            json.dump(data, outfile)

    @staticmethod
    def _file_open_pkl(directory: str) -> pd.DataFrame or dict:
        return StructureOperations.file.open_pkl(directory=directory)

    @staticmethod
    def _file_save_pkl(data: dict or pd.DataFrame, directory: str) -> None:
        StructureOperations.directory.create(directory)
        StructureOperations.file.save_pkl(data=data, directory=directory)

    """ Security methods
    """

    def _update_containers(self, data):
        if self._check_format_descriptor(data=data):
            self.data = data.get("data")
            self.data_descriptor = data.get("data_descriptor")
        else:
            self.data = data
            self.data_descriptor = {
                "comment": "Unknown dataset. Descriptor not included.",
            }

    @staticmethod
    def _get_format_from_str(string, supported_formats) -> str or None:
        for file_format in supported_formats:
            if string.endswith(file_format):
                return file_format

    def _check_format_descriptor(self, data: dict) -> bool:
        if set(data) == set(self._FORMAT_SAVE):
            return True
        else:
            return False

    @staticmethod
    def _overwrite_protection(save_dir) -> bool:
        if os.path.exists(save_dir):
            print(f"Passed directory does exist: {save_dir}")
            print(f"File will be overwritten. To continue?")
            overwrite_protection_question = input("Y/N\t")
            if overwrite_protection_question not in ("Y", "x_amp_spectra", "yes"):
                return False
        return True

    @staticmethod
    def _recognize_source_by_configuration_keys(configuration: dict) -> str or None:
        if "url" in configuration.keys():
            return "url"
        elif "file_name" in configuration.keys():
            return "file"
