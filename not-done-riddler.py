#!/usr/bin/python3

#not done:  my attempt at https://fivethirtyeight.com/tag/the-riddler/


import random
import math
	
RUNS=100
MAX_VALUE=9

def winner(a, b):
	aTotal=0
	bTotal=0
	for i in range(10):
		if a[i]>b[i]:
			aTotal+=(i+1)*2
		elif a[i]<b[i]:
			bTotal+=(i+1)*2
		else:
			aTotal+=i+1
			bTotal+=i+1
	if aTotal>bTotal:
		return 1
	elif aTotal<bTotal:
		return -1
	return 0

def setWeight(particles):
	for particle in particles:
		particle['weight']=0
	for particle1 in particles:
		print('.')
		for particle2 in particles:
			if particle1 == particle2: continue
			aWin=bWin=0
			for i in range(RUNS):
				winnerAnswer=winner(strategy(particle1), strategy(particle2))
				if winnerAnswer>0:
					aWin+=1
				elif winnerAnswer<0:
					bWin+=1
			#print(particle1, aWin, particle2, bWin)
			if aWin > bWin:
				particle1['weight']+=1
			elif aWin < bWin:
				particle2['weight']+=1


#def resample(particles):
#	output = []
#	maximumWeight = max([particle['weight'] for particle in particles])
#	
#	particleKeep = 0
#	weight = 0
#	len = particles0.length
#	index = random.nextInt(len(particles))
#
#	for count in range(len(particles)):
#		particleKeep += random.nextDouble() * 2 * maximumWeight
#		while particleKeep > (weight = particles0[index].getWeight()):
#			particleKeep -= weight
#			index = (index + 1) % len
#		particles1[count].set(particles0[index])
#	return output



def iterate(particles):
	for particle in particles:
		print(particle, strategy(particle))

	print()
	print()
	setWeight(particles)
	print()
	print()

	sortedParticles = sorted(particles, key=lambda particle: particle['weight'], reverse=True)

	for particle in sortedParticles:
		print(particle)
	
	particles = killOff(particles)
	return particles



def strategy(options):
	if 'stupid' in options:
		return stupid(options['stupid'])
	
	stdDev=options['stdDev']
	group=options['group']
	strategy=[group for i in range(10)]
	MAX_VALUE=9

	function=options['function']



	for i in range(100-group*10):
		#value=round(random.lognormvariate(math.log(MAX_VALUE), stdDev))
		value=function(stdDev)
		if value > MAX_VALUE:
			value=MAX_VALUE*2-value
		if value < 0:
			value = 0
		strategy[value]+=1
	return strategy

def stupid(groups):
	#return [11,0,0,0,0,0,0,25,28,36]
	strategy=[0 for i in range(10)]
	armies=100//groups
	for pos in range(10-groups,10):
		strategy[pos]=armies
	strategy[9]+=100%groups
	return strategy

def normalFunction(stdDev):
	return round(random.normalvariate(MAX_VALUE, stdDev))

def logFunction(stdDev):
	return round(random.lognormvariate(math.log(MAX_VALUE), stdDev))

particles=[
	{'stupid': 2},
	{'stupid': 3},
	{'stupid': 4},
	{'stupid': 5},
]


#2.25, .35
#2.525, .275
#2.575, .275

for i in range(10):
	True
	#particles.append({'stdDev': i/(10), 'function': normalFunction, 'group': 1})
	#particles.append({'stdDev': i/(10), 'function': normalFunction, 'group': 50})

for i in range(10):
	particles.append({'stdDev': i/(10), 'function': logFunction, 'group': 0})
	particles.append({'stdDev': i/(10), 'function': logFunction, 'group': 1})
	#particles.append({'stdDev': i/(10), 'function': logFunction, 'group': 50})

