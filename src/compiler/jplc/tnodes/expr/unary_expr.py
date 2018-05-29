from tnodes.expr.expr import Expr


class UnaryExpr(Expr):
    def __init__(self, expr_type, op):
        super(UnaryExpr, self).__init__(expr_type)
        self.op = op

    def get_children(self):
        return [self.op]

    def to_json(self):
        return self._to_json({
            "operands": [self.op.to_json()]
        })
