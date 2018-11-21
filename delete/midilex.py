# ------------------------------------------------------------
# midilex.py
#
# tokenizer for a simple midi shorthand
# e.g. '3 2 1 2 3 3 3' -> E D C D E E E
# ------------------------------------------------------------
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NOTE',         # Numbers 1 thru 7
    'REST',         # Number 0
    'SHARP',        # # before a note e.g. 1 3 #4 5
    'FLAT',         # b before a note e.g. 1 b7v b6v 5v
    'OCTAVE_DOWN',  # ^ after a note e.g. 1 3^ 5
    'OCTAVE_UP',    # v after a note e.g. 1 7v 6v
    'LBRACKET',     # [ - opening of a chord
    'RBRACKET',     # ] - closing of a chord
    'LPAREN',       # ( - opening of a group
    'RPAREN',       # ) - closing of a group
#    'CHORD',        # notes inside brackets e.g. [1 3 5]
    'NOTE_LENGTHEN',# - after a note; multiple for longer note; 1--- is whole note; 1- is half note
    'NOTE_SHORTEN', # / after a note; multiple for shorter note; 1/ is eigth note, 1// is sixteenth note
    'ARPEGGIO',     # ~ inside chord bracket e.g. [~1 3 5] 
    'DOT',          # . after a note; one dot increases note by half, two dots increases by quarter 
    'MEASURE_SEP'   # |
)

# Regular expression rules for simple tokens
t_SHARP         = r'[#]'
t_FLAT          = r'b'
t_OCTAVE_DOWN   = r'\^'
t_OCTAVE_UP     = r'v'
t_LBRACKET      = r'\['
t_RBRACKET      = r'\]'
t_LPAREN        = r'\('
t_RPAREN        = r'\)'   
# t_CHORD         = r'\[(.*?)\]'
t_NOTE_LENGTHEN = r'-'
t_NOTE_SHORTEN  = r'/'
t_ARPEGGIO      = r'~'
t_DOT           = r'.'
t_MEASURE_SEP   = r'\|'


# A regular expression rule with some action code
def t_NOTE(t):
    r'[1-7]'
    t.value = int(t.value)    
    return t

def t_REST(t):
    r'0'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


if __name__ == '__main__':
    # Test it out
    data = '''
    3 2 1 2 | 3 3 3 - | 2 2 2 - | 3 5 5 - | 
    3 2 1 2 | 3 3 3 3 | 2 2 3 2 | 1 - - - |
    1. 3 #4 6/ | 5. 3 1 b7v |
    #4v/ #4v/ #4v/ 5v/ 0 0 | 0/ #4v/ #4v/ #4v/ 5v/ b7v. | 
    1/ 1/ 1/ 1/
    '''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
        # print(tok.type, tok.value, tok.lineno, tok.lexpos)