from tnodes.stmt.statement import Statement


class ForStatement(Statement):
    def __init__(self, index_name, start, end, step, body):
        """index_name - name of index var (string)
        start, end, step - expressions
        body - statement"""
        super(ForStatement, self).__init__()
        self.index_name = index_name
        self.start = start
        self.end = end
        self.step = step
        self.body = body

    def get_children(self):
        return [self.start, self.end, self.step, self.body]

    def to_json(self):
        return self._to_json("for", {
            "var": self.index_name,
            "first": self.start.to_json(),
            "last": self.end.to_json(),
            "step": self.step.to_json(),
            "body": self.body.to_json()
        })
