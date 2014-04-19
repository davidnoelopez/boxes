class MemoryDir:
	def __init__(self, varis, varfs, varss, limit):
		self.varis = [varis, 0];
		self.varfs = [varfs, 0];
		self.varss = [varss, 0];
		self.limit = limit;

	def __str__(self):
		return str(self.varis) + ' ' + str(self.varfs) + ' ' + str(self.varss) + ' ' + str(self.limit)

	def addVari(self, x=1):
		if (self.varis[0] + self.varis[1] + x) < self.varfs[0]:
			self.varis[1] = self.varis[1] + x
			return (self.varis[0] + self.varis[1] - x)
		else:
			print "StackOverflow!"
			exit(1)

	def addVarf(self, x=1):
		if (self.varfs[0] + self.varfs[1] + x) < self.varss[0]:
			self.varfs[1] = self.varfs[1] + x
			return (self.varfs[0] + self.varfs[1] - x)
		else:
			print "StackOverflow!"
			exit(1)

	def addVars(self, x=1):
		if (self.varss[0] + self.varss[1] + x) < self.limit:
			self.varss[1] = self.varss[1] + x
			return (self.varss[0] + self.varss[1] - x)
		else:
			print "StackOverflow!"
			exit(1)
