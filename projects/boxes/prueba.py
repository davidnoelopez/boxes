queue = [1, "[", 3, "[", 4, "[", 5, 6, "]", "]", "]"]

def queueToList():
	if len(queue) is 0:
		return []
	else:
		element = queue[0]
		queue.pop(0)
		print element
		if element is "[":
			return [queueToList()]
		elif element is "]":
			return queueToList()
		else:
			return [element] + queueToList()

testList = queueToList()
print testList
