import re
from typing import List, Optional

from ..utils import ConfigData, KernelArgument


def process_size_of_work_groups(set_of_config: List[str]) -> Optional[List[int]]:
    cws: bool = ".cws" in set_of_config[1]
    return list(map(int, set_of_config[1].replace(',', ' ').split()[1:])) if cws else None


def process_local_size(set_of_config: List[str]) -> Optional[int]:
    localsize: bool = "localsize" in set_of_config[4]
    return int(set_of_config[4][11:]) if localsize else None


def process_arg_row(row: str) -> KernelArgument:
    _, arg_name, _, arg_type, *other = row.strip().replace(',', ' ').split()
    if len(other) > 0:
        arg_type = "__" + other[0] + " " + arg_type
    if arg_type[-1] == "*":
        arg_type = arg_type[:-1]
        arg_name = "*" + arg_name
    return KernelArgument(
        type_name=arg_type,
        name=arg_name,
        offset=None,
    )


def process_params(set_of_config: List[str]) -> List[KernelArgument]:
    return [process_arg_row(row) for row in set_of_config if ".arg" in row and "_." not in row]


def get_setup_params_offsets(set_of_config: List[str]) -> List[str]:
    return [
        hex(i * 8) for i, row in
        enumerate(row for row in set_of_config if ".arg" in row)
        if row.startswith('.arg _.')
    ]


def process_config(set_of_config: List[str]) -> ConfigData:
    return ConfigData(
        dimensions=set_of_config[0][6:],
        usesetup=".usesetup" in set_of_config,
        size_of_work_groups=process_size_of_work_groups(set_of_config),
        local_size=process_local_size(set_of_config),
        arguments=process_params(set_of_config),
        setup_params_offsets=get_setup_params_offsets(set_of_config),
    )


def get_global_data_bytes(row, set_of_global_data_bytes):
    line_of_bytes = row.split()
    if line_of_bytes.pop(0) == ".fill":
        amount = line_of_bytes[0][:-1]
        value = line_of_bytes[2]
        expand_list = [value for _ in range(int(amount))]
        set_of_global_data_bytes += expand_list
    else:
        for i, elem in enumerate(line_of_bytes):
            line_of_bytes[i] = re.sub(",", "", elem)
        set_of_global_data_bytes += line_of_bytes
    return set_of_global_data_bytes


def parse_kernel(text):
    status_of_parse = "start"
    set_of_instructions = []
    set_of_global_data_instruction = []
    set_of_config = []
    set_of_global_data_bytes = []
    name_of_program = ""
    for row in text:
        row = re.sub(r"/\*(.*?)\*/", "", row)
        row = row.strip()
        if ".kernel " in row:
            if status_of_parse == "instruction":
                status_of_parse = "kernel"
                yield (name_of_program, process_config(set_of_config), set_of_instructions,
                       set_of_global_data_bytes, set_of_global_data_instruction)
                set_of_instructions = []
                set_of_config = []
            name_of_program = row.split()[1]
        if row == ".config":
            status_of_parse = "config"
        elif row == ".text":
            status_of_parse = "instruction"
        elif row == ".gdata:":
            status_of_parse = "global_data"
        elif status_of_parse == "instruction":
            if ".gdata" in row:
                set_of_global_data_instruction.append(row)
            set_of_instructions.append(row)
        elif status_of_parse == "config":
            set_of_config.append(row)
        elif status_of_parse == "global_data":
            set_of_global_data_bytes = \
                get_global_data_bytes(row, set_of_global_data_bytes)
    yield name_of_program, process_config(set_of_config), set_of_instructions, \
        set_of_global_data_bytes, set_of_global_data_instruction
