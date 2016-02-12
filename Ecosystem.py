# Jack Hall-Tipping
# CSCI - 204 - Dancy
# P1-2

from random import *
import re
from collections import deque

class Ecosystem:

	def __init__(self, filename):
		self.open_file(filename)
		self.riverList = []
		self.input_file_to_river_list()
		self.inputFile.close()
		self.outputFile = open('output.txt', 'w' )
		self.newOutputFile = self.outputFile

	def open_file(self, filename):
		'''opens the file'''
		if '.txt' not in filename:
			raise ValueError('Please enter a valid text filename')
		try:
			self.inputFile = open(filename, 'r')
			self.newInputFile = self.inputFile.readlines()
		except ValueError:
			print('Please enter a valid text filename')

	def input_file_to_river_list(self):
		'''Adds the appropriate animal objects to the riverList depending on
		the input file'''
		for animal in self.newInputFile:
			if animal[0] == 'B':
				self.riverList.append(Bear(animal[2], int(re.search(r'\d+', animal).group())))
			elif animal[0] == 'F':
				self.riverList.append(Fish(animal[2], int(re.search(r'\d+', animal).group())))
			else:
				self.riverList.append(None)

	def write_to_output_file(self):
		'''For each bear, fish and none instance it writes the appropriate
		string letter, i.e. F B N to an output file'''
		outputList = []
		for animal in self.riverList:
			if isinstance(animal, Fish):
				if animal.get_gender() == 'M':
					gender = 'Male'
				else:
					gender = 'Female'
				outputList.append('Fish ' + (gender) + ' ' + str(animal.get_strength()) + '\n')
			elif isinstance(animal, Bear):
				if animal.get_gender() == 'M':
					gender = 'Male'
				else:
					gender = 'Female'
				outputList.append('Bear ' + (gender) + ' ' + str(animal.get_strength()) + '\n')
			else:
				outputList.append('None' + '\n')
		return outputList

	def step(self):
		''' Moves the whole river one step forward in time.
		also prints the state of the river
		to an output file at the end of the each step
		'''
		riverListCopy = self.riverList[:]
		for animal in riverListCopy:
			if self.check_collision(riverListCopy, animal):
				self.collision_type(riverListCopy, animal)
		riverListCopy = deque(riverListCopy[:])
		riverListCopy.rotate(1)
		riverListCopy = list(riverListCopy)
		self.riverList = riverListCopy[:]
		output = self.write_to_output_file()
		outputString = ''.join(output)
		self.outputFile.write(outputString + '\n')

	def check_collision(self, riverListCopy, animal):
		'''returns True or False if there is or isnt a collision between
		animals'''
		if animal is None:
			return False
		elif riverListCopy.index(animal) + 1 == len(riverListCopy):
			if riverListCopy[0] is None:
				return False
			else:
				return True
		else:
			if riverListCopy[riverListCopy.index(animal) + 1] is None:
				return False
			else:
				return True

	def collision_type(self, riverListCopy, animal):
		'''checks the type of collision and calls the appropriate function'''
		if riverListCopy.index(animal) + 1 == len(riverListCopy):
			if animal.__class__.__name__ == 'Bear' and riverListCopy[0].__class__.__name__ == 'Fish':
				self.eat(riverListCopy, animal)
			elif animal.__class__.__name__ == riverListCopy[0].__class__.__name__:
				if animal.get_gender() == riverListCopy[0].get_gender():
					self.fight(riverListCopy, animal)
				else:
					self.mate(riverListCopy, animal)
		else:
			if animal.__class__.__name__ == 'Bear' and riverListCopy[riverListCopy.index(animal) + 1].__class__.__name__ == 'Fish':
				self.eat(riverListCopy, animal)
			elif animal.__class__.__name__ == riverListCopy[riverListCopy.index(animal) + 1].__class__.__name__:
				if animal.get_gender() == riverListCopy[riverListCopy.index(animal) + 1].get_gender():
					self.fight(riverListCopy, animal)
				else:
					self.mate(riverListCopy, animal)

	def mate(self, riverListCopy, animal):
		'''if two animals of the same species but different genders collide
		it randomly spawns a new animal of the same species. this new animal
		takes the gender of the stronger parent, and the strength of this
		new animal is the average of its parents'''
		newStrength = 0
		newGender = 0
		newAnimal = animal.__class__.__name__
		if riverListCopy.index(animal) + 1 == len(riverListCopy):
			newStrength = (animal.get_strength() + riverListCopy[0].get_strength()) / 2
			if animal.get_strength() > riverListCopy[0].get_strength():
				newGender = animal.get_gender()
			else:
				newGender = riverListCopy[0].get_gender()
		else:
			newStrength = (animal.get_strength() + riverListCopy[riverListCopy.index(animal) + 1].get_strength()) / 2
			if animal.get_strength() > riverListCopy[riverListCopy.index(animal) + 1].get_strength():
				newGender = animal.get_gender()
			else:
				newGender = riverListCopy[riverListCopy.index(animal) + 1].get_gender()
		emptySpace = randrange(0,len(riverListCopy))
		while riverListCopy[emptySpace] != None:
			emptySpace = randrange(0,len(riverListCopy))
		riverListCopy.pop(emptySpace)
		if newAnimal == 'Fish':
			riverListCopy.insert(emptySpace, Fish(newGender, newStrength))
		elif newAnimal == 'Bear':
			riverListCopy.insert(emptySpace, Bear(newGender, newStrength))

	def eat(self, riverListCopy, animal):
		'''if a bear collides with a fish the bear eats the fish
		and gets the strength of the fish'''
		if riverListCopy.index(animal) + 1 == len(riverListCopy):
			newStrength = animal.get_strength() + riverListCopy[0].get_strength()
			animal.set_strength(newStrength)
			riverListCopy.pop(0)
			riverListCopy.insert(0, None)
		else:
			newStrength = animal.get_strength() + riverListCopy[riverListCopy.index(animal) + 1].get_strength()
			animal.set_strength(newStrength)
			newSpace = riverListCopy.index(animal) + 1
			riverListCopy.pop(riverListCopy.index(animal) + 1)
			riverListCopy.insert(newSpace, None)

	def fight(self, riverListCopy, animal):
		'''if two animals of the same species and gender collide, the
		animals fight and the animal with more strength wins and the other
		dies. the animal that survives loses the amount of strength
		equal to the one that died'''
		if riverListCopy.index(animal) + 1 == len(riverListCopy):
			if animal.get_strength() > riverListCopy[0].get_strength():
				newStrength = animal.get_strength() - riverListCopy[0].get_strength()
				animal.set_strength(newStrength)
				riverListCopy.pop(0)
				riverListCopy.insert(0, None)
			else:
				newStrength = riverListCopy[0].get_strength() - animal.get_strength()
				riverListCopy[0].set_strength(newStrength)
				newSpace = riverListCopy.index(animal)
				riverListCopy.pop(riverListCopy.index(animal))
				riverListCopy.insert(newSpace, None)
		else:
			if animal.get_strength() > riverListCopy[riverListCopy.index(animal) + 1].get_strength():
				newStrength = animal.get_strength() - riverListCopy[riverListCopy.index(animal) + 1].get_strength()
				animal.set_strength(newStrength)
				newSpace = riverListCopy.index(animal) + 1
				riverListCopy.pop(riverListCopy.index(animal) + 1)
				riverListCopy.insert(newSpace, None)
			else:
				newStrength = riverListCopy[riverListCopy.index(animal) + 1].get_strength() - animal.get_strength()
				riverListCopy[riverListCopy.index(animal) + 1].set_strength(newStrength)
				newSpace = riverListCopy.index(animal)
				riverListCopy.pop(riverListCopy.index(animal))
				riverListCopy.insert(newSpace, None)

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

