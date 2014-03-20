#Cubo Semantico
# DATA TYPES:
#	varI = 0
#	varF = 1
#	varST = 2
#
# OPERATORS
# 	[+ => 0]
# 	[- => 1] 
#	[* => 2]
#	[/ => 3] 
#	[== => 4] 
#	[< => 5]
#	[> => 6] 
#	[<= => 7] 
#	[<= => 8]
#

n = 3 #dim 1
o = 3 #dim 2
p = 9 #dim 3
cube = [[[0 for k in xrange(n)] for j in xrange(o)] for i in xrange(p)]

# varI #
cube[0][0][0]= 0; # varI + varI = varI
cube[0][0][1]= 0; # varI - varI = varI
cube[0][0][2]= 0; # varI * varI = varI
cube[0][0][3]= 0; # varI / varI = varI
cube[0][0][4]= 0; # varI == varI = varI [0, 1]
cube[0][0][5]= 0; # varI < varI = varI [0, 1]
cube[0][0][6]= 0; # varI > varI = varI [0, 1]
cube[0][0][7]= 0; # varI <= varI = varI [0, 1]
cube[0][0][8]= 0; # varI >= varI = varI [0, 1]

cube[0][1][0]= 1; # varI + varF = varF
cube[0][1][1]= 1; # varI - varF = varF
cube[0][1][2]= 1; # varI * varF = varF
cube[0][1][3]= 1; # varI / varF = varF
cube[0][1][4]= 0; # varI == varF = varI [0, 1]
cube[0][1][5]= 0; # varI < varF = varI [0, 1]
cube[0][1][6]= 0; # varI > varF = varI [0, 1]
cube[0][1][7]= 0; # varI <= varF = varI [0, 1]
cube[0][1][8]= 0; # varI >= varF = varI [0, 1]

cube[0][2][0]= -1; # varI + varST = ERROR
cube[0][2][1]= -1; # varI - varST = ERROR
cube[0][2][2]= -1; # varI * varST = ERROR
cube[0][2][3]= -1; # varI / varST = ERROR
cube[0][2][4]= -1; # varI == varST = ERROR
cube[0][2][5]= -1; # varI < varST = ERROR
cube[0][2][6]= -1; # varI > varST = ERROR
cube[0][2][7]= -1; # varI <= varST = ERROR
cube[0][2][8]= -1; # varI >= varST = ERROR

# varF #
cube[1][0][0]= 1; # varF + varI = varF
cube[1][0][1]= 1; # varF - varI = varF
cube[1][0][2]= 1; # varF * varI = varF
cube[1][0][3]= 1; # varF / varI = varF
cube[1][0][4]= 0; # varF == varI = varI [0, 1]
cube[1][0][5]= 0; # varF < varI = varI [0, 1]
cube[1][0][6]= 0; # varF > varI = varI [0, 1]
cube[1][0][7]= 0; # varF <= varI = varI [0, 1]
cube[1][0][8]= 0; # varF >= varI = varI [0, 1]

cube[1][1][0]= 1; # varF + varF = varF
cube[1][1][1]= 1; # varF - varF = varF
cube[1][1][2]= 1; # varF * varF = varF
cube[1][1][3]= 1; # varF / varF = varF
cube[1][1][4]= 0; # varF == varF = varI [0, 1]
cube[1][1][5]= 0; # varF < varF = varI [0, 1]
cube[1][1][6]= 0; # varF > varF = varI [0, 1]
cube[1][1][7]= 0; # varF <= varF = varI [0, 1]
cube[1][1][8]= 0; # varF >= varF = varI [0, 1]

cube[1][2][0]= -1; # varF + varST = ERROR
cube[1][2][1]= -1; # varF - varST = ERROR
cube[1][2][2]= -1; # varF * varST = ERROR
cube[1][2][3]= -1; # varF / varST = ERROR
cube[1][2][4]= -1; # varF == varST = ERROR
cube[1][2][5]= -1; # varF < varST = ERROR
cube[1][2][6]= -1; # varF > varST = ERROR
cube[1][2][7]= -1; # varF <= varST = ERROR
cube[1][2][8]= -1; # varF >= varST = ERROR

# varST #
cube[2][0][0]= -1; # varST + varI = ERROR
cube[2][0][1]= -1; # varST - varI = ERROR
cube[2][0][2]= -1; # varST * varI = ERROR
cube[2][0][3]= -1; # varST / varI = ERROR
cube[2][0][4]= -1; # varST == varI = ERROR
cube[2][0][5]= -1; # varST < varI = ERROR
cube[2][0][6]= -1; # varST > varI = ERROR
cube[2][0][7]= -1; # varST <= varI = ERROR
cube[2][0][8]= -1; # varST >= varI = ERROR

cube[2][1][0]= -1; # varST + varF = ERROR
cube[2][1][1]= -1; # varST - varF = ERROR
cube[2][1][2]= -1; # varST * varF = ERROR
cube[2][1][3]= -1; # varST / varF = ERROR
cube[2][1][4]= -1; # varST == varF = ERROR
cube[2][1][5]= -1; # varST < varF = ERROR
cube[2][1][6]= -1; # varST > varF = ERROR
cube[2][1][7]= -1; # varST <= varF = ERROR
cube[2][1][8]= -1; # varST >= varF = ERROR

cube[2][2][0]= -1; # varST + varST = ERROR
cube[2][2][1]= -1; # varST - varST = ERROR
cube[2][2][2]= -1; # varST * varST = ERROR
cube[2][2][3]= -1; # varST / varST = ERROR
cube[2][2][4]= 0; # varST == varST = varI [0, 1]
cube[2][2][5]= -1; # varST < varST = ERROR
cube[2][2][6]= -1; # varST > varST = ERROR
cube[2][2][7]= -1; # varST <= varST = ERROR
cube[2][2][8]= -1; # varST >= varST = ERROR