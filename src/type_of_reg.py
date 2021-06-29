from enum import Enum, auto


class Type(Enum):
    unknown = auto()
    global_id_x = auto()
    global_id_y = auto()
    global_id_z = auto()
    work_group_id_x = auto()
    work_group_id_y = auto()
    work_group_id_z = auto()
    work_item_id_x = auto()
    work_item_id_y = auto()
    work_item_id_z = auto()
    global_offset_x = auto()
    global_offset_y = auto()
    global_offset_z = auto()
    global_data_pointer = auto()
    arguments_pointer = auto()
    work_group_id_x_local_size = auto()
    work_group_id_y_local_size = auto()
    work_group_id_z_local_size = auto()
    work_group_id_x_local_size_offset = auto()
    work_group_id_y_local_size_offset = auto()
    work_group_id_z_local_size_offset = auto()
    work_group_id_x_work_item_id = auto()
    work_group_id_y_work_item_id = auto()
    work_group_id_z_work_item_id = auto()
    param_global_id_x = auto()
    param_global_id_y = auto()
    param_global_id_z = auto()
    local_size_x = auto()
    local_size_y = auto()
    local_size_z = auto()
    global_size_x = auto()
    global_size_y = auto()
    global_size_z = auto()
    param = auto()
    paramA = auto()
    program_param = auto()
    int32 = auto()
    work_dim = auto()
    general_setup = auto()
