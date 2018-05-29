from tnodes.expr.expr import Expr


class BinaryExpr(Expr):
    def __init__(self, expr_type, op1, op2):
        super(BinaryExpr, self).__init__(expr_type)
        self.op1 = op1
        self.op2 = op2

    def get_children(self):
        return [self.op1, self.op2]

    def to_json(self):
        return self._to_json({
            "operands": [self.op1.to_json(), self.op2.to_json()]
        })
    