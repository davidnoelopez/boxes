#!/usr/bin/python
import cgi
import json
import sys
import boxesLex
import ply.yacc as yacc
import cubetest
from memStruct import MemoryDir

# Get the token map
tokens = boxesLex.tokens
tmpMethod = ""
tmpIdMethod = ""
tmptypeVar = ""
tmpDirMethod = 0 #variable para la direccion del metodo
VarDic = dict()	#diccionario de variables (tabla de variables)
MetDic = dict()	#diccionario de metodos (directorio de procedimientos)
ConDic = dict() #diccionario de constantes
ParList = list()	#lista de parametros de cada metodo
TamList = [0,0,0]	#lista de tipos de variables locales de cada metodo
tmpList = list() #fila temporal donde guarda los elementos parseados de la lista
listStack = list() #stack para guardar las listas generadas
POper = list()	#stack para guardar operadores
PilaO = list()	#stack para guardar operandos
PSaltos = list() #stack para guardar saltos
listQuadruple = list() #lista de cuadruplos
tempArray = list() #lista de tamanios de matrices para tabla de variables
tempArrayStack = list() #pila para almacenar los tamanios de matrices
pilaDim = list() #pila para arreglos
tempArraySize = 1 #tamanio del arreglo temporal
valID = None
varID = None
queue = [1, "[", 3, "[", 4, "[", 5, 6, "]", "]", "]"]


#Direcciones de memoria
memGlobal = MemoryDir(0, 2000, 4000, 6000)
memLocal = MemoryDir(6000, 8000, 10000, 12000)
memTemp = MemoryDir(12000, 14000, 16000, 18000)
memConst = MemoryDir(18000, 20000, 22000, 24000)

def addVarDictionary( idVar, valueVar, typeVar, arrayList, p ):
	TamList[typeVar] = TamList[typeVar] + 1
	if idVar in VarDic:
		print "BoxesSemanticError: Duplicate variable: '", idVar, "' In line: ", str(p.lineno(1))
		print "</body></html>"
		exit(1)
	elif "global" in MetDic and idVar in MetDic["global"][1]:
		print "BoxesSemanticError: Duplicate variable in global context: '", idVar, "' In line: ", str(p.lineno(1))
		print "</body></html>"
		exit(1)
	else:
		if tmpMethod is "global":
			if typeVar is 0:
				memDir = memGlobal.addVari(arrayList[len(arrayList)-1])
			elif typeVar is 1:
				memDir = memGlobal.addVarf(arrayList[len(arrayList)-1])
			elif typeVar is 2:
				memDir = memGlobal.addVars(arrayList[len(arrayList)-1])
		else:
			if typeVar is 0:
				memDir = memLocal.addVari(arrayList[len(arrayList)-1])
			elif typeVar is 1:
				memDir = memLocal.addVarf(arrayList[len(arrayList)-1])
			elif typeVar is 2:
				memDir = memLocal.addVars(arrayList[len(arrayList)-1])
		VarDic[idVar] = [valueVar, typeVar, memDir, arrayList]

def addMetDictionary( idMet, typeMet, p ):
	global ParList
	if idMet in MetDic:
		print "BoxesSemanticError: Duplicate method: '", idMet, "' In line: ", str(p.lineno(1))
		print "</body></html>"
		exit(1)
	else:
		localParList = list(ParList)
		MetDic[idMet] = [typeMet, dict(), tmpDirMethod, localParList, list()]
		if idMet is "global":
			localDic = VarDic.copy()
			localTamList = list(TamList)
			MetDic[idMet][1] = localDic
			MetDic[idMet][4] = localTamList
			VarDic.clear()
			TamList[:] = [0,0,0]
		ParList[:] = []

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
			print("BoxesSemanticError: Arithmetic error. In line: " + str(p.lineno(1)))
			print "</body></html>"
			exit(1)
		else:
			listQuadruple.append([oper, op1[0], None, result[0]])
	else:
		#check cube
		resultCube = cubetest.cube[op1[1],op2[1],oper]
		if resultCube is -1:
			print("BoxesSemanticError: Arithmetic error. In line: " + str(p.lineno(1)))
			print "</body></html>"
			exit(1)

		else:
			#saca la direccion para las temporales.
			if result is "t":
				if resultCube is 0:
					result = memTemp.addVari()
				elif resultCube is 1:
					result = memTemp.addVarf()
				elif resultCube is 2:
					result = memTemp.addVars()
			listQuadruple.append([oper, op1[0], op2[0], result])
			PilaO.append([result, resultCube])
			TamList[resultCube] = TamList[resultCube] + 1

