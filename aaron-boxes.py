#!/usr/bin/python3

MAX_VALUE=100000

def findSets(totalBoxes, boxNumber, maxValue, sets):
	if boxNumber == 0:
		if not trySets(totalBoxes, sets, 0, 0):
			return sets
		return False
	boxNumber-=1
	for i in range(1, maxValue):
		#if totalBoxes == boxNumber+1: print(i)
		sets[boxNumber]=i
		if findSets(totalBoxes, boxNumber, i, sets):
			return sets

def trySets(boxNumber, sets, totalA, totalB):
	if boxNumber == 0:
		return totalA == totalB and totalA > 0
	boxNumber-=1
	return trySets(boxNumber, sets, totalA+sets[boxNumber], totalB) or trySets(boxNumber, sets, totalA, totalB+sets[boxNumber]) or trySets(boxNumber, sets, totalA, totalB)

	
for f in range(1, 10):
	answer=findSets(f, f, MAX_VALUE, [0 for i in range(f)])
	print(answer[f-1], answer)

