#!/usr/bin/python3

import random

class Card:
	def __init__(self, suit, value):
		self.suit = suit
		self.value = value
	@classmethod
	def fromIntegerCard(cls, integerCard):
		suit=integerCard//13
		return cls(suit, integerCard-suit*13)
	
	def __eq__(self, other):
		return self.suit==other.suit and self.value==other.value
	def __hash__(self):
		#heh.  kinda weird to use 13 here, but why not?
		return hash(self.suit)*13+hash(self.value)
	def __repr__(self):
		#return str((list(range(2,10))+['t','j','q','k','a'])[self.value]) + chr([0x2660,0x2663,0x2665,0x2666][self.suit])
		cardValue = self.value
		if cardValue == 12: cardValue = -1
		cardValue += 1
		if cardValue >= 11: cardValue += 1
		return chr(0x1f0a1 + self.suit*16 + cardValue)

remainingDeck = set([Card.fromIntegerCard(integerCard) for integerCard in range(52)])

playersHand = set()
housesHand = set()
	
#double monte-carlo
SCENARIO_COUNT = 10000
PLAYER_SCENARIO_COUNT = 50
#RECURSE_DEPTH of 4 is the "adrian method".  TOO SLOW!
#RECURSE_DEPTH of 0 is the "aaron method"
#RECURSE_DEPTH of 1 is a hybrid-method.  VERY slow but higher score.
RECURSE_DEPTH = 1

def pickCards(stage):
	#the stage# is the same as the number of cards we get back:
	global remainingDeck
	return set(random.sample(remainingDeck, stage))


def straightFlushHand(hand):
	for suit in range(4):
		cards=flushHandSuit(hand, suit)
		if cards is not None:
			cards=straightHand(cards)
			if cards is not None:
				return cards

def flushHandSuit(hand, suit):
	hand = set(card for card in hand if card.suit == suit)
	if len(hand)<5: return None
	return sortedHand(hand)[:5]

def flushHand(hand):
	for suit in range(4):
		cards = flushHandSuit(hand, suit)
		if cards is not None: return cards
	return None

def straightHand(hand):
	valuesHand = set(card.value for card in hand)
	length=0
	for cardValue in reversed(range(-1,13)):
		if cardValue == -1: cardValue = 12
		if cardValue not in valuesHand:
			length=0
			continue
		length+=1
		if length == 5:
			if cardValue == 12: cardValue = -1
			outputHand = []
			for cardValue in reversed(range(cardValue, cardValue+5)):
				if cardValue == -1: cardValue = 12
				outputHand.append([card for card in hand if card.value==cardValue][0])
			return outputHand

def ofKindHands(hand):
	valueOutput = {}
	valueCount = [0 for value in range(13)]
	suitCount = [0 for value in range(4)]
	suitOutput = []
	for card in hand:
		valueCount[card.value]+=1
		suitCount[card.suit]+=1
	for cardValue in reversed(range(13)):
		current = valueCount[cardValue]
		if current >= 2:
			if current not in valueOutput:
				valueOutput[current] = []
			valueOutput[current].append([card for card in hand if card.value==cardValue])
	for cardSuit in range(4):
		current = suitCount[cardValue]
		if current >= 5:
			suitOutput.append([card for card in hand if card.suit==cardSuit])
	return valueOutput, suitOutput


#just unwrap the map
def removeDuplicates(ofKindHands):
	return {key: sortedHand(value[0]) for key, value in ofKindHands.items()}

TIE_GAME=0
PLAYER_1_WINS=1
PLAYER_2_WINS=2

#high card assumes that one of the players has a 5-card hand?
def highCard(player1Hand, player2Hand):
	player1Hand = sortedHand(player1Hand)
	player2Hand = sortedHand(player2Hand)
	#zip with different sizes, it stops at the shortest list.  that's what we want
	for player1Card, player2Card in zip(player1Hand, player2Hand):
		if player1Card.value == player2Card.value: continue
		return PLAYER_1_WINS if player1Card.value > player2Card.value else PLAYER_2_WINS
	return TIE_GAME