def createGoToQuadruple(oper, op1, op2, result):
	listQuadruple.append([oper, op1, op2, result])

def p_BOXES(p):
	"""
	BOXES : BOX OC before_vars VARS seen_globalvars METHODS seen_methods MAINBOX OP CP BLOCKS CC
	| BOX OC before_vars VARS seen_globalvars seen_methods MAINBOX OP CP BLOCKS CC
	"""

def p_before_vars(p):
	"""
	before_vars :
	"""
	#inicializa valores para metodo global.
	global tmpMethod, tmpIdMethod, tmpDirMethod
	tmpMethod = "global"
	tmpIdMethod = "global"
	tmpDirMethod = 0

def p_seen_globalvars(p):
	"""
	seen_globalvars :
	"""
	#agrega el metodo global a diccionario
	addMetDictionary( tmpMethod, tmpMethod, p )
	createGoToQuadruple(22, None, None, None)
	PSaltos.append(len(listQuadruple)-1)

def p_seen_methods(p):
	"""
	seen_methods :
	"""

	global tmpMethod, tmpIdMethod, tmpDirMethod
	tmpMethod = "main"
	tmpIdMethod = "main"
	tmpDirMethod = len(listQuadruple)
	jump = PSaltos.pop()
	listQuadruple[jump][3] = len(listQuadruple)

def p_VARS(p):
	"""
	VARS : VARI VARS
		| VARF VARS
		| VARST VARS
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
		| IDV VAR_ARRAY COMMA VARF3
		| IDV VAR_ARRAY
	"""


	#varF is type var 1
	if p[2] is '=':
		addVarDictionary( p[1], p[3], 1, [1], p )
		#add assignation quadruple
		valType = 1
		valID = p[1]
		createArithmeticQuadruple(12, [p[3], 1], None, [VarDic[valID][2], valType], p)
	else:
		auxList = tempArrayStack.pop()
		addVarDictionary( p[1], None, 1, auxList, p )

def p_VAR_ARRAY(p):
	"""
	VAR_ARRAY : OB seen_ARRAY_LIMIT CB VAR_ARRAY
	| 
	"""

	global tempArray, tempArraySize
	if len(p) is 1:
		tempArray.append(tempArraySize)
		tempArrayStack.append(list(tempArray))
		tempArray[:] = []
		tempArraySize = 1
		

def p_seen_ARRAY_LIMIT(p):
	"""
	seen_ARRAY_LIMIT : INT
	"""

	global tempArray, tempArraySize
	tempArray.append(p[1])
	tempArraySize = tempArraySize * int(p[1])

def p_VARI(p):
	"""
	VARI : VARISMALL VARI3 PC 
	"""

def p_VARI3(p):
	"""
	VARI3 : IDV EQUALS INT COMMA VARI3
		| IDV EQUALS INT
		| IDV VAR_ARRAY COMMA VARI3
		| IDV VAR_ARRAY
	"""
	#varI is type var 0
	if p[2] is '=':
		addVarDictionary( p[1], p[3], 0, [1], p )
		#add assignation quadruple
		valType = 0
		valID = p[1]
		createArithmeticQuadruple(12, [p[3], 0], None, [VarDic[valID][2], valType], p)
	else:
		auxList = tempArrayStack.pop()
		addVarDictionary( p[1], None, 0, auxList, p )

def p_VARST(p):
	"""
	VARST : VARSTSMALL VARST3 PC 
	"""

def p_VARST3(p):
	"""
	VARST3 : IDV EQUALS STRING COMMA VARST3
		| IDV EQUALS STRING
		| IDV VAR_ARRAY COMMA VARST3
		| IDV VAR_ARRAY
	"""

	#varST is type var 2
	if p[2] is '=':
		addVarDictionary( p[1], p[3], 2, [1], p )
		#add assignation quadruple
		valType = 2
		valID = p[1]
		createArithmeticQuadruple(12, [p[3], 2], None, [VarDic[valID][2], valType], p)
	else:
		auxList = tempArrayStack.pop()
		addVarDictionary( p[1], None, 2, auxList, p )

