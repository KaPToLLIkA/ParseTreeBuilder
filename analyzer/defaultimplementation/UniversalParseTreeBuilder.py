from analyzer.interfaces.IParseTreeBuilder import IParseTreeBuilder
from analyzer.model.TreeNode import TreeNode


class UniversalParseTreeBuilder(IParseTreeBuilder):
    def __init__(self):
        pass

    def build_tree(self):
        pass

    def _rec_build_tree(self, start_pos: int, current_node: TreeNode):
        pass
