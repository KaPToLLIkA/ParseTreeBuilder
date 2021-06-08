from analyzer.model.TreeNode import TreeNode


class IParseTreeBuilder:
    def build_tree(self):
        pass

    def _rec_build_tree(self, start: int, end: int, current_node: TreeNode):
        pass
