
class PreprocessorConstants:
    """ Class provided for constants.py collection used in wrapper instructions.
    """

    PROCESS_DATA_AS_Y: int
    PROCESS_DATA_AS_MULTIPLE_YX: int
    PROCESS_DATA_AS_Y_OF_X: int

    DATA_FORMAT_AVAILABLE_UNPACK: list

    DATA_FORMAT_AVAILABLE_PACK: list

    DATA_FORMAT_AVAILABLE_Y: list

    DATA_FORMAT_AVAILABLE_X: list

    def __init__(self):
        self.PROCESS_DATA_AS_Y = 0
        self.PROCESS_DATA_AS_MULTIPLE_YX = 1
        self.PROCESS_DATA_AS_Y_OF_X = 2

        self.DATA_FORMAT_AVAILABLE_UNPACK = [
            self.PROCESS_DATA_AS_Y,
            self.PROCESS_DATA_AS_MULTIPLE_YX,
            self.PROCESS_DATA_AS_Y_OF_X
        ]

        self.DATA_FORMAT_AVAILABLE_PACK = [
            self.PROCESS_DATA_AS_Y,
            self.PROCESS_DATA_AS_MULTIPLE_YX
        ]

        self.DATA_FORMAT_AVAILABLE_Y = []

        self.DATA_FORMAT_AVAILABLE_X = []

    def instruction_check(self, instruction: str) -> None:
        if instruction not in (self.DATA_FORMAT_AVAILABLE_Y+self.DATA_FORMAT_AVAILABLE_X):
            raise ValueError(f"Instruction: <{instruction}> not allowed.")


def PreprocessorConfiguration(
    instruction_type_unpack: int,
    instruction_type_pack: int,
    instruction_unpack: dict,
    instruction_pack: dict,
    parent_class: type(PreprocessorConstants) = PreprocessorConstants,
    security_check: bool = False
) -> object:
    """ Mutable parent class wrapper for PreprocConfig class.
    #TODO Complete docstring
    Args:
        instruction_type_unpack (int):
        instruction_type_pack (int):
        instruction_unpack (dict):
        instruction_pack (dict):
        security_check (bool): Turn on/off security checks.
        parent_class:

    Return:
        (object)
    """
    class PreprocConfig(parent_class):

        security_check: bool

        instruction_type_unpack: int
        instruction_type_pack: int

        instruction_unpack: dict
        instruction_pack: dict

        _STRUCTURE_Y: dict = {
            "y": "signal"
        }
        _STRUCTURE_MULTIPLE_Y: dict = {
            "y": ["signal"]
        }
        _STRUCTURE_Y_OF_X: dict = {
            "y": "signal",
            "x": "x_axis"
        }

        def __init__(
                self,
                _instruction_type_unpack: int,
                _instruction_type_pack: int,
                _instruction_unpack: dict,
                _instruction_pack: dict,
                _security_check: bool
        ):
            if issubclass(self.__class__, PreprocessorConstants):
                super().__init__()
            else:
                raise ValueError(f"Passed object {parent_class} does not meet requirements.")

            self.security_check = _security_check
            self.instruction_type_unpack = _instruction_type_unpack
            self.instruction_type_pack = _instruction_type_pack
            self.instruction_unpack = _instruction_unpack
            self.instruction_pack = _instruction_pack

        def get_instructions_type(self) -> tuple:
            return self.instruction_type_unpack, self.instruction_type_pack

        def get_instructions(self) -> tuple:
            return self.instruction_unpack, self.instruction_pack

    return PreprocConfig(
        _instruction_type_unpack=instruction_type_unpack,
        _instruction_type_pack=instruction_type_pack,
        _instruction_unpack=instruction_unpack,
        _instruction_pack=instruction_pack,
        _security_check=security_check
    )

