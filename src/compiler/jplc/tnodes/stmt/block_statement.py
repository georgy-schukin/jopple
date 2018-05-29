from tnodes.stmt.statement import Statement


class BlockStatement(Statement):
    def __init__(self, items):
        """items - list of statements"""
        super(BlockStatement, self).__init__()
        self.items = items
        self.dfs = []

    def get_children(self):
        return self.items

    def to_json(self):
        return self._to_json("block", {
            "items": [it.to_json() for it in self.items],
            "dfs": self.dfs
        })
