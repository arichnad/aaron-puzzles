#!/usr/bin/python3

MAX_VALUE=100000

def findTie(boxNumber, boxes, totalA, totalB, totalLeft):
	if abs(totalB - totalA) > totalLeft: return False
	if boxNumber == 0:
		return totalA == totalB and totalA > 0
	boxNumber-=1
	totalLeft-=boxes[boxNumber]
	return findTie(boxNumber, boxes, totalA+boxes[boxNumber], totalB, totalLeft) or findTie(boxNumber, boxes, totalA, totalB+boxes[boxNumber], totalLeft) or findTie(boxNumber, boxes, totalA, totalB, totalLeft)

	
def findBoxes(totalBoxes, boxNumber, maxValue, boxes, total):
	if boxNumber == 0:
		if findTie(totalBoxes, boxes, 0, 0, total):
			return False
		return boxes
	boxNumber-=1
	for i in range(1, maxValue):
	#for i in reversed(range(1, maxValue)) if totalBoxes != boxNumber+1 else range(1, maxValue):
		#if totalBoxes == boxNumber+1: print(i)
		boxes[boxNumber]=i
		if findBoxes(totalBoxes, boxNumber, i, boxes, total+i):
			return boxes

for f in range(1, 10):
	answer=findBoxes(f, f, MAX_VALUE, [0 for i in range(f)], 0)
	print(answer[f-1], list(reversed(answer)))

