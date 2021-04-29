from src.base_instruction import BaseInstruction
from src.decompiler_data import DecompilerData
from src.operation_status import OperationStatus
from src.upload import upload_usesetup, upload, find_first_last_num_to_from
from src.type_of_reg import Type
from src.global_data import get_gdata_offset


class SLoad(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData()
        output_string = ""
        sdata = instruction[1]
        sbase = instruction[2]
        offset = instruction[3]
        to_registers = sdata
        left_board_to = to_registers.find("[")
        first_to, last_to, name_of_to, name_of_from, first_from, last_from \
            = find_first_last_num_to_from(sdata, sbase)
        from_registers = name_of_from + str(first_from)
        if left_board_to != -1:
            separation_to = to_registers.index(":")
            first_to = int(to_registers[(left_board_to + 1):separation_to])
            name_of_to = to_registers[:left_board_to]
            to_registers = name_of_to + str(first_to)

        if suffix == 'dword':
            if flag_of_status == OperationStatus.to_print_unresolved:
                decompiler_data.write(sdata + " = *(uint*)(smem + (" + offset + " & ~3)) // s_load_dword\n")
                return node
            if flag_of_status == OperationStatus.to_fill_node:
                if (node.state.registers[from_registers] is not None and node.state.registers[
                    from_registers].type == Type.global_data_pointer) \
                        or decompiler_data.usesetup is False and sbase == "s[4:5]" \
                        or decompiler_data.usesetup is True and sbase == "s[6:7]":
                    upload(node.state, sdata, sbase, offset, decompiler_data.kernel_params)
                else:
                    upload_usesetup(node.state, sdata, offset)
                if (node.state.registers[from_registers] is not None and node.state.registers[
                    from_registers].type == Type.global_data_pointer):
                    data_type = node.state.registers[from_registers].type_of_data
                    id = get_gdata_offset(node.state.registers[from_registers].val)
                else:
                    node.state.registers[to_registers].type_of_data = suffix
                return node
            return output_string

        elif suffix == 'dwordx2':
            if flag_of_status == OperationStatus.to_print_unresolved:
                decompiler_data.write(sdata + " = *(ulong*)(smem + (" + offset + " & ~3)) // s_load_dwordx2\n")
                return node
            if flag_of_status == OperationStatus.to_fill_node:
                if (node.state.registers[from_registers] is not None and node.state.registers[
                    from_registers].type == Type.global_data_pointer) \
                        or decompiler_data.usesetup is False and sbase == "s[4:5]" \
                        or decompiler_data.usesetup is True and sbase == "s[6:7]":
                    upload(node.state, sdata, sbase, offset, decompiler_data.kernel_params)
                else:
                    upload_usesetup(node.state, sdata, offset)
                if (node.state.registers[from_registers] is not None and node.state.registers[
                    from_registers].type == Type.global_data_pointer):
                    data_type = node.state.registers[from_registers].type_of_data
                    id = get_gdata_offset(node.state.registers[from_registers].val)
                else:
                    node.state.registers[to_registers].type_of_data = suffix
                return node
            return output_string

        elif suffix == 'dwordx4' or suffix == 'dwordx8':
            if flag_of_status == OperationStatus.to_print_unresolved:
                i_cnt = suffix[-1]
                decompiler_data.write("for (BYTE i = 0; i < " + i_cnt + "; i++) // s_load_dword" + i_cnt + "\n")
                decompiler_data.write("    " + sdata + "[i] = *(uint*)(SMEM + i*4 + (" + offset + " & ~3))\n")
                return node
            if flag_of_status == OperationStatus.to_fill_node:
                if decompiler_data.usesetup is False and sbase == "s[4:5]" \
                        or decompiler_data.usesetup is True and sbase == "s[6:7]":
                    upload(node.state, sdata, sbase, offset, decompiler_data.kernel_params)
                else:
                    upload_usesetup(node.state, sdata, offset)
                node.state.registers[to_registers].type_of_data = suffix
                return node
            return output_string
