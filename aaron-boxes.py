#!/usr/bin/python3

MAX_VALUE=100000

def findSets(totalBoxes, boxNumber, maxValue, sets, total):
	if boxNumber == 0:
		if total % 2 == 0 or findTie(totalBoxes, sets, 0, 0, total):
			return False
		return sets
	boxNumber-=1
	for i in range(1, maxValue):
		if totalBoxes == boxNumber+1: print(i)
		sets[boxNumber]=i
		if findSets(totalBoxes, boxNumber, i, sets, total+i):
			return sets

def findTie(boxNumber, sets, totalA, totalB, totalLeft):
	if abs(totalB - totalA) > totalLeft: return False
	if boxNumber == 0:
		return totalA == totalB and totalA > 0
	boxNumber-=1
	totalLeft-=sets[boxNumber]
	return findTie(boxNumber, sets, totalA+sets[boxNumber], totalB, totalLeft) or findTie(boxNumber, sets, totalA, totalB+sets[boxNumber], totalLeft) or findTie(boxNumber, sets, totalA, totalB, totalLeft)

	
for f in range(1, 10):
	answer=findSets(f, f, MAX_VALUE, [0 for i in range(f)], 0)
	print(answer[f-1], answer)

