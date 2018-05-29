from tnodes.stmt.statement import Statement


class CFStatement(Statement):
    def __init__(self, cf_id, code_name, args):
        """id - id expression
        code_name - string
        args - list of arguments"""
        super(CFStatement, self).__init__()
        self.id = cf_id
        self.code_name = code_name
        self.args = args

    def get_children(self):
        return [self.id] + self.args

    def to_json(self):
        return self._to_json("exec", {
            "id": self.id.to_json(),
            "code": self.code_name,
            "args": [arg.to_json() for arg in self.args]
        })
