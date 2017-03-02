import numpy as np
import string
from collections import Counter

translator = str.maketrans('', '', string.punctuation)


def generate_file_names():
	"""
	Generates the list of file names in the data folder.
	"""
	list_file_names = []
	for i in range(1, 10):
		list_file_names.append('data/00' + str(i) + ".txt")
	for i in range(10, 100):
		list_file_names.append('data/0' + str(i) + ".txt")
	list_file_names.append('data/100.txt')
	return list_file_names


def create_sets_dictionary(names):
	"""
	Returns a dictionary keyed by a file name. The associated value
	is the set of words in the file.
	"""
	set_dictionary = {}
	for fl_name in names:
		new_set = set()
		with open(fl_name,'r') as f:
			for line in f:
				for word in line.split():
					word = word.lower()
					new_word = word.translate(translator)
					if new_word:
						new_set.add(new_word)
			set_dictionary[fl_name] = new_set
	return set_dictionary

def create_np_matrix():
	"""
	Returns 100x100 matrix of zeros.
	"""
	return np.zeros((100, 100))

def fill_matrix(matrix, names, dictionary):
	"""
	Fills and returns matrix with intersection of two files' word sets.
	"""
	sorted_names = sorted(names)
	len_names = len(sorted_names)
	for i in range(len_names):
		for j in range(len_names):
			set_i = dictionary[names[i]]
			set_j = dictionary[names[j]]
			matrix[i,j] = len(set_i.intersection(set_j))
	return matrix

def create_mono_frequency_dictionary(names):
	"""
	Returns 50 most common words sorted by highest frequencies.
	"""
	total_list = []
	for fl_name in names:
		with open(fl_name,'r') as f:
			for line in f:
				for word in line.split():
					word = word.lower()
					new_word = word.translate(translator)
					if new_word:
						total_list.append(new_word)
	ctr = Counter(total_list)
	most_common_50 = ctr.most_common(50)
	return [word for word, number in most_common_50]


def create_duo_frequency_dictionary(names):
	"""
	Returns 50 most common bigrams sorted by highest frequencies.
	"""
	duo_list = []
	for fl_name in names:
		short_list = []
		with open(fl_name,'r') as f:
			for line in f:
				for word in line.split():
					word = word.lower()
					new_word = word.translate(translator)
					if new_word:
						short_list.append(new_word)
		for i in range(1, len(short_list)):
			duo_list.append((short_list[i - 1], short_list[i]))
	ctr = Counter(duo_list)
	most_common_duo_50 = ctr.most_common(50)
	return [str(duo) for duo, number in most_common_duo_50]


def main_1():
	file_names = generate_file_names()
	sets_dictionary = create_sets_dictionary(file_names)
	matrix = create_np_matrix()
	filled_matrix = fill_matrix(matrix, file_names, sets_dictionary)
	np.savetxt("intersections.csv", filled_matrix, delimiter=",", fmt='%10.0f')

def main_2():
	file_names = generate_file_names()
	mono_50 = create_mono_frequency_dictionary(file_names)
	duo_50 = create_duo_frequency_dictionary(file_names)
	f = open('frequencies.txt', 'w')
	for line in mono_50:
		f.write(line + '\n')
	for line in duo_50:
		f.write(line + '\n')
	f.close()

main_1()
main_2()