def returnWinTie(player1Hand, player2Hand, player1FullHand, player2FullHand):
	highCardValue = highCard(player1Hand, player2Hand)
	if highCardValue != TIE_GAME:
		#TODO, this will fail because it'll return ace even if it's a 5 high straight
		return highCardValue
	player1Hand = set(player1Hand)
	player2Hand = set(player2Hand)
	player1FullHand -= player1Hand
	player2FullHand -= player2Hand
	returnValue = highCard(player1FullHand, player2FullHand)
	player1FullHand |= player1Hand
	player2FullHand |= player2Hand
	return returnValue

def returnWinTie2(player1Hand, player2Hand, player1HandB, player2HandB, player1FullHand, player2FullHand):
	highCardValue = highCard(player1Hand, player2Hand)
	if highCardValue != TIE_GAME:
		return highCardValue
	player1Hand = set(player1Hand)
	player2Hand = set(player2Hand)
	player1FullHand -= player1Hand
	player2FullHand -= player2Hand
	returnValue = returnWinTie(player1HandB, player2HandB, player1FullHand, player2FullHand)
	player1FullHand |= player1Hand
	player2FullHand |= player2Hand
	return returnValue


def returnWin(player1Hand, player2Hand, player1FullHand, player2FullHand):
	if player1Hand is not None and player2Hand is not None:
		return returnWinTie(player1Hand, player2Hand, player1FullHand, player2FullHand)
	if player1Hand is not None:
		return PLAYER_1_WINS
	if player2Hand is not None:
		return PLAYER_2_WINS
	return None

def playerWinsHand(player1Hand, player2Hand):
	#verbose means that we keep all of the pairs
	ofKindHands1Verbose,flushOutput1=ofKindHands(player1Hand)
	ofKindHands2Verbose,flushOutput2=ofKindHands(player2Hand)

	ofKindHands1 = removeDuplicates(ofKindHands1Verbose)
	ofKindHands2 = removeDuplicates(ofKindHands2Verbose)

	if len(flushOutput1)>0 or len(flushOutput2)>0:
		win = returnWin(straightFlushHand(player1Hand), straightFlushHand(player2Hand), player1Hand, player2Hand)
		if win is not None: return win

	win = returnWin(ofKindHands1.get(4), ofKindHands2.get(4), player1Hand, player2Hand)
	if win is not None: return win

	if 3 in ofKindHands1 and 2 in ofKindHands1 and 3 in ofKindHands2 and 2 in ofKindHands2:
		return returnWinTie2(ofKindHands1[3], ofKindHands2[3], ofKindHands1[2], ofKindHands2[2], player1Hand, player2Hand)
	
	if 3 in ofKindHands1 and 2 in ofKindHands1: return PLAYER_1_WINS
	if 3 in ofKindHands2 and 2 in ofKindHands2: return PLAYER_2_WINS
	
	win = returnWin(flushOutput1[0] if len(flushOutput1)>0 else None, flushOutput2[0] if len(flushOutput2)>0 else None, player1Hand, player2Hand)
	if win is not None: return win

	win = returnWin(straightHand(player1Hand), straightHand(player2Hand), player1Hand, player2Hand)
	if win is not None: return win
	
	win = returnWin(ofKindHands1.get(3), ofKindHands2.get(3), player1Hand, player2Hand)
	if win is not None: return win

	if 2 in ofKindHands1 and len(ofKindHands1Verbose[2])>=2 and 2 in ofKindHands2 and len(ofKindHands2Verbose[2])>=2:
		return returnWinTie2(ofKindHands1Verbose[2][0], ofKindHands2Verbose[2][0], ofKindHands1Verbose[2][1], ofKindHands2Verbose[2][1], player1Hand, player2Hand)
	
	if 2 in ofKindHands1 and len(ofKindHands1Verbose[2])>=2: return PLAYER_1_WINS
	if 2 in ofKindHands2 and len(ofKindHands2Verbose[2])>=2: return PLAYER_2_WINS
	
	win = returnWin(ofKindHands1.get(2), ofKindHands2.get(2), player1Hand, player2Hand)
	if win is not None: return win

	return returnWinTie(player1Hand, player2Hand, player1Hand, player2Hand)

