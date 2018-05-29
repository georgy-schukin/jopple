from tnodes.expr.expr import Expr


class ConstExpr(Expr):
    class ConstType:
        Int = "iconst"
        Real = "rconst"
        String = "sconst"
        Bool = "bconst"
        Unknown = "unknown"

        @classmethod
        def get_const_type(cls, value):
            if isinstance(value, bool):
                return cls.Bool
            elif isinstance(value, int):
                return cls.Int
            elif isinstance(value, float):
                return cls.Real
            elif isinstance(value, str):
                return cls.String
            else:
                return cls.Unknown

    def __init__(self, value):
        """value - constant of supported scalar type"""
        super(ConstExpr, self).__init__(ConstExpr.ConstType.get_const_type(value))
        self.value = value

    def to_json(self):
        return self._to_json({
            "value": self.value
        })
