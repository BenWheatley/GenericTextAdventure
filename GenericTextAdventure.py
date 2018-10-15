#!python

import string
import functools

class Room:
	def __init__(self, emptyRoomDescription, nodes = []):
		self.emptyRoomDescription = emptyRoomDescription
		self.nodes = nodes
	
	def getDescription(self):
		result = self.emptyRoomDescription
		for node in self.nodes:
			result += " " + node.getVagueDescription()
		return result
	
	def examine(self, noun):
		for node in self.nodes:
			if node.matchesNoun(noun):
				return node.getExamineDescription()
		return "There is no "+noun+" to examine!"
	
	def pickUp(self, noun):
		for node in self.nodes:
			if node.matchesNoun(noun):
				if node.goesInInventory():
					return node
				return None
		return None
		

class Node:
	def __init__(self, vague_description, examine_description, nouns = []):
		self._vague_description = vague_description
		self._examine_description = examine_description
		self._nouns = map(string.upper, nouns)
	
	def matchesNoun(self, otherNoun):
		return otherNoun.upper() in self._nouns
		
	def goesInInventory(self):
		return False
	
	def getVagueDescription(self):
		return self._vague_description
	
	def getExamineDescription(self):
		return self._examine_description

class Item(Node):
	def goesInInventory(self):
		return len(self._nouns)>0

class Exit(Node):
	def goesInInventory(self):
		return False

class Player:
	_inventory = []
	
	@staticmethod
	def addToInventory(item):
		if item.goesInInventory():
			Player._inventory.append(item)
	
	@staticmethod
	def getInventory():
		result = ", ".join(map(str, Player._inventory))
	

class Parser:
	EXAMINE = "EXAMINE"
	PICK_UP = "PICK_UP"
	INVENTORY = "INVENTORY"
	
	@staticmethod
	def splitInput(userInput):
		mapping = {}
		mapping[Parser.EXAMINE] = ["examine", "look at", "look", "observe", "view", "inspect"]
		mapping[Parser.PICK_UP] = ["pick up", "pick", "carry", "hold", "collect"]
		mapping[Parser.INVENTORY] = ["inventory"]
		
		for key in mapping:
			for v in mapping[key]:
				if userInput.startswith(v):
					return key, userInput[len(v)+1:]
		
		return None, None

for i in range(5):
	print


room = Room("You are in a plain grey room.")
room.nodes.append( Item("There is a wooden table.", "The wooden table is simple wood. Unvarnished and undecorated, it could have been passed down in the family for generations.", nouns=["table", "wooden table"]) )

complete = False
while not complete:
	print
	print room.getDescription()
	
	verb, noun = Parser.splitInput( raw_input("> ") )
	if verb == Parser.EXAMINE:
		print room.examine(noun)
		
	elif verb == Parser.PICK_UP:
		item = room.pickUp(noun)
		if item is not None:
			Player.addToInventory(item)
			print "You have put "+noun+" into your inventory"
		
	elif verb == Parser.INVENTORY:
		print Player.getInventory()
		
	else:
		print "I don't know how to do that"
	
