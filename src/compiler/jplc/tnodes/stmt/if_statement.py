from tnodes.stmt.statement import Statement


class IfStatement(Statement):
    def __init__(self, cond, body, body_else=None):
        """cond - expression
        body, body_else - statements"""
        super(IfStatement, self).__init__()
        self.cond = cond
        self.body = body
        self.body_else = body_else

    def get_children(self):
        return [self.cond, self.body, self.body_else]

    def to_json(self):
        json = self._to_json("if", {
            "cond": self.cond.to_json(),
            "body": self.body.to_json(),
        })
        if self.body_else:
            json["body_else"] = self.body_else.to_json()
        return json
