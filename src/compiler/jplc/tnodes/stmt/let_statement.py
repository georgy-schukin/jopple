from tnodes.stmt.statement import Statement


class LetStatement(Statement):
    def __init__(self, args, body):
        """args - list of arguments
        body - statement"""
        super(LetStatement, self).__init__()
        self.args = args
        self.body = body

    def get_children(self):
        return self.args + [self.body]

    def to_json(self):
        return self._to_json("let", {
            "args": [arg.to_json() for arg in self.args],
            "body": self.body.to_json()
        })
