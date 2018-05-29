from tnodes.expr.expr import Expr


class TernaryExpr(Expr):
    def __init__(self, expr_type, cond, op1, op2):
        """cond, op1, op2 - expressions"""
        super(TernaryExpr, self).__init__(expr_type)
        self.cond = cond
        self.op1 = op1
        self.op2 = op2

    def get_children(self):
        return [self.cond, self.op1, self.op2]

    def to_json(self):
        return self._to_json({
            "operands": [self.cond.to_json(), self.op1.to_json(), self.op2.to_json()]
        })
