# Jack Hall-Tipping
# CSCI - 204 - Dancy
# P1-1

from random import *

class Ecosystem:

	def __init__(self, filename):
		self.open_file(filename)
		self.riverList =[]
		self.add_file_to_river_list()
		self.inputFile.close()
		self.outputFile = open('output.txt', 'w' )
		self.newOutputFile = self.outputFile

	def open_file(self, filename):
		'''opens the file'''
		if '.txt' not in filename:
			raise ValueError('Please enter a valid text filename')
		try:
			self.inputFile = open(filename, 'r')
			self.newInputFile = self.inputFile.readline()
		except ValueError:
			print('Please enter a valid text filename')

	def add_file_to_river_list(self):
		'''Adds the appropriate animal objects to the riverList depending on
		the input file'''
		try:
			for animal in self.newInputFile:
				if animal == 'F':
					self.riverList.append(Fish())
				elif animal == 'B':
					self.riverList.append(Bear())
				elif animal == 'N':
					self.riverList.append(None)
		except ValueError:
			print('Text file does not have only B F or N as a string')

	def write_to_output_file(self):
		'''For each bear, fish and none instance it writes the appropriate
		string letter, i.e. F B N to an output file'''
		outputList = []
		for animal in self.riverList:
			if isinstance(animal, Fish):
				outputList.append('F')
			elif isinstance(animal, Bear):
				outputList.append('B')
			else:
				outputList.append('N')
		return outputList

	def step(self):
		''' Moves the whole river one step forward in time.
		also prints the state of the river
		to an output file at the end of the each step
		'''
		riverListCopy = self.riverList[:]
		self.fish_collision(riverListCopy)
		self.bear_collision(riverListCopy)
		self.bear_eat_fish(riverListCopy)
		self.fish_scared_of_bear(riverListCopy)
		lastAnimal = riverListCopy.pop()
		riverListCopy.insert(0, lastAnimal)
		self.riverList = riverListCopy[:]
		output = self.write_to_output_file()
		outputString = ''.join(output)
		self.outputFile.write(outputString + '\n')

	def fish_scared_of_bear(self, riverListCopy):
		'''updates riverlist if a fish is scared of a bear'''
		if len(self.check_fish_scared_of_bear(riverListCopy)) != 0:
			scaredFishPositions = self.check_fish_scared_of_bear(riverListCopy)
			for position in scaredFishPositions:
				spot = riverListCopy[position]
				newSpot = riverListCopy[position-1]
				riverListCopy[position-1] = spot
				riverListCopy[position] = newSpot
		return riverListCopy

	def bear_eat_fish(self, riverListCopy):
		'''updates riverlist if a bear eats a fish'''
		if len(self.check_bear_eat_fish(riverListCopy)) != 0:
			fishToDiePositions = self.check_bear_eat_fish(riverListCopy)
			for position in fishToDiePositions:
				riverListCopy.pop(position)
				riverListCopy.insert(position, None)
		return riverListCopy

	def bear_collision(self, riverListCopy):
		'''updates riverlist if a collision of two bears'''
		if len(self.check_bear_collide(riverListCopy)) != 0:
			leftBearPositions = self.check_bear_collide(riverListCopy)
			for position in leftBearPositions:
				bear = riverListCopy[position]
				newSpot = riverListCopy[position-1]
				riverListCopy[position-1] = bear
				riverListCopy[position] = newSpot
		return riverListCopy

	def fish_collision(self, riverListCopy):
		'''updates riverlist if a collision of two fish'''
		if self.check_fish_collide(riverListCopy) != 0:
			numBabies = self.check_fish_collide(riverListCopy)
			newPosition = self.new_fish_position(riverListCopy, numBabies)
			for fish in newPosition:
				riverListCopy.pop(fish)
				riverListCopy.insert(fish, Fish())
		return riverListCopy

	def new_fish_position(self, riverListCopy, numBabies):
		'''Chooses the position for the new fish'''
		emptySpaces = []
		newPosition = []
		for animal in riverListCopy:
			if animal == None:
				emptySpaces.append(riverListCopy.index(animal))
		while numBabies > 0:
			spot = choice(emptySpaces)
			emptySpaces.pop(emptySpaces.index(spot))
			newPosition.append(spot)
			numBabies -= 1
		return newPosition

	def check_fish_collide(self, riverListCopy):
		'''Returns the number of fish collisions'''
		numBabies = 0
		for animal in riverListCopy:
			if None in riverListCopy and isinstance(animal, Fish) and isinstance(riverListCopy[(riverListCopy.index(animal) + 1) % len(riverListCopy)], Fish):
				numBabies += 1
		return numBabies

	def check_bear_collide(self, riverListCopy):
		'''returns the indexes of the bear collisions'''
		leftBearPositions = []
		for animal in riverListCopy:
			if isinstance(animal, Bear) and isinstance(riverListCopy[(riverListCopy.index(animal) + 1) % len(riverListCopy)], Bear):
				leftBearPositions.append(riverListCopy.index(animal))
		return leftBearPositions

	def check_bear_eat_fish(self, riverListCopy):
		'''checks if a bear will collide with a fish'''
		fishToDiePositions = []
		for animal in riverListCopy:
			if isinstance(animal, Bear) and isinstance(riverListCopy[(riverListCopy.index(animal) + 1) % len(riverListCopy)], Fish):
				if riverListCopy.index(animal) != len(riverListCopy) - 1:
					fishToDiePositions.append(riverListCopy.index(riverListCopy[riverListCopy.index(animal)+1]))
				else:
					fishToDiePositions.append(0)
		return fishToDiePositions

	def check_fish_scared_of_bear(self, riverListCopy):
		'''checks if a fish will collide with a bear'''
		scaredFishPositions = []
		for animal in riverListCopy:
			if isinstance(animal, Fish) and isinstance(riverListCopy[(riverListCopy.index(animal) + 1) % len(riverListCopy)], Bear):
				scaredFishPositions.append(riverListCopy.index(animal))
		return scaredFishPositions

	def get_size(self):
		''' Returns the size of the river '''
		return(len(self.riverList))

	def get_inhabitant(self, index):
		''' Returns the item at this index of the river.
		It should either be a Bear, Fish, or None
		'''
		return(self.riverList[index])

	def quit(self):
		'''Called when program quits. Close your output file.'''
		self.outputFile.close()

class Animal:

	def __init__(self):
		pass

class Bear(Animal):

	def get_image(self):
		return "bear.ppm"

class Fish(Animal):

	def get_image(self):
		return "salmon.ppm"
