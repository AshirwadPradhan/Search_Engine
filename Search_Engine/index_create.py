import os
import re

def get_filenames(file_list):
	'''
	get file names which contains the corpus
	'''
	files = []
	try:
		with open(file_list, mode = 'r') as f:
			files = f.readlines()
	except OSError:
		print('Files not available')

	for i,f in enumerate(files):
		files[i] = os.path.normpath('data'+'/'+ f[:-1])
	
	#print(files)
	return files


def raw_tokenize(filenames):
	"""
	removes punctuation and split into words and creates a dict
	which maps filenames to the list of tokens
	INPUT : list of file names
	OUTPUT : dict mapping of file to the list of words in the file
	"""
	dict_words = {}
	for file in filenames:
		with open(file, mode = 'r') as f:
			dict_words[file] = f.read().lower()

			#identify all the charcter's which are not 
			#a word character
			reg_obj = re.compile('[\W_]+')
			#replace all the non word charcters with a space
			dict_words[file] = reg_obj.sub(' ',dict_words[file])
			#print(dict_words)
			#re.sub('[\W_]+', ' ', dict_words[file])
			#print(dict_words)
			dict_words[file] = dict_words[file].split()
			#print(dict_words)
	return dict_words


def word_position_index(word_list):
	"""
	maps words to the position in the document
	INPUT : list of words
	OUTPUT : dict mapping of list of words to the position of 
			 occurences of that word
	"""
	word_index = {}
	#make a mapping from the word to the position in the word_list
	for i, word in enumerate(word_list):
		if word in word_index.keys():
			word_index[word].append(i)
		else:
			word_index[word] = [i]
	#print(word_index)
	return word_index


def create_all_index(dict_words):
	'''
	creates indicies of all the word in a file based on position
	using word_position_index() function
	INPUT : dict mapping of file names to the list of words in the 
			file
	OUTPUT : dict mapping of file names to the dict mapping of list 
			 of word based on occurences of that word  
	'''
	all_index = {}
	for f in dict_words.keys():
		all_index[f] = word_position_index(dict_words[f])
	#print(all_index)
	return all_index

def inverted_index(all_index):
	"""
	creates inverted index based on forward index of the document
	INPUT : forward index from create_all_index()
	OUTPUT: inverted index 
	"""
	inv_index = {}
	#fetching the file name
	for fname in all_index.keys():
		#fetching the word in the filename
		for w in all_index[fname].keys():
			if w in inv_index.keys():
				if fname in inv_index[w].keys():
					inv_index[w][fname].extend(all_index[fname][w][:])
				else:
					inv_index[w][fname] = all_index[fname][w]
			else:
				inv_index[w] = {fname:all_index[fname][w]}
	print(inv_index)
	return inv_index





if __name__ == '__main__':
	filenames = get_filenames('files_list.txt')
	dict_words = raw_tokenize(filenames)
	all_index = create_all_index(dict_words)
	inv_index = inverted_index(all_index)