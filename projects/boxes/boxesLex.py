#!/usr/bin/python
# ------------------------------------------------------------
# boxesLex.py
#
# tokenizer for a simple expression evaluator for
# numbers and +,-,*,/
# ------------------------------------------------------------
import sys
sys.path.insert(0,"../..")

if sys.version_info[0] >= 3:
    raw_input = input

import ply.lex as lex

# List of token names.   This is always required

reserved = {
   'box' : 'BOX',
   'vari' : 'VARISMALL',
   'vars' : 'VARSTSMALL',
   'varf' : 'VARFSMALL',
   'if' : 'IF',
   'else' : 'ELSE',
   'recursivebox': 'RECURSIVEBOX',
   'mainbox': 'MAINBOX',
   'voidbox': 'VOIDBOX',
   'varibox': 'VARIBOX',
   'varfbox': 'VARFBOX',
   'varsbox': 'VARSBOX',
   'return': 'RETURNW',
   'say': 'SAYW',
   'askuser': 'ASKUSER',
   'callbox': 'CALLBOXW',
   'loop': 'LOOPW',
   'from': 'FROM',
   'to': 'TO',
   'by': 'BY',
   'loopif': 'LOOPIFW',
   'and': 'AND',
   'or': 'OR'
}

tokens = [
'PC',
'COMMA',
'OC',
'CC',
'OP',
'CP',
'OB',
'CB',
'LT',
'GT',
'LTE',
'GTE',
'LTGT',
'DOUBLEEQUALS',
'EQUALS',
'PLUS',
'MINUS',
'MULTIPLY',
'DIVISION',
'IDV',
'IDM',
'FLOAT',
'INT',
'STRING',
'DOT',
]+ list(reserved.values())

# Regular expression rules for simple tokens
t_PC = r'\;'
t_COMMA = r'\,'
t_OC = r'\{'
t_CC = r'\}'
t_OP = r'\('
t_CP = r'\)'
t_OB = r'\['
t_CB = r'\]'
t_LT = r'<'
t_GT = r'>'
t_LTE = r'<='
t_GTE = r'>='
t_LTGT = r'<>'
t_DOUBLEEQUALS = r'=='
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVISION = r'/'
t_DOT = r'\.'

# A regular expression rule with some action code
def t_IDV(t):
    r'\#[a-z](_?[a-z0-9]+)*'
    t.type = reserved.get(t.value,'IDV') 
    return t

def t_IDM(t):
    r'[a-z](_?[a-z0-9]+)*'
    t.type = reserved.get(t.value,'IDM') 
    return t


def t_FLOAT(t):
    r'[-+]?[0-9]+\.[0-9]+'
    t.type = reserved.get(t.value,'FLOAT') 
    return t


def t_INT(t):
    r'[-+]?[0-9]+'
    t.type = reserved.get(t.value,'INT') 
    return t

def t_STRING(t):
    #r'\"[a-zA-Z0-9]*\"'
    r'\"(?:\\?.)*?\"' 
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "BoxesLexerError: Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)
    exit(1)


lexer = lex.lex()
if __name__ == "__main__":
    lex.runmain(lexer)

#LEXER SOLO
# Build the lexer
#lexer = lex.lex()

# Test it out
#data = '''
#program hola_2;
#var hola_1,hola_2:float;
#hola_3,hola_4:int;
#{ 
#	prueba_prueba=10;
#	if(7>9){
#		prueba_prueba2=5;{{{{{{	
#	}else{
#		probando2=10.10;	
#	};
#	print("hola");
#}
#'''

# Give the lexer some input
#lexer.input(data)

# Tokenize
#while True:
#    tok = lexer.token()
#    if not tok: break      # No more input
#    print tok.type, tok.value
