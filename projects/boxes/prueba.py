queue = ['"hola"', '1.2', '3', '[', '1', '2', '3', ']', '[', '1', '[', '2', ']', '[', '2', '[', '3', '4', ']', ']', ']']

def queueToList():
	if len(queue) is 0:
		return []
	else:
		element = queue[0]
		queue.pop(0)
		if element is "[":
			return [queueToList()] + queueToList()
		elif element is "]":
			return []
		else:
			return [element] + queueToList()

testList = queueToList()
print testList
