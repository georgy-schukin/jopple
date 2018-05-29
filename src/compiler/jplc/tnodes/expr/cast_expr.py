from tnodes.expr.expr import Expr


class CastExpr(Expr):
    class CastType:
        ToBool = "bcast"
        ToInt = "icast"
        ToReal = "rcast"
        ToString = "scast"
        ToUnknown = "unknown"

        @classmethod
        def get_cast_type(cls, type_str):
            return {
                "bool": cls.ToBool,
                "int": cls.ToInt,
                "real": cls.ToReal,
                "string": cls.ToString
            }.get(type_str, cls.ToUnknown)

    def __init__(self, type_str, inner_expr):
        super(CastExpr, self).__init__(CastExpr.CastType.get_cast_type(type_str))
        self.expr = inner_expr

    def get_children(self):
        return [self.expr]

    def to_json(self):
        return self._to_json({
            "expr": self.expr.to_json()
        })
