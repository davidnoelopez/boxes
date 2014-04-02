import sys
import boxesLex
import ply.yacc as yacc
import cubetest
cubetest.cube

# Get the token map
tokens = boxesLex.tokens
tmpMethod = ""
tmpIdMethod = ""
tmptypeVar = ""
tmpDirMethod = 0 #variable para la direccion del metodo
VarDic = dict()	#diccionario de variables (tabla de variables)
MetDic = dict()	#diccionario de metodos (directorio de procedimientos)
tmpList = list() #fila temporal donde guarda los elementos parseados de la lista
listStack = list() #stack para guardar las listas generadas
POper = list()	#stack para guardar operadores
PilaO = list()	#stack para guardar operandos
PSaltos = list() #stack para guardar saltos
listQuadruple = list() #lista de cuadruplos
tCounter = 0 #contador para temporales
queue = [1, "[", 3, "[", 4, "[", 5, 6, "]", "]", "]"]


def addVarDictionary( idVar, valueVar, typeVar, p ):
	if idVar in VarDic:
		print "BoxesSemanticError: Duplicate variable: '", idVar, "' In line: ", str(p.lineno(1))
		exit(1)
	else:
		VarDic[idVar] = [valueVar, typeVar]
		#print "Found var: ", idVar, " - ", VarDic[idVar]

def addMetDictionary( idMet, typeMet, p ):
	if idMet in MetDic:
		print "BoxesSemanticError: Duplicate method: '", idMet, "' In line: ", str(p.lineno(1))
		exit(1)
	else:
		localDic = VarDic.copy()
		MetDic[idMet] = [typeMet, localDic, tmpDirMethod]
		print "Found method: ", idMet, " - ", MetDic[idMet]
		VarDic.clear()

def queueToList():
	if len(tmpList) is 0:
		return []
	else:
		element = tmpList[0]
		tmpList.pop(0)
		if element is "[":
			return [queueToList()] + queueToList()
		elif element is "]":
			return []
		else:
			return [element] + queueToList()

def createArithmeticQuadruple(oper, op1, op2, result, p):
	if oper is 12: #"=" ASSIGNATION
		#check cube
		resultCube = cubetest.cube[result[1],op1[1],oper]
		if resultCube is -1:
			print [oper, op1[1], None, result[1]]
			print("BoxesSemanticError: Arithmetic error. In line: " + str(p.lineno(1)))
			exit(1)
		else:
			listQuadruple.append([oper, op1[0], None, result[0]])
			#PilaO.append([result[0], resultCube])
			#print [result[0], resultCube]	
	else:
		#check cube
		resultCube = cubetest.cube[op1[1],op2[1],oper]
		if resultCube is -1:
			print("BoxesSemanticError: Arithmetic error. In line: " + str(p.lineno(1)))
			exit(1)
		else:
			listQuadruple.append([oper, op1[0], op2[0], result])
			PilaO.append([result, resultCube])

def createGoToQuadruple(oper, op1, op2, result):
	listQuadruple.append([oper, op1, op2, result])

def p_BOXES(p):
	"""
	BOXES : BOX OC VARS seen_globalvars METHODS seen_methods MAINBOX OP CP BLOCKS CC
	| BOX OC VARS seen_globalvars seen_methods MAINBOX OP CP BLOCKS CC
	"""

def p_seen_globalvars(p):
	"""
	seen_globalvars :
	"""
	#agrega el metodo global a diccionario
	global tmpMethod, tmpIdMethod, tmpDirMethod
	tmpMethod = "global"
	tmpIdMethod = "global"
	tmpDirMethod = 0
	addMetDictionary( tmpMethod, tmpMethod, p )

def p_seen_methods(p):
	"""
	seen_methods :
	"""

	global tmpMethod, tmpIdMethod, tmpDirMethod
	tmpMethod = "main"
	tmpIdMethod = "main"
	tmpDirMethod = len(listQuadruple)

