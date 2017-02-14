#!/usr/bin/python3

#automatically generate puzzles involving making change for other people

#you have three people, paul, miguel, and adrian, and they all have different amounts of money. 

#miguel wants to pay adrian $2.00

#paul has two $10 bills, four $1 bills, 3 quarters, and 3 dimes. miguel has a $20 and a $5. adrian has a $10 and two nickels.

#dynamic programming

import random
import uuid
random.seed(100)

class person:
	def __init__(self):
		self.units = randomUnits()
		print([unit.unitAmount for unit in self.units])

class unit:
	def __init__(self, unitAmount):
		self.id = uuid.uuid4()
		self.unitAmount = unitAmount

def randomUnits():
	UNITS = random.randrange(4, 6)
	units = [1, 5, 25, 100, 500, 1000, 2000]
	unitList = list(sorted([units[random.randrange(len(units))] for i in range(UNITS)]))
	return [unit(unitAmount) for unitAmount in unitList]

def addToPossibilities(possibilities, person, multiplier = 1):
	for unit in person.units:
		for amount in possibilities.copy():
			for whichWay in possibilities[amount]:
				newEntry = amount + unit.unitAmount * multiplier
				if newEntry in whichWay:
					continue
				if unit in whichWay:
					continue
				newList = list(whichWay)
				newList.append(unit)
				if not newEntry in possibilities:
					possibilities[newEntry] = []
				possibilities[newEntry].append(newList)
	return possibilities

def generatePuzzle():
	people = [ person() for i in range(3) ]
	possibilities = {}
	possibilities[0] = [[]]
	#addTradesToPossibilities(possibilities, people[2], people[0])
	#addTradesToPossibilities(possibilities, people[2], people[1])
	possibilities = addToPossibilities(possibilities, people[0], 1)
	possibilities = addToPossibilities(possibilities, people[1], -1)

	#find the hardest thing
	for possibility in sorted(possibilities, key=lambda sortPossibility: len(possibilities[sortPossibility])):
		print(possibility, end=' => ')
		print(sorted([unit.unitAmount for unit in possibilities[possibility][len(possibilities[possibility])-1]]))

generatePuzzle()

