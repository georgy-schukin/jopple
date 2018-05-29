from tnodes.stmt.statement import Statement


class WhileStatement(Statement):
    def __init__(self, var_name, start, cond, body, out=None):
        """var_name - name of loop variable (string)
        start - expression
        cond - expression
        body - statement
        out - out variable (expression)"""
        super(WhileStatement, self).__init__()
        self.var = var_name
        self.cond = cond
        self.start = start
        self.body = body
        self.out = out

    def get_children(self):
        return [self.cond, self.body, self.out]

    def to_json(self):
        json = self._to_json("while", {
            "var": self.var,
            "cond": self.cond.to_json(),
            "start": self.start.to_json(),
            "body": self.body.to_json()
        })
        if self.out:
            json["out"] = self.out.to_json()
        return json