def p_VARS(p):
	"""
	VARS : VARI VARS
		| VARF VARS
		| VARST VARS
		| VARL VARS
		|
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


	#varF is type var 1
	if len(p) >= 4:
		addVarDictionary( p[1], p[3], 1, p )
		#add assignation quadruple
		if p[2] is '=':
			valType = 1
			valID = p[1]
			createArithmeticQuadruple(12, [p[3], 1], None, [valID, valType], p)
	else:
		addVarDictionary( p[1], None, 1, p )

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
	#varI is type var 0
	if len(p) >= 4:
		addVarDictionary( p[1], p[3], 0, p )
		#add assignation quadruple
		if p[2] is '=':
			valType = 0
			valID = p[1]
			createArithmeticQuadruple(12, [p[3], 0], None, [valID, valType], p)
	else:
		addVarDictionary( p[1], None, 0, p )

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

	#varST is type var 2
	if len(p) >= 4:
		addVarDictionary( p[1], p[3], 2, p )
		#add assignation quadruple
		if p[2] is '=':
			valType = 2
			valID = p[1]
			createArithmeticQuadruple(12, [p[3], 2], None, [valID, valType], p)
	else:
		addVarDictionary( p[1], None, 2, p )

def p_VARL(p):
	"""
	VARL : VARLSMALL VARL3 PC 
	"""

def p_VARL3(p):
	"""
	VARL3 : IDV EQUALS OB VARL4 CB
		| IDV EQUALS OB VARL4 CB COMMA VARL3
		| IDV COMMA VARL3
		| IDV
	"""

	#Si la lista es vacia agrega una lista vacia al diccionario
	if len(p) is 4:
		addVarDictionary( p[1], [], "L", p )
	#si la lista no es vacia y hay listas en el stack, saca un elemento del stack y lo agrega al diccionario, si el ultimo elemento es 0 saca el siguiente elemento del stack y lo agrega.
	elif len(listStack) > 0:
		newList = listStack.pop()
		if newList is 0:
			addVarDictionary( p[1], listStack.pop(), "L", p )
		else:
			addVarDictionary( p[1], newList, "L", p )
	tmpList[:]

def p_VARL4(p):
	"""
	VARL4 : CTEL
		| CTEL COMMA VARL4
		| 
	"""

	#Saca la lista generada con los elementos de tmpList
	actualList = queueToList()
	tmpList[:]
	if len(listStack) > 0:
		#obtiene los saltos que debe dar
		jumps = listStack.pop()
		if jumps > 0:
			listStack.append(jumps-1)
		else:
			#agrega la lista generada en actual-List y el tamanio de la lista menos 1 para saber cuantos elementos debe saltarse.
			listStack.append(actualList)
			if (len(actualList)-1) > 0:
				listStack.append(len(actualList)-1)
	else:
		#agrega la lista generada en actualList y el tamanio de la lista menos 1 para saber cuantos elementos debe saltarse.
		listStack.append(actualList)
		if len(actualList)-1 > 0:
			listStack.append(len(actualList)-1)

def p_BLOCKS(p):
	"""
	BLOCKS : OC VARS BLOCKS2 CC
		| OC VARS CC
		| OC BLOCKS2 CC
		| OC CC
	"""
	global tmpIdMethod, tmpMethod
	addMetDictionary( tmpIdMethod, tmpMethod, p )

def p_BLOCKS2(p):
	"""
	BLOCKS2 : CODE
		| CODE BLOCKS2
	"""

def p_CODE(p):
	"""
	CODE : RETURN
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
	CONDITION : IF OP STM CP OC seen_OC_IF BLOCKS2 CC CONDITION2 
		| IF OP STM CP OC seen_OC_IF CC CONDITION2 
		| IF OP STM CP OC seen_OC_IF BLOCKS2 CC seen_CC_IF
		| IF OP STM CP OC seen_OC_IF CC seen_CC_IF
	"""

def p_seen_OC_IF(p):
	"""
	seen_OC_IF :
	"""

	#type of top element
	aux = PilaO.pop()
	#if type of aux is int
	if aux[1] is 0:
		createGoToQuadruple(20, aux[0], None, None)
		PSaltos.append(len(listQuadruple)-1)

def p_seen_CC_IF(p):
	"""
	seen_CC_IF :
	"""

	end = PSaltos.pop()
	listQuadruple[end][3] = len(listQuadruple)

def p_CONDITION2(p):
	"""
	CONDITION2 : ELSE seen_ELSE OC CONDITION3
	"""

def p_CONDITION3(p):
	"""
	CONDITION3 : BLOCKS2 CC seen_CC_ELSE
		| CC seen_CC_ELSE
	"""

def p_seen_ELSE(p):
	"""
		seen_ELSE :
	"""

	createGoToQuadruple(22, None, None, None)
	end = PSaltos.pop()
	listQuadruple[end][3] = len(listQuadruple)
	PSaltos.append(len(listQuadruple)-1)

def p_seen_CC_ELSE(p):
	"""
	seen_CC_ELSE :
	"""

	end = PSaltos.pop()
	listQuadruple[end][3] = len(listQuadruple)

def p_STM(p):
	"""
	STM : EXPRESSION STM2 EXPRESSION seen_STM 
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

	switch = {
				'==': 4,
				'<': 5,
				'>': 6,
				'<=': 7,
				'>=': 8,
				'<>': 9 }

	POper.append(switch[p[1]])