def p_BLOCKS(p):
	"""
	BLOCKS : OC VARS BLOCKS2 CC
		| OC VARS CC
		| OC BLOCKS2 CC
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

	if len(POper) > 0:
		top = POper.pop()
		if top in range(4, 10):
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(top, op1, op2, "t", p)
		else:
			POper.append(top)

def p_PARAM(p):
	"""
	PARAM : PARAM2 IDV
	"""
	#dependiendo del tipo de variable se guarda en el diccionario
	global tmptypeVar, TamList
	if tmptypeVar == 'vari':	
		addVarDictionary( p[2], None, 0, [1], p )
		ParList.append(0)
	if tmptypeVar == 'varf':	
		addVarDictionary( p[2], None, 1, [1], p )
		ParList.append(1)
	if tmptypeVar == 'vars':			
		addVarDictionary( p[2], None, 2, [1], p )
		ParList.append(2)

def p_PARAM2(p):
	"""
	PARAM2 : VARISMALL
   		| VARSTSMALL
   		| VARFSMALL
	"""
	global tmptypeVar	
	tmptypeVar = p[1]
	

def p_METHODS(p):
	"""
	METHODS : METHODS2 seen_IDM OP METHODS3 CP BLOCKS METHOD_UPDATE
		| METHODS2 seen_IDM OP METHODS3 CP BLOCKS METHOD_UPDATE METHODS
	"""

def p_METHOD_UPDATE(p):
	"""
	METHOD_UPDATE :
	"""

	#actualizar diccionario de metodos
	localTamList = list(TamList)
	MetDic[tmpIdMethod][4] = localTamList
	VarDic.clear()
	TamList[:] = [0,0,0]
	listQuadruple.append([25, None, None, None])

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
	"""
	#asigna a tmpMethod el nombre del metodo actual
	global tmpMethod
	if p[1] == "voidbox":
		tmpMethod = -1
	elif p[1] == "varibox":
		tmpMethod = 0
	elif p[1] == "varfbox":
		tmpMethod = 1
	elif p[1] == "varsbox":
		tmpMethod = 2

def p_METHODS3(p):
	"""
	METHODS3 : PARAM COMMA METHODS3
		| PARAM
		| 
	"""

	addMetDictionary( tmpIdMethod, tmpMethod, p )

def p_RETURN(p):
	"""
	RETURN : RETURNW EXPRESSION PC
	"""

	top = PilaO.pop()
	if tmpMethod is top[1]:
		listQuadruple.append([29, top[0], None, None])
	else:
		print("BoxesSemanticError: invalid return value type. In line: " +  str(p.lineno(1)))
		print "</body></html>"
		exit(1)

def p_ASSIGNATION(p):
	"""
	ASSIGNATION : seen_ID_ASSIGNATION seen_ARRAY_CTE end_ARRAY EQUALS EXPRESSION PC
	| seen_ID_ASSIGNATION EQUALS EXPRESSION PC
	"""

	op1 = PilaO.pop()
	
	if len(p) is 5:
		PilaO.pop()
		op2 = None
	else:
		op2 = PilaO.pop()

	if ID_AS in VarDic:
		valType = VarDic[ID_AS][1]
		if op2 is None:
			op2 = [VarDic[ID_AS][2], valType]
	elif ID_AS in MetDic['global'][1]:
		valType = MetDic['global'][1][ID_AS][1]
		if op2 is None:
			op2 = [MetDic['global'][1][ID_AS][2], valType]
	else:
		print("BoxesSemanticError: Non declared variable: " +  ID_AS)
		print "</body></html>"
		exit(1)

	createArithmeticQuadruple(12, op1, None, op2, p)
	
def p_seen_ID_ASSIGNATION(p):
	"""
	seen_ID_ASSIGNATION : IDV
	"""

	
	PilaO.append(p[1])
	global ID_AS
	ID_AS = p[1]
	

def p_EXPRESSION(p):
	"""
	EXPRESSION : OPER seen_EXPF
		| OPER seen_EXPF seen_OPER EXPRESSION
	"""

