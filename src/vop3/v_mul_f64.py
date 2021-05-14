from src.base_instruction import BaseInstruction
from src.decompiler_data import DecompilerData
from src.operation_status import OperationStatus
from src.upload import find_first_last_num_to_from
from src.register import Register
from src.integrity import Integrity


class VMulF64(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData()
        output_string = ""
        vdst = instruction[1]
        src0 = instruction[2]
        src1 = instruction[3]
        if flag_of_status == OperationStatus.to_print_unresolved:
            decompiler_data.write(vdst + " = as_double(" + src0 + ") * as_double(" + src1 + ") // v_mul_f64\n")
            return node
        elif flag_of_status == OperationStatus.to_fill_node:
            _, _, _, name_of_from, first_from, last_from \
                = find_first_last_num_to_from(vdst, src0)
            from_registers_src0 = name_of_from + str(first_from)
            first_to, last_to, name_of_to, name_of_from, first_from, last_from \
                = find_first_last_num_to_from(vdst, src1)
            from_registers_src1 = name_of_from + str(first_from)
            to_registers = name_of_to + str(first_to)
            suffix = node.state.registers[from_registers_src0].type_of_data
            decompiler_data.names_of_vars[node.state.registers[from_registers_src0].val] = suffix
            type_reg = node.state.registers[from_registers_src0].type
            new_val = node.state.registers[from_registers_src0].val
            node.state.registers[to_registers] = Register(new_val, type_reg, Integrity.entire)
            decompiler_data.make_version(node.state, to_registers)
            if node.state.registers[to_registers].type_of_data is None:
                node.state.registers[to_registers].type_of_data = suffix
            return node
        return output_string
