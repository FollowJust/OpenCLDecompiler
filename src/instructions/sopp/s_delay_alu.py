from src.base_instruction import BaseInstruction


class SDelayAlu(BaseInstruction):
    def to_fill_node(self):
        return self.node
