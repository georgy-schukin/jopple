import ply.lex as lex
import re

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'df': 'DF',
    'cf': 'CF',
    'sub': 'SUB',
    'out': 'OUT',
    'let': 'LET',
    'as': 'AS',
    'import': 'IMPORT',
    'int': 'KW_INT',
    'real': 'KW_REAL',
    'string': 'KW_STRING',
    'bool': 'KW_BOOL',
    'value': 'KW_VALUE',
    'name': 'KW_NAME'
}

tokens = (
    'REAL',
    'INT',
    'STRING',
    'BOOL',
    'ID',
    'LT',
    'GT',
    'LE',
    'GE',
    'EQ',
    'NEQ',
    'DOT',
    'DBL_DOT',
    'AND',
    'OR',
    'NOT',
    'COMMENT'
) + tuple(reserved.values())

literals = ".,+-*/%<>(){}[]!?:&="

t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NEQ = r'!='
t_DOT = r'\.'
t_DBL_DOT = r'\.\.'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'\!'


def t_COMMENT(t):
    r'(/\*(.|\n)*?\*/)|(//.*)'
    pass


def t_BOOL(t):
    r'true|false'
    t.value = True if t.value == "true" else False
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


def t_STRING(t):
    r'\"(.|\n)*?\"'
    t.value = str(t.value[1:-1])  # strip quotes
    t.value = re.sub(r'\n\s*', "", t.value)  # remove newlines and indent spaces for multiline string
    return t


def t_REAL(t):
    r'(\d+(\.\d*)?[Ee][+-]?\d+)|(\d+\.\d+)'
    t.value = float(t.value)
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


t_ignore = ' \t\r;'


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def test():
    lexer = lex.lex()
    while True:
        try:
            data = input("Input:")
        except EOFError:
            break
        if not data:
            continue
        lexer.input(data)
        for token in lexer:
            print(token)


def create_lexer():
    return lex.lex()


if __name__ == "__main__":
    test()
