from tnodes.tree_node import TreeNode


class Sub(TreeNode):
    def __init__(self, sub_type, name, params):
        super(Sub, self).__init__()
        self.type = sub_type
        self.name = name
        self.params = params

    def _to_json(self, args={}):
        json = {
            "type": self.type,
            "name": self.name,
            "params": [p.to_json() for p in self.params]
        }
        json.update(args)
        return json

