import csv
from constants import *

#Building variables.
b_abbr2full:dict
b_full2abbr:dict
b_abbr2postal:dict
b_postal2abbr:dict

def load_data_buil(dir=building_list_DIR) -> None:
	assert type(dir) == str
	'''
	This function read building data from local csv files,
		and create dictionary objects in global context.
			(1) b_abbr2full:dict
			(2) b_full2abbr:dict
			(3) b_abbr2postal:dict
			(4) b_postal2abbr:dict
		those dict take string as key and return a string object.
	'''
	print('==== Loading building data from local files ====')
	print('==== Reading local files ====')
	print('Data source: {0:s}'.format(dir))
	with open(dir, 'r') as csvfile:
		full_names = list()
		abbr = list()
		postal = list()

		reader = csv.reader(csvfile)
		for item in reader:
			full_names.append(item[0])
			abbr.append(item[1])

			p = item[3] # potential postal code.
			if len(p) == 8 and p[4] == ' ':
				# 'len(p) == 8...' There would a space before postal code
				# in the raw csv file.
				postal.append(item[3].strip()) # Read data is postal code.
			else:
				postal.append('FALSE') # Read data is not postal code.

		print('==== Checking data validity ====')

		assert len(full_names) == len(abbr) == len(postal)
		num_buil = len(abbr)

		print('==== Creating dictionary objects ====')
		global b_abbr2full, b_full2abbr, b_abbr2postal, b_postal2abbr
		b_abbr2full = dict((abbr[i], full_names[i]) for i in range(num_buil))
		b_full2abbr = dict((v, k) for k, v in b_abbr2full.items())

		b_abbr2postal = dict((abbr[i], postal[i]) for i in range(num_buil))
		b_postal2abbr = dict((v, k) for k, v in b_abbr2postal.items())

def get_b_info(buil:str, info_sele:str) -> str:
	'''

	:param buil: input building full name or abbrivation or postal code.
	:param info_sele:
		'a': return abbrivation as a string.
		'f': return full name as a string.
		'p': return postal code as a string.
	:return: a string.
	'''
	assert type(buil) == str and type(info_sele) == str
	# Analyzing input buil type.
	try:
		if len(buil) == 2 and [char.isupper() for char in buil] == [True] * len(buil):
			# Building input is Abbrivation
			if info_sele == 'a':
				output = buil
			elif info_sele == 'f':
				output = b_abbr2full[buil]
			elif info_sele == 'p':
				output = b_abbr2postal[buil]
		elif len(buil) == 7 and buil[3] == ' ':
			# Building input is Postal code
			if info_sele == 'a':
				output = b_postal2abbr[buil]
			elif info_sele == 'f': # Postal -> Full Name
				output = b_abbr2full[b_postal2abbr[buil]]
			elif info_sele == 'p':
				output = buil
		else:
			# Building input is Full name
			if info_sele == 'a':
				output = b_full2abbr[buil]
			elif info_sele == 'p': # Full Name -> Postal
				output = b_abbr2postal[b_full2abbr[buil]]
			elif info_sele == 'f':
				output = buil
	except KeyError:
		print('Given building information cannot be found in database.')
		output = False
	return output

load_data_buil()