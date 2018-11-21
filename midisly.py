# -----------------------------------------------------------------------------
# calc.py
# -----------------------------------------------------------------------------

import sys
sys.path.insert(0, "../..")

from sly import Lexer, Parser

import shmidi

QUARTER = 960

class ShmidiLexer(Lexer):
    tokens = { NOTE, REST }  # add NAME later? Need to deconflict with 'b' and 'v'
    ignore = ' \t\|'
    literals = { '#', 'b', '^', 'v', '.', '-', '/' } # ADD ~ for arpeggio; ADD [EXPR] FOR CHORDS; do some analysis of | for correct timing?

    # Tokens
    NOTE = r'[1-7]'

    REST = r'0'

    # NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class ShmidiParser(Parser):
    tokens = ShmidiLexer.tokens

    precedence = (
        ('left', '-'),
        ('left', '^', 'v', '.', '/'), 
        ('right', SHARP_FLAT),
        ('left', EXPR)
        )

    def __init__(self):
        self.names = { }
        self.line = []
        self.melody = []
        self.note = None

    # @_('NAME "=" expr')
    # def statement(self, p):
    #     self.names[p.NAME] = p.expr

    @_('expr')
    def statement(self, p):
        self.melody.append(p.expr.return_msg())
        print(p.expr.return_msg())

    @_('expr expr %prec EXPR')
    def expr(self, p):
        self.melody.append(p.expr0.return_msg())
        print(p.expr0.return_msg())
        return p.expr1

    @_('expr "#" expr')
    def expr(self, p):
        self.melody.append(p.expr0.return_msg())
        print(p.expr0.return_msg())
        p.expr1.note += 1
        return p.expr1

    @_('expr "b" expr')
    def expr(self, p):
        self.melody.append(p.expr0.return_msg())
        print(p.expr0.return_msg())        
        p.expr1.note -= 1
        return p.expr1

    @_('expr "^"')
    def expr(self, p):
        p.expr.note += 12
        return p.expr

    @_('expr "v"')
    def expr(self, p):
        p.expr.note -= 12
        return p.expr

    @_('expr "."')
    def expr(self, p):
        p.expr.length *= 1.5
        return p.expr

    @_('expr "-"')
    def expr(self, p):
        p.expr.length += QUARTER
        return p.expr

    @_('expr "/"')
    def expr(self, p):
        p.expr.length *= 0.5
        return p.expr

    @_('"#" expr %prec SHARP_FLAT')
    def expr(self, p):
        # self.note.note += 1
        p.expr.note += 1
        return p.expr1

    @_('"b" expr %prec SHARP_FLAT')
    def expr(self, p):
        # self.note.note -= 1
        p.expr.note -= 1
        return p.expr

    # @_('"(" expr ")"')
    # def expr(self, p):
    #     return p.expr

    @_('REST')
    def expr(self, p):
        # self.note = Note(1, velocity=0)    
        return shmidi.Note(1, velocity=0)

    @_('NOTE')
    def expr(self, p):
        # self.note = Note(p.NOTE)
        return shmidi.Note(p.NOTE)

    # @_('NAME')
    # def expr(self, p):
    #     try:
    #         return self.names[p.NAME]
    #     except LookupError:
    #         print("Undefined name '%s'" % p.NAME)
    #         return 0

if __name__ == '__main__':
    lexer = ShmidiLexer()
    parser = ShmidiParser()
    # while True:
    #     try:
    #         text = input('|𝄞: ')
    #     except EOFError:
    #         break
    #     if text:
    #         parser.parse(lexer.tokenize(text))
    
    melody = '''
            6v. 6v/ 6v 3 | 3 2 1 - | 7v. 7v/ 7v 1/ 7v/ | 6v - - - |
            6v/ 6v 6v/ 6 6/ 5/ | 6 5 3 - | 2/ 2 1/ 2 5 | 3 - - - |
            4/ 4 3/ 4/ 4 3/ | 4 3/ 2/ 1 - | '''
    
    parser.parse(lexer.tokenize(melody))