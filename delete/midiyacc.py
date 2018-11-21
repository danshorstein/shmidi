
# note_xwalk_dict = {
#     1: 60,
#     2: 62,
#     3: 64,
#     4: 65,
#     5: 67,
#     6: 69,
#     7: 70
# }

# def note_xwalk(note):
#     return note_xwalk_dict[note]


# Yacc example
""" DELETE*****   
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

EXAMPLE:
    3 2 1 2 | 3 3 3 - | 2 2 2 - | 3 5 5 - | 
    3 2 1 2 | 3 3 3 3 | 2 2 3 2 | 1 - - - |
    1. 3 #4 6/ | 5. 3 1 b7v |
    #4v/ #4v/ #4v/ 5v/ 0 0 | 0/ #4v/ #4v/ #4v/ 5v/ b7v. | 
    1/ 1/ 1/ 1/

Each Note has various properties standard with MIDI notes
note.val = the value of the note in MIDI number, in key of middle C (C4) unless otherwise set (e.g. key='D')
note.octave = 0 - middle octave. +1 is up one octave, +2 is up two octaves
note.length = '1/4'

Grammar                             Action
--------------------------------    -------------------------------------------- 
expression0 : expression1 #         expression0.val = expression1.val + 1
            | expression1 b         expression0.val = expression1.val - term.val
            | term                  expression0.val = term.val

term0       : term1 * factor        term0.val = term1.val * factor.val
            | term1 / factor        term0.val = term1.val / factor.val
            | factor                term0.val = factor.val

factor      : NOTE                  factor.val = note_xwalk(NOTE.lexval)
            | ( expression )        factor.val = expression.val
"""

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from midilex import tokens


def p_expression_sharp(p):
    'expression : expression SHARP expression'

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
   try:
       s = input('calc > ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)