from memStruct import MemoryDir

memGlobal = MemoryDir(0, 2, 200, 300)

direccion = memGlobal.addVari()
direccion = memGlobal.addVari()
print (memGlobal)
print (direccion)