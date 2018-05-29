from tnodes.tree_node import TreeNode


class Statement(TreeNode):
    def _to_json(self, stmt_type, args={}):
        json = {
            "type": stmt_type
        }
        json.update(args)
        return json
