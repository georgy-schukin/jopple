from tnodes.stmt.statement import Statement


class DFStatement(Statement):
    def __init__(self, dfs):
        """dfs - list of df names (strings)"""
        super(DFStatement, self).__init__()
        self.dfs = dfs

    def to_json(self):
        return self._to_json("df", {
            "dfs": self.dfs
        })
