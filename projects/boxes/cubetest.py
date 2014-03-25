#Cubo Semantico
# DATA TYPES:
#	varI : 0
#	varF : 1
#	varST : 2
#
# OPERATION CODES
# 	(+ 	:> 0)
# 	(- 	:> 1) 
#	(* 	:> 2)
#	(/ 	:> 3) 
#	(== :> 4) 
#	(< 	:> 5)
#	(> 	:> 6) 
#	(<= :> 7) 
#	(>= :> 8)
#	(<>	:> 9)
#	(&&	:> 10)
#	(||	:> 11)
#	(= 	:> 12)
#	(GoToF 	:> 20)
#	(GoToT 	:> 21)
#	(GoTo 	:> 22)


# varI #
cube = {
(0,0,0): 0, # varI + varI : varI
 (0,0,1): 0, # varI - varI : varI
 (0,0,2): 0, # varI * varI : varI
 (0,0,3): 0, # varI / varI : varI
 (0,0,4): 0, # varI == varI : varI (0, 1)
 (0,0,5): 0, # varI < varI : varI (0, 1)
 (0,0,6): 0, # varI > varI : varI (0, 1)
 (0,0,7): 0, # varI <= varI : varI (0, 1)
 (0,0,8): 0, # varI >= varI : varI (0, 1)
 (0,0,9): 0, # varI = varI : varI (0, 1)

 (0,1,0): 1, # varI + varF : varF
 (0,1,1): 1, # varI - varF : varF
 (0,1,2): 1, # varI * varF : varF
 (0,1,3): 1, # varI / varF : varF
 (0,1,4): 0, # varI == varF : varI (0, 1)
 (0,1,5): 0, # varI < varF : varI (0, 1)
 (0,1,6): 0, # varI > varF : varI (0, 1)
 (0,1,7): 0, # varI <= varF : varI (0, 1)
 (0,1,8): 0, # varI >= varF : varI (0, 1)
 (0,1,9): -1, # varI = varF : ERROR

 (0,2,0): -1, # varI + varST : ERROR
 (0,2,1): -1, # varI - varST : ERROR
 (0,2,2): -1, # varI * varST : ERROR
 (0,2,3): -1, # varI / varST : ERROR
 (0,2,4): -1, # varI == varST : ERROR
 (0,2,5): -1, # varI < varST : ERROR
 (0,2,6): -1, # varI > varST : ERROR
 (0,2,7): -1, # varI <= varST : ERROR
 (0,2,8): -1, # varI >= varST : ERROR
 (0,2,9): -1, # varI = varST : ERROR

# varF #
 (1,0,0): 1, # varF + varI : varF
 (1,0,1): 1, # varF - varI : varF
 (1,0,2): 1, # varF * varI : varF
 (1,0,3): 1, # varF / varI : varF
 (1,0,4): 0, # varF == varI : varI (0, 1)
 (1,0,5): 0, # varF < varI : varI (0, 1)
 (1,0,6): 0, # varF > varI : varI (0, 1)
 (1,0,7): 0, # varF <= varI : varI (0, 1)
 (1,0,8): 0, # varF >= varI : varI (0, 1)
 (1,0,9): -1, # varF = varI : ERROR

 (1,1,0): 1, # varF + varF : varF
 (1,1,1): 1, # varF - varF : varF
 (1,1,2): 1, # varF * varF : varF
 (1,1,3): 1, # varF / varF : varF
 (1,1,4): 0, # varF == varF : varI (0, 1)
 (1,1,5): 0, # varF < varF : varI (0, 1)
 (1,1,6): 0, # varF > varF : varI (0, 1)
 (1,1,7): 0, # varF <= varF : varI (0, 1)
 (1,1,8): 0, # varF >= varF : varI (0, 1)
 (1,1,9): 1, # varF = varF : varI (0, 1)

 (1,2,0): -1, # varF + varST : ERROR
 (1,2,1): -1, # varF - varST : ERROR
 (1,2,2): -1, # varF * varST : ERROR
 (1,2,3): -1, # varF / varST : ERROR
 (1,2,4): -1, # varF == varST : ERROR
 (1,2,5): -1, # varF < varST : ERROR
 (1,2,6): -1, # varF > varST : ERROR
 (1,2,7): -1, # varF <= varST : ERROR
 (1,2,8): -1, # varF >= varST : ERROR
 (1,2,9): -1, # varF = varST : ERROR

# varST #
 (2,0,0): -1, # varST + varI : ERROR
 (2,0,1): -1, # varST - varI : ERROR
 (2,0,2): -1, # varST * varI : ERROR
 (2,0,3): -1, # varST / varI : ERROR
 (2,0,4): -1, # varST == varI : ERROR
 (2,0,5): -1, # varST < varI : ERROR
 (2,0,6): -1, # varST > varI : ERROR
 (2,0,7): -1, # varST <= varI : ERROR
 (2,0,8): -1, # varST >= varI : ERROR
 (2,0,9): -1, # varST = varI : ERROR

 (2,1,0): -1, # varST + varF : ERROR
 (2,1,1): -1, # varST - varF : ERROR
 (2,1,2): -1, # varST * varF : ERROR
 (2,1,3): -1, # varST / varF : ERROR
 (2,1,4): -1, # varST == varF : ERROR
 (2,1,5): -1, # varST < varF : ERROR
 (2,1,6): -1, # varST > varF : ERROR
 (2,1,7): -1, # varST <= varF : ERROR
 (2,1,8): -1, # varST >= varF : ERROR
 (2,1,9): -1, # varST = varF : ERROR

 (2,2,0): -1, # varST + varST : ERROR
 (2,2,1): -1, # varST - varST : ERROR
 (2,2,2): -1, # varST * varST : ERROR
 (2,2,3): -1, # varST / varST : ERROR
 (2,2,4): 0, # varST == varST : varI (0, 1)
 (2,2,5): -1, # varST < varST : ERROR
 (2,2,6): -1, # varST > varST : ERROR
 (2,2,7): -1, # varST <= varST : ERROR
 (2,2,8): -1, # varST >= varST : ERROR
 (2,2,9): 0 # varST = varST : varI (0, 1)
}
