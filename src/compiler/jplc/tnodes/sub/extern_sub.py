from tnodes.sub.sub import Sub


class ExternSub(Sub):
    def __init__(self, name, code_name, params):
        """
        :param name (string): name of the sub
        :param code_name (string): name of the external code
        :param params (Param list): parameters of the sub
        """
        super(ExternSub, self).__init__("extern", name, params)
        self.code_name = code_name

    def get_children(self):
        return self.params

    def to_json(self):
        return self._to_json({
            "code": self.code_name
        })
