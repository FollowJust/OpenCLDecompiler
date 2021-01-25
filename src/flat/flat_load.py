from src.base_instruction import BaseInstruction
from src.decompiler_data import DecompilerData
from src.integrity import Integrity
from src.register import Register
from src.type_of_reg import Type
from src.operation_status import OperationStatus
from src.upload import find_first_last_num_to_from


class FlatLoad(BaseInstruction):
    def execute(self, node, instruction, flag_of_status, suffix):
        decompiler_data = DecompilerData()
        if suffix == "dword":
            vdst = instruction[1]
            vaddr = instruction[2]
            inst_offset = instruction[3] if len(instruction) > 3 else "0"
            if flag_of_status == OperationStatus.to_print_unresolved:
                decompiler_data.write(vdst + " = *(uint*)(" + vaddr + " + " + inst_offset + ") // flat_load_dword \n")
                # decompiler_data.write(instruction + "  # " + to_registers + " = " + variable + "\n")
                return node
            variable = "var" + str(decompiler_data.num_of_var)
            first_to, last_to, name_of_to, name_of_from, first_from, last_from \
                = find_first_last_num_to_from(vdst, vaddr)
            from_registers = name_of_from + str(first_from)
            to_registers = name_of_to + str(first_to)
            if flag_of_status == OperationStatus.to_fill_node:
                if inst_offset == "0":
                    if first_to == last_to:
                        data_type = node.state.registers[from_registers].type_of_data
                        node.state.registers[to_registers] = \
                            Register(variable, Type.program_param, Integrity.integer)
                        decompiler_data.make_version(node.state, to_registers)
                        node.state.registers[to_registers].type_of_data = data_type
                        node.state.registers[to_registers].val = variable
                        decompiler_data.make_var(node.state.registers[to_registers].version, variable,
                                                 node.state.registers[from_registers].type_of_data)
                return node
            output_string = node.state.registers[to_registers].val + " = " + \
                node.parent[0].state.registers[from_registers].val
            return output_string

        elif suffix == "dwordx4":
            vdst = instruction[1]
            vaddr = instruction[2]
            inst_offset = instruction[3] if len(instruction) > 3 else ""
            if flag_of_status == OperationStatus.to_print_unresolved:
                vm = "vm" + str(decompiler_data.number_of_vm)
                decompiler_data.write("short* " + vm + " = (" + vaddr + " + "
                                      + inst_offset + ") // flat_load_dwordx4 \n")
                decompiler_data.write(vdst + "[0] = *(uint*)" + vm + "\n")
                decompiler_data.write(vdst + "[1] = *(uint*)(" + vm + " + 4)\n")
                decompiler_data.write(vdst + "[2] = *(uint*)(" + vm + " + 8)\n")
                decompiler_data.write(vdst + "[3] = *(uint*)(" + vm + " + 12)\n")
                decompiler_data.number_of_vm += 1
                return node
