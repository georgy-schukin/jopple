from tnodes.tree_node import TreeNode


class Program(TreeNode):
    def __init__(self, subs):
        """subs - list of subroutines"""
        super(TreeNode, self).__init__()
        self.subs = subs

    def get_children(self):
        return self.subs

    def to_json(self):
        return {
            "subs": [sub.to_json() for sub in self.subs]
        }

