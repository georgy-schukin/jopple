from tnodes.tree_node import TreeNode


class Arg(TreeNode):
    def __init__(self, name, value):
        """name - string
        value - expression"""
        super(Arg, self).__init__()
        self.name = name
        self.value = value

    def get_children(self):
        return [self.value]

    def to_json(self):
        return {
            "name": self.name,
            "value": self.value.to_json()
        }
