
from src.readers.operations_structure_files import FileOperations
from src.readers.operations_structure_directory import DirectoryOperations
from src.readers.operations_variable import VariableOperations


class StructureOperations:
    """ Class collecting the basic files, paths, and structure operations.
    """

    file: FileOperations = FileOperations()
    directory: DirectoryOperations = DirectoryOperations()
    var: VariableOperations = VariableOperations()
