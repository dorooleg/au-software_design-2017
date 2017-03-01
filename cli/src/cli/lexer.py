from enum import Enum

class LexemType(Enum):
    pass


class Lexem:

    def __init__(self, tp, val, start_idx, end_idx):
        pass

    def get_value(self):
        pass

    def get_type(self):
        pass

    def get_position(self):
        pass


class Lexer:

    @staticmethod
    def get_lexems(raw_str):
        pass
