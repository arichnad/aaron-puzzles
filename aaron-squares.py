#!/usr/bin/python3

N=4
walls = [[[True for i in range(N)] for j in range(N)] for direction in range(2)]
answers=[]

def tryEach(j, i, direction, deadEnds):
	if direction == 2:
		direction=0
		#performance improvement:
		directions=getDirections(j, i)
		if failCell(directions):
			return
		#performance improvement:
		deadEnds += 1 if directions == 3 else 0
		if deadEnds >= 3:
			return
		i+=1
		if i==N:
			i=0
			j+=1
			if j==N:
				return testWalls()
	walls[direction][j][i]=True
	tryEach(j, i, direction+1, deadEnds)
	
	if direction == 0 and i==N-1 or direction == 1 and j==N-1:
		#skip
		return
	walls[direction][j][i]=False
	tryEach(j, i, direction+1, deadEnds)

def isWall(j, i, direction):
	actualDirection=direction&1
	negative=direction>>1!=0
	if negative:
		if actualDirection==0:
			i-=1
		else:
			j-=1
	if j<0 or i<0:
		return True
	return walls[actualDirection][j][i]

def printWalls(input):
	for i in range(N):
		print(' _', end='')
	print()
	for j in range(N):
		print('|',end='')
		for i in range(N):
			print(' ', end='')
			print('|' if input[0][j][i] else ' ', end='')
		print()
		print(' ',end='')
		for i in range(N):
			print('_' if input[1][j][i] else ' ', end='')
			print(' ', end='')
		print()
	print()
	print()
	print()

def rotate(input):
	#clockwise
	output = [[[True for i in range(N)] for j in range(N)] for direction in range(2)]
	for j in range(N):
		for i in range(N):
			output[1][j][i]=input[0][N-1-i][j]
		for i in range(N-1):
			output[0][j][i]=input[1][N-2-i][j]
	return output

def flip(input):
	#horizontal
	output = [[[True for i in range(N)] for j in range(N)] for direction in range(2)]
	for j in range(N):
		for i in range(N):
			output[1][j][i]=input[1][j][N-1-i]
		for i in range(N-1):
			output[0][j][i]=input[0][j][N-2-i]
	return output
	

def addAnswer():
	#make sure not a rotation of a previous	
	test=walls
	for direction in range(3):
		test=rotate(test)
		if test in answers:
			return
	test=flip(walls)
	if test in answers:
		return
	for direction in range(3):
		test=rotate(test)
		if test in answers:
			return

	print(len(answers))
	printWalls(walls)

	from copy import deepcopy
	answers.append(deepcopy(walls))

def floodFill(j, i, visited):
	if visited[j][i]:
		return 0
	visited[j][i]=True
	answer=1
	if i+1<N and not walls[0][j][i]:
		answer+=floodFill(j, i+1, visited)
	if i-1>=0 and not walls[0][j][i-1]:
		answer+=floodFill(j, i-1, visited)
	
	if j+1<N and not walls[1][j][i]:
		answer+=floodFill(j+1, i, visited)
	if j-1>=0 and not walls[1][j-1][i]:
		answer+=floodFill(j-1, i, visited)
	return answer

def failCell(directions):
	return directions<=1 or directions == 4

def getDirections(j, i):
	directions=0
	for direction in range(4):
		if isWall(j, i, direction):
			directions+=1
	return directions

def testWalls():
	#make sure 2 dead ends
	deadEnds=0
	for j in range(N):
		for i in range(N):
			directions=getDirections(j, i)
			if directions == 3:
				deadEnds+=1
				deadEnd = (j,i)
	if deadEnds != 2:
		return
	
	#make sure you can cover everything
	visited = [[False for i in range(N)] for j in range(N)]
	if floodFill(j,i,visited) != N*N:
		return
	
	addAnswer()


tryEach(0, 0, 0, 0)


