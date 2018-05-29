import json

import ply.yacc as yacc

import lexer as lx
from lexer import tokens
from tnodes import Program, Param, Arg
from tnodes.expr import BinaryExpr, ConstExpr, CastExpr, UnaryExpr, IdExpr, TernaryExpr
from tnodes.stmt import BlockStatement, IfStatement, ForStatement, \
    WhileStatement, DFStatement, CFStatement, LetStatement
from tnodes.sub import StructSub, ExternSub


precedence = (
    ('nonassoc', 'TERNARY'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('nonassoc', 'EQ', 'NEQ'),
    ('nonassoc', 'LT', 'GT', 'LE', 'GE'),
    ('left', '+', '-'),
    ('left', '*', '/', '%'),
    ('right', 'UMINUS', 'NOT'),
    ('left', 'DOT'),
    ('left', 'DBL_DOT'),
    ('nonassoc', 'IFX'),
    ('nonassoc', 'ELSE'),
)


# Program
def p_program(p):
    """program : sub_list"""
    p[0] = Program(p[1])


def p_sub_list(p):
    """sub_list : sub
    | sub_list sub"""
    p[0] = make_no_separator_list(p)


def p_sub(p):
    """sub : struct_sub
     | extern_sub"""
    p[0] = p[1]


def p_struct_sub(p):
    """struct_sub : SUB ID '(' param_list ')' statement"""
    p[0] = StructSub(p[2], p[4], p[6])


def p_extern_sub(p):
    """extern_sub : extern_sub_with_alias
    | extern_sub_without_alias"""
    p[0] = p[1]


def p_extern_sub_with_alias(p):
    """extern_sub_with_alias : IMPORT ID '(' param_list ')' AS ID"""
    p[0] = ExternSub(p[7], p[2], p[4])


def p_extern_sub_without_alias(p):
    """extern_sub_without_alias : IMPORT ID '(' param_list ')' """
    p[0] = ExternSub(p[2], p[2], p[4])


# Statements
def p_statement(p):
    """statement : block_statement
    | if_statement
    | for_statement
    | while_statement
    | cf_statement
    | let_statement"""
    p[0] = p[1]


def p_block_statement(p):
    """block_statement : '{' '}'
    | '{' statement_list '}' """
    if len(p) == 3:
        p[0] = BlockStatement([])
    else:
        p[0] = BlockStatement(p[2])


def p_statement_list(p):
    """statement_list : statement_ext
    | statement_list statement_ext"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement_ext(p):
    """statement_ext : statement
    | df_statement"""
    p[0] = p[1]


def p_if_statement(p):
    """if_statement : if_solo_statement
     | if_else_statement"""
    p[0] = p[1]


def p_if_solo_statement(p):
    """if_solo_statement : IF '(' expr ')' statement %prec IFX"""
    p[0] = IfStatement(p[3], p[5])


def p_if_else_statement(p):
    """if_else_statement : IF '(' expr ')' statement ELSE statement"""
    p[0] = IfStatement(p[3], p[5], p[7])


def p_for_statement(p):
    """for_statement : for_statement_with_step
    | for_statement_without_step"""
    p[0] = p[1]


def p_for_statement_with_step(p):
    """for_statement_with_step : FOR ID '=' expr DBL_DOT expr ':' expr statement"""
    p[0] = ForStatement(p[2], p[4], p[6], p[8], p[9])


def p_for_statement_without_step(p):
    """for_statement_without_step : FOR ID '=' expr DBL_DOT expr statement"""
    step = ConstExpr(1)  # default step
    p[0] = ForStatement(p[2], p[4], p[6], step, p[7])


def p_while_statement(p):
    """while_statement : while_statement_with_out
    | while_statement_without_out"""
    p[0] = p[1]


def p_while_statement_with_out(p):
    """while_statement_with_out : WHILE expr ',' ID '=' expr DBL_DOT OUT id_expr statement"""
    p[0] = WhileStatement(p[4], p[6], p[2], p[10], p[9])


def p_while_statement_without_out(p):
    """while_statement_without_out : WHILE expr ',' ID '=' expr statement"""
    p[0] = WhileStatement(p[4], p[6], p[2], p[7])


def p_cf_statement(p):
    """cf_statement : cf_statement_with_id
    | cf_statement_without_id"""
    p[0] = p[1]


def p_cf_statement_with_id(p):
    """cf_statement_with_id : CF id_expr ':' ID '(' arg_list ')' """
    p[0] = CFStatement(p[2], p[4], p[6])


def p_cf_statement_without_id(p):
    """cf_statement_without_id : ID '(' arg_list ')' """
    cf_id = AutoCFId.next_id()
    p[0] = CFStatement(cf_id, p[1], p[3])


def p_df_statement(p):
    """df_statement : DF df_name_list"""
    p[0] = DFStatement(p[2])


def p_df_name_list(p):
    """df_name_list : df_name
    | df_name_list ',' df_name"""
    p[0] = make_separator_list(p)


def p_df_name(p):
    """df_name : ID"""
    p[0] = p[1]


def p_let_statement(p):
    """let_statement : LET arg_assign_list statement"""
    p[0] = LetStatement(p[2], p[3])


# Args
def p_arg_list(p):
    """arg_list :
    | arg
    | arg_list ',' arg"""
    p[0] = make_separator_list(p)


def p_arg(p):
    """arg : expr"""
    p[0] = Arg("", p[1])


def p_arg_assign_list(p):
    """arg_assign_list : arg_assign
    | arg_assign_list ',' arg_assign"""
    p[0] = make_separator_list(p)


def p_arg_assign(p):
    """arg_assign : ID '=' expr"""
    p[0] = Arg(p[1], p[3])


# Params
def p_param_list(p):
    """param_list :
    | param
    | param_list ',' param"""
    p[0] = make_separator_list(p)


def p_param(p):
    """param : type ID
    | type"""
    if len(p) == 3:
        p[0] = Param(p[1], p[2])
    else:
        p[0] = Param(p[1], "")


def p_type(p):
    """type : KW_INT
    | KW_REAL
    | KW_STRING
    | KW_BOOL
    | KW_NAME
    | KW_VALUE"""
    p[0] = p[1]


# Expressions
def p_expr_binary_plus(p):
    """expr : expr '+' expr"""
    p[0] = BinaryExpr("+", p[1], p[3])


def p_expr_binary_minus(p):
    """expr : expr '-' expr"""
    p[0] = BinaryExpr("-", p[1], p[3])


def p_expr_binary_multiply(p):
    """expr : expr '*' expr"""
    p[0] = BinaryExpr("*", p[1], p[3])


def p_expr_binary_modulo(p):
    """expr : expr '%' expr"""
    p[0] = BinaryExpr("%", p[1], p[3])


def p_expr_binary_divide(p):
    """expr : expr '/' expr"""
    p[0] = BinaryExpr("/", p[1], p[3])


def p_expr_binary_lt(p):
    """expr : expr LT expr"""
    p[0] = BinaryExpr("<", p[1], p[3])


def p_expr_binary_gt(p):
    """expr : expr GT expr"""
    p[0] = BinaryExpr(">", p[1], p[3])


def p_expr_binary_le(p):
    """expr : expr LE expr"""
    p[0] = BinaryExpr("<=", p[1], p[3])


def p_expr_binary_ge(p):
    """expr : expr GE expr"""
    p[0] = BinaryExpr(">=", p[1], p[3])


def p_expr_binary_eq(p):
    """expr : expr EQ expr"""
    p[0] = BinaryExpr("==", p[1], p[3])


def p_expr_binary_and(p):
    """expr : expr AND expr"""
    p[0] = BinaryExpr("&&", p[1], p[3])


def p_expr_binary_or(p):
    """expr : expr OR expr"""
    p[0] = BinaryExpr("||", p[1], p[3])


def p_expr_binary_neq(p):
    """expr : expr NEQ expr"""
    p[0] = BinaryExpr("!=", p[1], p[3])


def p_expr_unary_minus(p):
    """expr : '-' expr %prec UMINUS"""
    p[0] = UnaryExpr("u-", p[2])


def p_expr_unary_not(p):
    """expr : NOT expr"""
    p[0] = UnaryExpr("!", p[2])


def p_expr_ternary(p):
    """expr : expr '?' expr ':' expr %prec TERNARY"""
    p[0] = TernaryExpr("?:", p[1], p[3], p[5])


def p_expr_id(p):
    """expr : id_expr"""
    p[0] = p[1]


def p_id_expr(p):
    """id_expr : ID
    | ID indices_list"""
    if len(p) == 2:
        p[0] = IdExpr(p[1])
    else:
        p[0] = IdExpr(p[1], p[2])


def p_indices_list(p):
    """indices_list : index
    | indices_list index"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_index(p):
    """index : '[' expr ']' """
    p[0] = p[2]


def p_expr_cast(p):
    """expr : KW_INT '(' expr ')'
    | KW_REAL '(' expr ')'
    | KW_STRING '(' expr ')'
    | KW_BOOL '(' expr ')' """
    p[0] = CastExpr(p[1], p[3])


def p_expr_paren(p):
    """expr : '(' expr ')' """
    p[0] = p[2]


def p_expr_const(p):
    """expr : INT
    | REAL
    | STRING
    | BOOL"""
    p[0] = ConstExpr(p[1])


# Error handling
def p_error(p):
    if p:
        print("Syntax error at token '{0}' (line {1}, pos {2})".
              format(p.value, p.lineno, p.lexpos))
    else:
        print("Syntax error at EOF")


# Utils
class AutoCFId(object):
    current_id = 0

    @classmethod
    def next_id(cls):
        next_id = cls.current_id
        cls.current_id += 1
        return IdExpr("_cf_{0}".format(next_id))


def make_separator_list(p):
    """For rules like 'empty | list_elem | list ',' list_elem' """
    if len(p) == 1:
        return []
    elif len(p) == 2:
        return [p[1]]
    else:
        return p[1] + [p[3]]


def make_no_separator_list(p):
    """For rules like 'list_elem | list list_elem' """
    if len(p) == 2:
        return [p[1]]
    else:
        return p[1] + [p[2]]


# Test
def input_code():
    lines = []
    while True:
        try:
            line = input(">>> ")
        except EOFError:
            return None
        if not line:
            break
        else:
            lines.append(line)
    return "\n".join(lines)


def test():
    parser = LunaParser()
    print("Input code line by line, empty line to complete, Ctrl+D to exit")
    while True:
        code = input_code()
        if not code:
            break
        tree = parser.parse(code)
        if tree:
            json_str = json.dumps(tree.to_json(), indent=4)
            print(json_str)


class LunaParser(object):
    def __init__(self):
        super(LunaParser, self).__init__()
        self.lexer = lx.create_lexer()
        self.parser = yacc.yacc()

    def parse(self, code):
        return self.parser.parse(code, lexer=self.lexer)


if __name__ == "__main__":
    test()




