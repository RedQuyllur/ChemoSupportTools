
from os import path, walk, mkdir, sep
from src.readers.operations_structure_files import FileOperations


class DirectoryOperations:
    """ Class collecting the basic directory operations.
    """

    @staticmethod
    def list_files(directory: str) -> list:
        """ Returns a list of files contained in the chosen directory.
        """
        files_list = []
        for root, dirs, files in walk(path.expanduser(directory), topdown=False):
            files_list.extend([path.join(root, name) for name in files])
        return files_list

    @staticmethod
    def list_folders(directory: str) -> list:
        """ Returns a list of folders in the chosen directory.
        """
        folders_list = []
        for root, dirs, files in walk(path.expanduser(directory), topdown=False):
            folders_list.extend([path.join(root, name) for name in dirs])
        return folders_list

    @staticmethod
    def create(directory: str) -> None:
        """ Create passed directory. Does work with nested structure.
        """
        if path.exists(directory):
            # If file in dir exist just clear file content
            FileOperations.create(directory)
        else:
            folder_path_head = path.split(directory)[0]
            folder_path_head = folder_path_head.split(sep)
            folder_path = sep
            for component in folder_path_head[1:]:
                folder_path = path.join(folder_path, component)
                if not path.exists(folder_path):
                    DirectoryOperations.create_folder(folder_path)
            FileOperations.create(directory)

    @staticmethod
    def create_folder(directory: str) -> None:
        try:
            mkdir(directory)
        except OSError:
            print("Creation of the directory %s failed\n" % directory)
        else:
            print("Successfully created the directory %s \n" % directory)
