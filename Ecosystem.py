# Jack Hall-Tipping
# CSCI - 204 - Dancy
# P1-2

from random import *
import re

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
			self.newInputFile = self.inputFile.readlines()
		except ValueError:
			print('Please enter a valid text filename')

	def add_file_to_river_list(self):
		'''Adds the appropriate animal objects to the riverList depending on
		the input file'''
		for animal in self.newInputFile:
			if animal[0] == 'B':
				self.riverList.append(Bear(animal[2], int(re.search(r'\d+', animal).group())))
				print(self.riverList[0].strength)
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
				if animal.gender == 'M':
					gender = 'Male'
				else:
					gender = 'Female'
				outputList.append('Fish ' + (gender) + ' ' + str(animal.strength) + '\n')
			elif isinstance(animal, Bear):
				if animal.gender == 'M':
					gender = 'Male'
				else:
					gender = 'Female'
				outputList.append('Bear ' + (gender) + ' ' + str(animal.strength) + '\n')
			else:
				outputList.append('None' + '\n')
		return outputList

	def step(self):
		''' Moves the whole river one step forward in time.
		also prints the state of the river
		to an output file at the end of the each step
		'''
		riverListCopy = self.riverList[:]
		self.riverList = riverListCopy[:]
		output = self.write_to_output_file()
		outputString = ''.join(output)
		self.outputFile.write(outputString + '\n')

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
		self.gender = gender
		self.strength = strength

class Bear(Animal):

	def __init__(self, gender, strength):
		super(Bear, self).__init__(gender, strength)

	def get_image(self):
		return "bear.ppm"

class Fish(Animal):

	def __init__(self, gender, strength):
		super(Fish, self).__init__(gender, strength)

	def get_image(self):
		return "salmon.ppm"