def p_seen_EXPF(p):
	"""
	seen_EXPF :

	"""
	if len(POper) > 0:
		top = POper.pop()
		if top is '+':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(0, op1, op2, "t", p)
		elif top is '-':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(1, op1, op2, "t", p)
		elif top == """or""":
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(11, op1, op2, "t", p)
		else:
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
	if len(POper) > 0:
		top = POper.pop()
		if top is '*':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(2, op1, op2, "t", p)
		elif top is '/':
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(3, op1, op2, "t", p)
		elif top == """and""":
			op2 = PilaO.pop()
			op1 = PilaO.pop()
			createArithmeticQuadruple(10, op1, op2, "t", p)
		else:
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
	| seen_ID seen_ARRAY_CTE end_ARRAY
	"""

	global valType, valID
	#borra varID de PilaO
	if len(p) is 1:
		PilaO.pop()

	#agrega constante
	if valID is None or len(p) is not 4:
		if p[1] in ConDic:
			PilaO.append([ConDic[p[1]], valType])
		else:
			if valType is 0:
				memDir = memConst.addVari()
			elif valType is 1:
				memDir = memConst.addVarf()
			elif valType is 2:
				memDir = memConst.addVars()
			ConDic[p[1]] = memDir
			PilaO.append([memDir, valType])
	#agrega variable
	elif len(p) is not 4:
		if valID in VarDic:
			PilaOapp = [VarDic[valID][2], valType]
			
		elif valID in MetDic["global"][1]:
			PilaOapp = [MetDic["global"][1][valID][2], valType]
		else:
			print("BoxesSemanticError: Non declared variable: " + p[1] + ". In line: " + str(p.lineno(1)))
			print "</body></html>"
			exit(1)
		if len(p) is not 3:
			PilaO.append(PilaOapp)
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
	"""

	global valType, valID
	PilaO.append(p[1])
	if len(p) is 2:
		if p[1] in VarDic:
			valType = VarDic[p[1]][1]
			valID = p[1]
		elif p[1] in MetDic['global'][1]:
			valType = MetDic['global'][1][p[1]][1]
			valID = p[1]
		else:
			print("BoxesSemanticError: Non declared variable: " + p[1] + ". In line: " + str(p.lineno(1)))
			print "</body></html>"
			exit(1)



def p_seen_ARRAY_CTE(p):
	"""
	seen_ARRAY_CTE : OB start_ARRAY EXPRESSION seen_EXPRESSION_ARRAY CB  seen_ARRAY_CTE
	| OB start_ARRAY EXPRESSION seen_EXPRESSION_ARRAY CB
	"""
	global varID
	varID = None

def p_start_ARRAY(p):
	"""
	start_ARRAY :
	"""

	global varID
	if varID is None:
		varID = PilaO.pop()
	
	if len(VarDic[varID][3]) is 1:
		print("BoxesSemanticError: Var is not array: " + varID + ". In line: " + str(p.lineno(1)))
		print "</body></html>"
		exit(1)
	else:
		global pilaDim, arrayLength
		dim = 0
		pilaDim.append([varID, dim])
		POper.append('(')
		arrayLength = VarDic[varID][3][len(VarDic[varID][3]) - 1]

def p_end_ARRAY(p):
	"""
	end_ARRAY :
	"""

	aux = PilaO.pop()
	temporal = memTemp.addVari()
	varDIM = pilaDim.pop() #varID = [id, DIM]
	base = VarDic[varDIM[0]][2]
	if base in ConDic:
		memDir = ConDic[base]
	else:
		memDir = memConst.addVari()
		ConDic[base] = memDir
	listQuadruple.append([0, aux[0], memDir, (temporal * -1)])
	PilaO.append([(temporal * -1), 0])
	POper.pop()

def p_seen_EXPRESSION_ARRAY(p):
	"""
	seen_EXPRESSION_ARRAY :
	"""

	global arrayLength, pilaDim
	result = PilaO.pop()
	varDIM = pilaDim.pop() #varDIM = [id, DIM]
	if str(VarDic[varDIM[0]][3][varDIM[1]]) in ConDic:
		memDir = ConDic[str(VarDic[varDIM[0]][3][varDIM[1]])]
	else:
		memDir = memConst.addVari()
		ConDic[str(VarDic[varDIM[0]][3][varDIM[1]])] = memDir
	listQuadruple.append([30, result[0], None, memDir])

	if varDIM[1] < len(VarDic[varDIM[0]][3]) - 2 or varDIM[1] is 0:
		m = arrayLength / int(VarDic[varDIM[0]][3][varDIM[1]])
		arrayLength = m
		if str(m) in ConDic:
			memDir = ConDic[str(m)]
		else:
			memDir = memConst.addVari()
			ConDic[str(m)] = memDir
		temporal = memTemp.addVari()
		listQuadruple.append([2, result[0], memDir, temporal])
		PilaO.append([temporal, 0])
	if varDIM[1] > 0:
		aux = PilaO.pop()
		temporal = memTemp.addVari()
		listQuadruple.append([0, aux[0], result[0], temporal])
		PilaO.append([temporal, 0])

	varDIM[1] = varDIM[1] + 1
	pilaDim.append(varDIM)
	
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
		print("BoxesSemanticError: Non declared variable: " + p[5] + ". In line: " + str(p.lineno(1)))
		print "</body></html>"
		exit(1)

	if valType is 2:
		write = p[3]
		listQuadruple.append([24, write, None, VarDic[p[5]][2]])
	else:
		print("BoxesSemanticError: askuser() return value must be 'vars'. In line: " + str(p.lineno(1)))
		print "</body></html>"
		exit(1)