def p_seen_STM(p):
	"""
	seen_STM :
	"""

	global tCounter
	if len(POper) > 0:
		top = POper.pop()
		if top in range(4, 10):
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(top, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		else:
			POper.append(top)

def p_PARAM(p):
	"""
	PARAM : PARAM2 IDV
	"""
	#dependiendo del tipo de variable se guarda en el diccionario
	global tmptypeVar
	if tmptypeVar == 'vari':	
		addVarDictionary( p[2], None, 0, p )
	if tmptypeVar == 'varf':	
		addVarDictionary( p[2], None, 1, p )
	if tmptypeVar == 'vars':	
		addVarDictionary( p[2], None, 2, p )
	if tmptypeVar == 'varl':	
		addVarDictionary( p[2], None, "L", p )

def p_PARAM2(p):
	"""
	PARAM2 : VARISMALL
   		| VARSTSMALL
   		| VARFSMALL
   		| VARLSMALL
	"""
	global tmptypeVar	
	tmptypeVar = p[1]
	

def p_METHODS(p):
	"""
	METHODS : METHODS2 seen_IDM OP METHODS3 CP BLOCKS
		| METHODS2 seen_IDM OP METHODS3 CP BLOCKS METHODS
	"""

def p_seen_IDM(p):
	"""
	seen_IDM : IDM
	"""
	#agrega el metodo al diccionario de metodos si es que no ha sido previamente declarado y borra variables en diccionario temporal para almacenar las que se declaren en el nuevo metodo
	global tmpIdMethod, tmpDirMethod
	tmpIdMethod = p[1]
	tmpDirMethod = len(listQuadruple)
	#VarDic.clear()
	

def p_METHODS2(p):
	"""
	METHODS2 : RECURSIVEBOX
   		| VOIDBOX
   		| VARIBOX
   		| VARFBOX
   		| VARSBOX
   		| VARLBOX
	"""
	#asigna a tmpMethod el nombre del metodo actual
	global tmpMethod
	tmpMethod = p[1]

def p_METHODS3(p):
	"""
	METHODS3 : PARAM COMMA METHODS3
		| PARAM
		| 
	"""

def p_RETURN(p):
	"""
	RETURN : RETURNW EQUALS PC
	"""

def p_ASSIGNATION(p):
	"""
	ASSIGNATION : IDV EQUALS EXPRESSION PC
	"""

	
	op1 = PilaO.pop()
	valID = p[1]
	if valID in VarDic:
		valType = VarDic[valID][1]
		createArithmeticQuadruple(12, op1, None, [valID, valType], p)
	elif valID in MetDic['global'][1]:
		valType = MetDic['global'][1][valID][1]
		createArithmeticQuadruple(12, op1, None, [valID, valType], p)
	else:
		print("BoxesSemanticError: Non declared variable: " +  valID)
		exit(1)

def p_EXPRESSION(p):
	"""
	EXPRESSION : OPER seen_EXPF
		| OPER seen_EXPF seen_OPER EXPRESSION
	"""

def p_seen_EXPF(p):
	"""
	seen_EXPF :

	"""
	global tCounter
	if len(POper) > 0:
		top = POper.pop()
		if top is '+':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(0, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		elif top is '-':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(1, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		elif top == """or""":
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(11, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		else:
			#print top
			POper.append(top)

def p_seen_OPER(p):
	"""
	seen_OPER : PLUS
		| MINUS
		| OR
	"""

	POper.append(p[1])

def p_OPER(p):
	"""
	OPER : TERM seen_TERMF
	| TERM seen_TERMF seen_TERM OPER
	"""

def p_seen_TERMF(p):
	"""seen_TERMF :	
	"""
	global tCounter
	if len(POper) > 0:
		top = POper.pop()
		if top is '*':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(2, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		elif top is '/':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(3, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		elif top == """and""":
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(10, op1, op2, "t"+str(tCounter), p)
			tCounter = tCounter + 1
		else:
			#print top
			POper.append(top)


def p_seen_TERM(p):
	"""seen_TERM : MULTIPLY
		| DIVISION
		| AND
	"""
	POper.append(p[1])

def p_TERM(p):
	"""
	TERM : OP seen_OP_TERM STM CP
	| TERM2
	"""

	if len(p) is 5:
		POper.pop()

def p_seen_OP_TERM(p):
	"""
	seen_OP_TERM :
	"""

	POper.append('(')

def p_TERM2(p):
	"""
	TERM2 : CTE 
	| PLUS CTE
	| MINUS CTE
	"""

def p_CTE(p):
	"""
	CTE : INT seen_INT
	| FLOAT seen_FLOAT
	| STRING seen_STRING
	| seen_ID
	"""
	global valType, valID
	if valID is None:
		PilaO.append([p[1], valType])
	else:
		PilaO.append([valID, valType])
		valID = None

def p_seen_INT(p):
	"""
	seen_INT : 
	"""
	global valType

	valType = 0

def p_seen_FLOAT(p):
	"""
	seen_FLOAT : 
	"""
	global valType

	valType = 1

def p_seen_STRING(p):
	"""
	seen_STRING : 
	"""
	global valType

	valType = 2

def p_seen_ID(p):
	"""
	seen_ID : IDV
	| IDV OB INT CB
	"""
	global valType, valID
	if len(p) is 2:
		if p[1] in VarDic:
			valType = VarDic[p[1]][1]
			valID = p[1]
		elif p[1] in MetDic['global'][1]:
			valType = MetDic['global'][1][p[1]][1]
			valID = p[1]
		else:
			print("BoxesSemanticError: Non declared variable: " + p[1] + "\nlineno: " + p.lineno(1))
			exit(1)
	else:
		#valType = MetDic[tmpIdMethod][1][p[1]][p[3]]
		#ignore - agregar tipos de datos a listas
		print("lista")


def p_CTEL(p):
	"""
	CTEL : INT 
	| FLOAT
	| STRING
	| IDV
	| IDV OB INT CB
	"""
	#| OB seen_OB CTEL2


	#agrega a tmpList elementos atomicos
	if len(p) is 2:
		tmpList.append(p[1])
	elif len(p) is 5:
		tmpList.append(p[1]+p[2]+p[3]+p[4])


def p_CTEL2(p):
	"""
	CTEL2 : CTEL CB seen_CB
	| CTEL COMMA CTEL2
	| CB seen_CB
	"""

def p_seen_OB(p):
	"seen_OB :"
	#agrega a la lista temporal el "["
	tmpList.append('[')

def p_seen_CB(p):
	"seen_CB :"
    #agrega a la lista temporal el "]"
	tmpList.append(']')
	
def p_SAY(p):
	"""
	SAY : SAYW OP CONCAT CP PC
	"""

def p_CONCAT(p):
	"""
	CONCAT : EXPRESSION seen_EXP_SAY DOT CONCAT  
	| EXPRESSION seen_EXP_SAY
	"""

def p_seen_EXP_SAY(p):
	"""
	seen_EXP_SAY :
	"""

	out = PilaO.pop()
	listQuadruple.append([23, None, None, out[0]])

def p_ASK(p):
	"""
	ASK : ASKUSER OP STRING COMMA IDV CP PC
	"""

	valID = p[5]
	if valID in VarDic:
		valType = VarDic[p[5]][1]
	elif valID in MetDic['global'][1]:
		valType = MetDic['global'][1][p[5]][1]
	else:
		print("BoxesSemanticError: Non declared variable: " + p[5], "\nlineno: " + str(p.lineno(1)))
		exit(1)

	if valType is 2:
		write = p[3]
		listQuadruple.append([24, write, None, valID])
	else:
		print("BoxesSemanticError: askuser() return value must be 'vars'. In line: " + str(p.lineno(1)))
		exit(1)

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
	LOOP : LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 BY LOOP3 LOOP2 CP seen_CP_LOOP1 OC BLOCKS2 CC
	| LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 CP seen_CP_LOOP2 OC BLOCKS2 CC
	| LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 BY LOOP3 LOOP2 CP seen_CP_LOOP1 OC CC
	| LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 CP seen_CP_LOOP2 OC CC
	"""

	global tCounter
	#saca la variable a aumentar de la pila de operandos
	start = PilaO.pop()
	#crea cuadruplo de aumento
	createArithmeticQuadruple(0, start, aumento, "t"+str(tCounter), p)
	tCounter = tCounter + 1

	#saca el temporal del aumento y lo asigna a la variable a aumentar
	aux = PilaO.pop()
	createArithmeticQuadruple(12, aux, None, start, p)

	false = PSaltos.pop()
	jump = PSaltos.pop()

	createGoToQuadruple(22, None, None, jump)
	listQuadruple[false][3] = len(listQuadruple)


def p_seen_CP_LOOP1(p):
	"""
	seen_CP_LOOP1 :
	"""
	global aumento, tCounter, simbol
	aumento = PilaO.pop()
	aumento[0] = str(int(aumento[0]) * simbol)
	print aumento
	end = PilaO.pop()
	start = PilaO.pop()

	global valID, valType
	createArithmeticQuadruple(12, start, None, [valID, valType], p)

	start = [valID, valType]
	PilaO.append(start)
	if simbol is -1:
		createArithmeticQuadruple(6, start, end, "t"+str(tCounter), p)
	else:
		createArithmeticQuadruple(5, start, end, "t"+str(tCounter), p)
	tCounter = tCounter + 1

	aux = PilaO.pop()
	createGoToQuadruple(20, aux[0], None, None)
	PSaltos.append(len(listQuadruple)-1)

def p_seen_CP_LOOP2(p):
	"""
	seen_CP_LOOP2 :
	"""

	global aumento, tCounter
	aumento = [1, 0]
	end = PilaO.pop()
	start = PilaO.pop()

	global valID, valType
	createArithmeticQuadruple(12, start, None, [valID, valType], p)

	start = [valID, valType]
	PilaO.append(start)
	createArithmeticQuadruple(5, start, end, "t"+str(tCounter), p)
	tCounter = tCounter + 1

	aux = PilaO.pop()
	createGoToQuadruple(20, aux[0], None, None)
	PSaltos.append(len(listQuadruple)-1)

def p_seen_VAR_LOOP(p):
	"""
	seen_VAR_LOOP : IDV
	"""

	global valID, valType
	valID = p[1]

	if valID in VarDic:
		valType = VarDic[p[1]][1]
	elif valID in MetDic['global'][1]:
		valType = MetDic['global'][1][valID][1]
	else:
		print("BoxesSemanticError: Non declared variable: " + valID + "\nlineno: " + p.lineno(1))
		exit(1)

def p_LOOP2(p):
	"""
	LOOP2 : seen_INT_LOOP
	| seen_FLOAT_LOOP
	"""

def p_seen_INT_LOOP(p):
	"""
	seen_INT_LOOP : INT
	"""

	#se agrega int a la pila de operandos
	PilaO.append([p[1], 0])

def p_seen_FLOAT_LOOP(p):
	"""
	seen_FLOAT_LOOP : FLOAT
	"""

	#se agrega int a la pila de operandos
	PilaO.append([p[1], 1])

def p_LOOP3(p):
	"""
	LOOP3 : PLUS 
	| MINUS
	|
	"""

	global simbol
	simbol = 1
	if len(p) > 1:
		if p[1] is '-':
			simbol = -1

def p_seen_LOOP(p):
	"""
	seen_LOOP :
	"""

	PSaltos.append(len(listQuadruple)+1)

def p_LOOPIF(p):
	"""
	LOOPIF : LOOPIFW seen_LOOPIF OP STM CP seen_CP_LOOPIF OC BLOCKS2 CC
	| LOOPIFW seen_LOOPIF OP STM CP seen_CP_LOOPIF OC CC
	"""

	false = PSaltos.pop()
	end = PSaltos.pop()
	createGoToQuadruple(22, None, None, end)
	listQuadruple[false][3] = len(listQuadruple)

def p_seen_LOOPIF(p):
	"""
	seen_LOOPIF :
	"""

	PSaltos.append(len(listQuadruple))

def p_seen_CP_LOOPIF(p):
	"""
	seen_CP_LOOPIF :
	"""

	aux = PilaO.pop()
	if aux[1] is 0:
		createGoToQuadruple(20, aux[0], None, None)
		PSaltos.append(len(listQuadruple)-1)
	else:
		print ("BoxesSemanticError: Error in LOOPIF statement. In line: " + str(p.lineno(1)))

def p_error(t):
    print "BoxesParserError: Error, lineno: ", t.lineno
    exit(1)

import profile
# Build the grammar

yacc.yacc(method='LALR')
with open(sys.argv[1],'r') as content_file:
	content = content_file.read()
yacc.parse(content)

print "Procedimientos:"
print(MetDic)
print "caudruplos:"
print(listQuadruple)
print("<<SUCCESS>>")
#profile.run("yacc.yacc(method='LALR')")




