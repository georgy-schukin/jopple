from tnodes.tree_node import TreeNode


class Param(TreeNode):
    def __init__(self, param_type, name):
        super(Param, self).__init__()
        self.type = param_type
        self.name = name

    def to_json(self):
        return {
            "type": self.type,
            "id": self.name
        }
