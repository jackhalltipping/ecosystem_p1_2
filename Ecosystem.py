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
		pass

	def write_to_output_file(self):
		'''For each bear, fish and none instance it writes the appropriate
		string letter, i.e. F B N to an output file'''
		pass

	def step(self):
		''' Moves the whole river one step forward in time.
		also prints the state of the river
		to an output file at the end of the each step
		'''
		pass

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

	def __init__(self, gender, strength):
		self.gender = gender
		self.strength = strength

	def get_image(self):
		return "bear.ppm"

class Fish(Animal):

	def __init__(self, gender, strength):
		self.gender = gender
		self.strength = strength

	def get_image(self):
		return "salmon.ppm"
