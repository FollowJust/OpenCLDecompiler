from src.base_instruction import BaseInstruction
from src.decompiler_data import check_reg_for_val, set_reg_value


class VAlignbit(BaseInstruction):
    def __init__(self, node, suffix):
        super().__init__(node, suffix)
        self.vdst = self.instruction[1]
        self.src0 = self.instruction[2]
        self.src1 = self.instruction[3]
        self.src2 = self.instruction[4]

    def to_print_unresolved(self):
        if self.suffix == 'b32':
            self.decompiler_data.write(self.vdst + " = (((ulong)" + self.src0 + ") << 32) | " + self.src1
                                       + ") >> (" + self.src2 + " & 31) // v_alignbit_b32\n")
            return self.node
        return super().to_print_unresolved()

    def to_fill_node(self):
        if self.suffix == 'b32':
            self.src0, _ = check_reg_for_val(self.node, self.src0)
            self.src1, _ = check_reg_for_val(self.node, self.src1)
            self.src2, _ = check_reg_for_val(self.node, self.src2)
            new_value = 'amd_bitalign(' + self.src0 + ', ' + self.src1 + ', ' + self.src2 + ')'
            return set_reg_value(self.node, new_value, self.vdst, [self.src0, self.src1, self.src2], self.suffix)
        return super().to_fill_node()