def runScenarios(scenarioCount, stage, recurseDepth, printIt=False):
	output={PLAYER_1_WINS: 0, PLAYER_2_WINS: 0, TIE_GAME: 0}
	for scenario in range(scenarioCount):
		if printIt:
			#print('starting a scenario')
			if scenario%10==0:
				print('.', end='', flush=True)
		output[runOneScenario(stage, recurseDepth, printIt)]+=1
	return output


def runOneScenario(stage, recurseDepth, printIt):
	global remainingDeck, playersHand, housesHand
	if stage == 6:
		return playerWinsHand(playersHand, housesHand)
	elif recurseDepth is not None and recurseDepth == 0:
		#"hybrid" aaron-method.  once you reach your "recurse depth", then pick out the remaining cards.
		dummyPlayerPool = pickCards(5-len(playersHand))
		dummyHousePool = pickCards(10-len(housesHand))
		playersHand |= dummyPlayerPool
		housesHand |= dummyHousePool
		
		returnValue = playerWinsHand(playersHand, housesHand)

		housesHand -= dummyHousePool
		playersHand -= dummyPlayerPool
		
		return returnValue
	
	pool = pickCards(stage)
	remainingDeck -= pool

	bestCard, bestWins = None, None
	if len(pool)==1:
		bestCard = next(iter(pool))
	else:
		for pickedCard in set(pool):
			pool.remove(pickedCard)
			playersHand.add(pickedCard)
			housesHand |= pool
			
			playerWins=runScenarios(PLAYER_SCENARIO_COUNT, stage+1, RECURSE_DEPTH if recurseDepth is None else recurseDepth - 1)[PLAYER_1_WINS]

			housesHand -= pool
			playersHand.remove(pickedCard)
			pool.add(pickedCard)
			
			if bestWins is None or playerWins > bestWins:
				bestWins = playerWins
				bestCard = pickedCard
	
	pickedCard = bestCard
	
	#if printIt:
	#	print('%d: %s vs %s got a pool of %s picked the %s' % (stage, printHand(playersHand|set([pickedCard])), printHand(housesHand|pool-set([pickedCard])), printHand(pool), printCard(bestCard)))
	
	pool.remove(pickedCard)
	playersHand.add(pickedCard)
	housesHand |= pool

	returnValue = runOneScenario(stage+1, None if recurseDepth is None else recurseDepth - 1, printIt)
	
	housesHand -= pool
	playersHand.remove(pickedCard)
	pool.add(pickedCard)
	
	remainingDeck |= pool

	return returnValue

def sortedHand(hand):
	return list(sorted(hand, reverse=True, key = lambda card : card.value))


def printHand(hand):
	hand=sortedHand(hand)
	return ' '.join([str(card) for card in hand])

#for scenario in range(1000):
	#playersHandTest = pickCards(5)
	#housesHandTest = pickCards(10)
	#print('%s vs %s  = %d wins' % (printHand(playersHandTest), printHand(housesHandTest), playerWinsHand(playersHand, housesHand)))
	#hand = flushHand(cards)
	#if hand is not None:
	#	print('from ' + printHand(cards) + ' got a flush: ' + printHand(hand))
	#hand = straightHand(cards)
	#if hand is not None:
	#	print('from ' + printHand(cards) + ' got a straight: ' + printHand(hand))
	#hand = straightFlushHand(cards)
	#if hand is not None:
	#	print('from ' + printHand(cards) + ' got a straight flush: ' + printHand(hand))
	#hand = ofKindHands(cards)
	#if 4 in hand:
	#	print('from ' + printHand(cards) + ' got a 4-of a kind: ' + printHand(hand[4][0]))


print(printHand(remainingDeck))
print(runScenarios(SCENARIO_COUNT, 1, None, True))
print(printHand(remainingDeck))

