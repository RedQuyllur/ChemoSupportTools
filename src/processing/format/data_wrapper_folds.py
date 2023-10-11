
from src.processing.format.data_wrapper_format_pack import data_pack
from src.processing.format.data_wrapper_format_unpack import data_unpack
from src.processing.format.constants.constants_template import PreprocessorConfiguration


def process_fold_by_fold(
        function,
        instruction: PreprocessorConfiguration,
        data: dict,
        updated_kwargs
) -> dict:
    """ Fold processing method.

    This method pass data on chosen processing method, every line of chosen variables will be calculated independently.

    Args:
        function: Chosen processing method.
        instruction: Dictionary with pack/unpack instructions that determines way the data is passed on processing
            method.
        data: Dataset package in Preprocessor format.
        updated_kwargs: Updated settings passed on processing method.

    Returns: Processed dataset.

    """

    instruction_unpack_type, instruction_pack_type = instruction.get_instructions_type()
    instruction_unpack, instruction_pack = instruction.get_instructions()

    data_processed = {}
    for fold_name, fold_data in data.items():
        data_unpacked = data_unpack(instruction_unpack_type, fold_data, instruction_unpack, **updated_kwargs)
        result = [function(**data_dict) for data_dict in data_unpacked]
        updated_fold = data_pack(instruction_pack_type, fold_data, instruction_pack, result)
        data_processed.update({fold_name: updated_fold})
    return data_processed

