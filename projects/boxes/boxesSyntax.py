import sys
import boxesLex
import ply.yacc as yacc

# Get the token map
tokens = boxesLex.tokens

def p_BOXES(p):
	"""
	BOXES : BOX OC VARS BLOCKS METHODS CC
	| BOX OC BLOCKS METHODS CC
	| BOX OC VARS BLOCKS CC
	| BOX OC BLOCKS CC
	"""
def p_VARS(p):
	"""
	VARS : VARI 
		| VARF 
		| VARST 
		| VARL
		
	"""

def p_VARF(p):
	"""
	VARF : VARFSMALL VARF3 PC 
	"""

def p_VARF3(p):
	"""
	VARF3 : IDV EQUALS FLOAT COMMA VARF3
		| IDV EQUALS FLOAT
		| IDV COMMA VARF3
		| IDV
	"""

def p_VARI(p):
	"""
	VARI : VARISMALL VARI3 PC 
	"""

def p_VARI3(p):
	"""
	VARI3 : IDV EQUALS INT COMMA VARI3
		| IDV EQUALS INT
		| IDV COMMA VARI3
		| IDV
	"""

def p_VARST(p):
	"""
	VARST : VARSTSMALL VARST3 PC 
	"""

def p_VARST3(p):
	"""
	VARST3 : IDV EQUALS STRING COMMA VARST3
		| IDV EQUALS STRING
		| IDV COMMA VARST3
		| IDV
	"""

def p_VARL(p):
	"""
	VARL : VARLSMALL VARL3 PC 
	"""

def p_VARL3(p):
	"""
	VARL3 : IDV EQUALS OB VARL4 CB
		| IDV EQUALS OB VARL4 CB VARL3
	"""

def p_VARL4(p):
	"""
	VARL4 : CTE
		| CTE COMMA VARL4
	"""

def p_BLOCKS(p):
	"""
	BLOCKS : MAINBOX OP CP OC BLOCKS2 CC
		| OC CC
	"""

def p_BLOCKS2(p):
	"""
	BLOCKS2 : CODE
		| CODE BLOCKS2
	"""

def p_CODE(p):
	"""
	CODE : RETURN
		| VARS
		| ASSIGNATION
		| LOOP
		| LOOPIF
		| CONDITION
		| ASK
		| SAY
		| CALLBOX
	"""

def p_CONDITION(p):
	"""
	CONDITION : IF OP STM CP OC BLOCKS2 CC CONDITION2
		| IF OP STM CP OC CC CONDITION2
		| IF OP STM CP OC BLOCKS2 CC
		| IF OP STM CP OC CC
	"""

def p_CONDITION2(p):
	"""
	CONDITION2 : ELSE OC BLOCKS2 CC
		| ELSE OC CC
	"""

def p_STM(p):
	"""
	STM : EXPRESSION STM2 EXPRESSION
		| EXPRESSION
	"""

def p_STM2(p):
	"""
	STM2 : GT
		| GTE
		| LT
		| LTE
		| DOUBLEEQUALS
		| LTGT
	"""

def p_PARAM(p):
	"""
	PARAM : PARAM2 IDV
	"""

def p_PARAM2(p):
	"""
	PARAM2 : VARISMALL
   		| VARSTSMALL
   		| VARFSMALL
   		| VARLSMALL
	"""

def p_METHODS(p):
	"""
	METHODS : METHODS2 IDM OP METHODS3 CP OC BLOCKS2 CC
		| METHODS2 IDM OP METHODS3 CP OC CC
	"""

def p_METHODS2(p):
	"""
	METHODS2 : RECURSIVEBOX
   		| VOIDBOX
   		| VARIBOX
   		| VARFBOX
   		| VARSBOX
   		| VARLBOX
	"""

def p_METHODS3(p):
	"""
	METHODS3 : PARAM COMMA METHODS3
		| PARAM
	"""

def p_RETURN(p):
	"""
	RETURN : RETURNW EQUALS PC
	"""

def p_ASSIGNATION(p):
	"""
	ASSIGNATION : IDV EQUALS EXPRESSION PC
	"""

def p_EXPRESSION(p):
	"""
	EXPRESSION : OPER 
		| OPER PLUS EXPRESSION
		| OPER MINUS EXPRESSION
	"""

def p_OPER(p):
	"""
	OPER : TERM 
	| TERM MULTIPLY OPER
	| TERM DIVISION OPER
	"""

def p_TERM(p):
	"""
	TERM : OP EXPRESSION CP
	| TERM2
	"""

def p_TERM2(p):
	"""
	TERM2 : CTE 
	| PLUS CTE
	| MINUS CTE
	"""

def p_CTE(p):
	"""
	CTE : INT 
	| FLOAT
	| STRING
	| IDV
	| IDV OB INT CB
	"""

def p_SAY(p):
	"""
	SAY : SAYW OP CONCAT CP PC
	"""

def p_CONCAT(p):
	"""
	CONCAT : EXPRESSION DOT CONCAT  
	| EXPRESSION
	"""

def p_ASK(p):
	"""
	ASK : ASKUSER OP STRING COMMA IDV CP PC  
	"""
	
def p_CALLBOX(p):
	"""
	CALLBOX : CALLBOXW OP IDM COMMA PARAMETERS CP PC  
	"""

def p_PARAMETERS(p):
	"""
	PARAMETERS : EXPRESSION COMMA PARAMETERS
			| EXPRESSION   
	"""

def p_LOOP(p):
	"""
	LOOP : LOOPW OP IDV FROM LOOP2 TO LOOP2 BY LOOP3 LOOP2 CP OC BLOCKS2 CC
	| LOOPW OP IDV FROM LOOP2 TO LOOP2 CP OC BLOCKS2 CC
	| LOOPW OP IDV FROM LOOP2 TO LOOP2 BY LOOP3 LOOP2 CP OC CC
	| LOOPW OP IDV FROM LOOP2 TO LOOP2 CP OC CC
	"""

def p_LOOP2(p):
	"""
	LOOP2 : INT
	| FLOAT  
	"""

def p_LOOP3(p):
	"""
	LOOP3 : PLUS 
	| MINUS 
	"""

def p_LOOPIF(p):
	"""
	LOOPIF : LOOPIFW OP EXPRESSION CP OC BLOCKS2 CC
	| LOOPIFW OP EXPRESSION CP OC CC 
	"""


def p_error(t):
    print "Error, lineno: ", t.lineno
    exit(1)

import profile
# Build the grammar

yacc.yacc(method='LALR')
with open(sys.argv[1],'r') as content_file:
	content = content_file.read()
yacc.parse(content); 

print("<<SUCCESS>>")
#profile.run("yacc.yacc(method='LALR')")




