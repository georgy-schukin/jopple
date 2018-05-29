from tnodes.sub.sub import Sub


class StructSub(Sub):
    def __init__(self, name, params, body):
        """
        :param name (string): name of the sub
        :param params (Param list): parameters of the sub
        :param body (Statement): body of the sub
        """
        super(StructSub, self).__init__("struct", name, params)
        self.body = body

    def get_children(self):
        return self.params + [self.body]

    def to_json(self):
        return self._to_json({
            "body": self.body.to_json()
        })
