

class TreeNode:
    def __init__(self, node_value="", child_s=None):
        if child_s is None:
            child_s = []
        self.node_value = node_value
        self._child_s = child_s

    def add_child(self, child):
        self._child_s.append(child)

    def get_child_s(self):
        return self._child_s