def p_CALLBOX(p):
	"""
	CALLBOX : CALLBOXW OP SEEN_IDM_CALL COMMA SEEN_CALL PARAMETERS CP PC  
		| CALLBOXW OP SEEN_IDM_CALL CP PC  
	"""
	listQuadruple.append([28, MetDic[tmpCallIDM][2], None, None])

def p_SEEN_IDM_CALL(p):
	"""
	SEEN_IDM_CALL : IDM  
	"""
	if p[1] not in MetDic:
		print("BoxesSemanticError: Non declared method: '" + p[1] + "'. In line: " + str(p.lineno(1)))
		print "</body></html>"
		exit(1)
	else:
		global tmpCallIDM
		tmpCallIDM = p[1]

def p_SEEN_CALL(p):
	"""
	SEEN_CALL :  
	"""
	listQuadruple.append([26, tmpCallIDM, None, None])
	global k
	k = 0

def p_PARAMETERS(p):
	"""
	PARAMETERS :  SEEN_EXPRESSION_PARAM COMMA PARAMETERS
			| SEEN_EXPRESSION_PARAM
	"""
	if len(MetDic[tmpCallIDM][3]) is not k:
		print("BoxesSemanticError: Missing Parameters in callbox. In line: " + str(p.lineno(1)))
		print "</body></html>"
		exit(1)
	

def p_SEEN_EXPRESSION_PARAM(p):
	"""
	SEEN_EXPRESSION_PARAM :	EXPRESSION
	"""
	global k
	argumento = PilaO.pop()
	if argumento[1] is MetDic[tmpCallIDM][3][k]:
		listQuadruple.append([27, argumento[0], None, "p"+str(k)])
		k = k + 1
	else:
		print("BoxesSemanticError: Parameter [" + str(k+1) + "] in callbox mismatched.")
		print "</body></html>"
		exit(1)

def p_LOOP(p):
	"""
	LOOP : LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 BY LOOP3 LOOP2 CP seen_CP_LOOP1 OC BLOCKS2 CC
	| LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 CP seen_CP_LOOP2 OC BLOCKS2 CC
	| LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 BY LOOP3 LOOP2 CP seen_CP_LOOP1 OC CC
	| LOOPW seen_LOOP OP seen_VAR_LOOP FROM LOOP2 TO LOOP2 CP seen_CP_LOOP2 OC CC
	"""

	#saca la variable a aumentar de la pila de operandos
	start = PilaO.pop()
	#crea cuadruplo de aumento
	createArithmeticQuadruple(0, start, aumento, "t", p)

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
	global aumento, simbol
	aumento = PilaO.pop()
	aumento[0] = str(int(aumento[0]) * simbol)
	end = PilaO.pop()
	start = PilaO.pop()

	global valID, valType
	createArithmeticQuadruple(12, start, None, [valID, valType], p)

	start = [VarDic[valID][2], valType]
	PilaO.append(start)
	if simbol is -1:
		createArithmeticQuadruple(6, start, end, "t", p)
	else:
		createArithmeticQuadruple(5, start, end, "t", p)

	aux = PilaO.pop()
	createGoToQuadruple(20, aux[0], None, None)
	PSaltos.append(len(listQuadruple)-1)

def p_seen_CP_LOOP2(p):
	"""
	seen_CP_LOOP2 :
	"""

	global aumento
	aumento = [1, 0]
	end = PilaO.pop()
	start = PilaO.pop()

	global valID, valType
	createArithmeticQuadruple(12, start, None, [valID, valType], p)

	start = [VarDic[valID][2], valType]
	PilaO.append(start)
	createArithmeticQuadruple(5, start, end, "t", p)

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
		print "</body></html>"
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
    print "</body></html>"
    exit(1)


import profile

# Build the grammar
yacc.yacc(method='LALR')
#READ CODE
with open(sys.argv[1],'r') as content_file:
	sourceCode = content_file.read()

# # Create instance of FieldStorage 
# form = cgi.FieldStorage() 
# # Get data from fields
# sourceCode = form.getvalue('code')

# print "Content-type: text/html"
# print
# print "<html><head>"
# print ""
# print "</head><body>"

# #parse code
# print sourceCode
yacc.parse(sourceCode)
outputDic = {'proc': MetDic, 'quad': listQuadruple, 'cons': ConDic}

print json.dumps(outputDic)
print "</body></html>"
print("<<SUCCESS>>")
print PilaO
#profile.run("yacc.yacc(method='LALR')")




