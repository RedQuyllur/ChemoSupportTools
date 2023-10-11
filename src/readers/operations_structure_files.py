
import pickle
import mmap


class FileOperations:
    """ Class collecting the basic file operations.
    """

    @staticmethod
    def open_pkl(directory: str) -> dict:
        with open(directory, 'rb') as handle:
            return pickle.load(handle)

    @staticmethod
    def save_pkl(data: dict, directory: str) -> None:
        with open(directory, 'wb') as handle:
            pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def create(directory) -> None:
        with open(directory, "w") as file:
            file.close()

    @staticmethod
    def append(directory: str, text: str) -> None:
        with open(directory, "a") as file:
            file.write(text)
            file.close()

    @staticmethod
    def write(directory: str, text: str) -> None:
        with open(directory, "w") as file:
            file.write(text)
            file.close()

    @staticmethod
    def read(directory) -> list:
        with open(directory, "r") as file:
            data = [line for line in file]
            file.close()
        return data

    @staticmethod
    def get_length(directory) -> int:
        """ Fast method to check the number of lines inside the file.
        """
        with open(directory, "r+") as f:
            buf = mmap.mmap(f.fileno(), 0)
            lines = 0
            readline = buf.readline
            while readline():
                lines += 1
            return lines

    @staticmethod
    def name_unique(file_name: str, files_list: list) -> bool:
        """ Check that chosen file name exists in passed files list.
        """
        if file_name in files_list:
            return False
        else:
            return True

