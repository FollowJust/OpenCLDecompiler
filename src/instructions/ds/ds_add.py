from src.base_instruction import BaseInstruction
from src.decompiler_data import make_op, set_reg_value


class DsAdd(BaseInstruction):
    def __init__(self, node, suffix):
        super().__init__(node, suffix)
        self.addr = self.instruction[1]
        self.vdata0 = self.instruction[2]
        self.offset = int(self.instruction[3][7:]) if len(self.instruction) == 4 else 0  # noqa: PLR2004

        self.new_value = make_op(node, self.addr, "4", "/", suffix=self.suffix)
        self.varname = f"{self.decompiler_data.lds_vars[self.offset][0]}[{self.new_value}]"

    def to_print_unresolved(self):
        if self.suffix == "u32":
            v = f"V{self.decompiler_data.number_of_v}"
            self.decompiler_data.write(f"uint* {v} = (uint*)(DS + (({self.addr} + {self.offset})&~3)) // {self.name}\n")
            self.decompiler_data.write(f"*{v} = *{v} + {self.vdata0}  // atomic operation\n")
            self.decompiler_data.number_of_v += 1
            return self.node
        return super().to_print_unresolved()

    def to_fill_node(self):
        if self.suffix == "u32":
            new_value = f"{self.node.state[self.varname].val} + {self.node.state[self.vdata0].val}"
            return set_reg_value(self.node, new_value, self.varname, [], self.suffix)
        return super().to_fill_node()

    def to_print(self):
        if self.suffix == "u32":
            self.output_string = f"{self.varname} += {self.node.state[self.vdata0].val}"
            return self.output_string
        return super().to_print()
