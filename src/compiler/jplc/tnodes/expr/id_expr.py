from tnodes.expr.expr import Expr


class IdExpr(Expr):
    def __init__(self, name, indices=[]):
        """name - id (string)
        indices - list of expressions"""
        super(IdExpr, self).__init__("id")
        self.name = name
        self.indices = indices

    def get_children(self):
        return self.indices

    def to_json(self):
        return self._to_json({
            "ref": [self.name] + [ind.to_json() for ind in self.indices]
        })
