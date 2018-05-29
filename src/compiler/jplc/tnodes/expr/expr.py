from tnodes.tree_node import TreeNode


class Expr(TreeNode):
    def __init__(self, expr_type):
        self.type = expr_type

    def _to_json(self, args={}):
        json = {
            "type": self.type
        }
        json.update(args)
        return json
