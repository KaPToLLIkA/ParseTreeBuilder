import enum


@enum.unique
class RuleBodyElementType(enum.Enum):
    NEXT_RULE = enum.auto(),
    VALUE = enum.auto(),


class RuleBodyElement:
    def __init__(self, string: str, element_type: RuleBodyElementType):
        self.element_type = element_type
        self.string = string