class Animal(object):

	def __init__(self, gender, strength):
		self._gender = gender
		self._strength = strength

	def get_gender(self):
		'''returns the gender of an animal'''
		return(self._gender)

	def get_strength(self):
		'''returns the strength of an animal'''
		return(self._strength)

	def set_gender(self, gender):
		'''sets the gender of an animal'''
		self._gender = gender

	def set_strength(self, strength):
		'''sets the strength of an animal'''
		self._strength = strength

class Bear(Animal):

	def __init__(self, gender, strength):
		super(Bear, self).__init__(gender, strength)

	def get_gender(self):
		return super(Bear, self).get_gender()

	def get_strength(self):
		return super(Bear, self).get_strength()

	def get_image(self):
		return "bear.ppm"

	def set_gender(self, gender):
		super(Bear, self).set_gender(gender)

	def set_strength(self, strength):
		super(Bear, self).set_strength(strength)

class Fish(Animal):

	def __init__(self, gender, strength):
		super(Fish, self).__init__(gender, strength)

	def get_gender(self):
		return super(Fish, self).get_gender()

	def get_strength(self):
		return super(Fish, self).get_strength()

	def get_image(self):
		return "salmon.ppm"

	def set_gender(self, gender):
		super(Fish, self).set_gender(gender)

	def set_strength(self, strength):
		super(Fish, self).set_strength(strength)
