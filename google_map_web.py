import numpy as np
import warnings
import multiprocessing
import data
import os
import csv
import time
import main
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from constants import *
from typing import List



def parallel_walk_info(start_buil:List[str], dest_buil:List[str], nthread=4) -> List[list]:
	'''
	[!] We represent building with 0-based integers by the position of building in our whole buidling list.
	:param start_buil:
		A list containing abbreviations of all buildings as starting building.
	:param dest_buil:
		A list containing abbreviations of all buildings as destination building.
	:param nthread:
		number of threads to deploy.
		By default, 4 threads (4 Independent Chrome will be run) will be initialized,
		Set nthread to 1, searching will be run in single thread model.
	:return:

	'''
	assert type(nthread) == int and nthread >= 1
	start_buil.sort()
	dest_buil.sort()
	num_start = len(start_buil)
	num_dest = len(dest_buil)

	threadBreak = list(np.linspace(0, num_start + 1, nthread+1).astype(int)) # We allocate tasks by dividing starting buildings into clusters.
	# e.g. for 100 items in start buildings and thread is 4.
	#threadBreak = [0, 25, 50, 75, 100]
	#(threadBreak[i], threadBreak[i + 1]) would be the range of tasks for worker i.


	# Task allocation
	task = list()
	for i in range(nthread):
		# threadID = i
		task.append([start_buil[threadBreak[i]:threadBreak[i+1]], dest_buil, i])
		#(arg0) List containing all abbreviations of buildings as the start building for this worker.
		#(arg1) List containing all abbreviations of buildings as the end building for this worker.
		#(arg2) Thread ID.

	with multiprocessing.Pool(nthread) as parpool: # Initializing pool.
		thread_result = parpool.map(thread_walk_info, task)

	# Collect results
	output_result = list()
	for result_each_worker in thread_result: # Result from each parallel worker.
		output_result.append(list(br for br in result_each_worker)) # br stands for building result.

	with open(distance_DIR, 'w') as file:
		writer = csv.writer(file)
		writer.writerow([' '].extend(dest_buil))
		for row_info in output_result:
			writer.writerow(row_info)

	return output_result # Result format: List[list]

def thread_walk_info(input_bundle) -> List[list]:
	# start_buil:List[str], dest_buil:List[str], threadID:int
	# This function is used for parallel multi-processing methods, so it won't write anything to any external file.
	# This function should be used by each worker in parallel tasking.
	start_buil = input_bundle[0]
	dest_buil = input_bundle[1]
	threadID = input_bundle[2]

	print('Thread{0:d}: To find: '.format(threadID))
	print(start_buil)
	print(dest_buil)

	gathered_info_per_start = list()
	gathered_info = list()

	# Initializing driver.
	driver = webdriver.Chrome()
	driver.get(google_map_URL)

	'''
	boxes = driver.find_elements_by_class_name('tactile-searchbox-input')
	box_start = boxes[0]
	box_dest = boxes[1]'''
	# Finished.

	for start_a in start_buil:
		start_f = data.get_b_info(start_a, 'f')
		start_f_clean = start_f.replace(' ','+')
		start_p = data.get_b_info(start_a, 'p') # This would be 'FALSE' if there's no postal code for this location, like 'Back Campus Fields'.
		start_p_DNE = bool(start_p == 'FALSE')
		gathered_info_per_start.append(start_a)

		for dest_a in dest_buil:
			dest_f = data.get_b_info(dest_a, 'f')
			dest_f_clean = dest_f.replace(' ','+')
			dest_p = data.get_b_info(dest_a, 'p')
			dest_p_DNE = bool(dest_p == 'FALSE')

			maxtry = 5 # Maximum of trails.

			result = get_travel_info_light(driver, start_f_clean, dest_f_clean, maxtry=maxtry)

			if result == False:
				print('Buildings {0:s} to {1:s}: Failed to fetch information with full name search, now trying to fetch with postal code.'.format(start_a, dest_a))
				if (not start_p_DNE) and (not dest_p_DNE):
					result = get_travel_info_light(driver, start_p, dest_p, maxtry=maxtry)
				elif start_p_DNE and (not dest_p_DNE):
					result = get_travel_info_light(driver, start_f_clean, dest_p, maxtry=maxtry)
				elif (not start_p_DNE) and dest_p_DNE:
					result = get_travel_info_light(driver, start_p, dest_f_clean, maxtry=maxtry)
				else:
					warnings.warn('Impossible to fetch with postal code. Travel information is left as False/Blank.')
					result = False

			if result != False:
				result = result.replace('\n', ' ')
			else:
				result = 'FALSE'
			print('========Thread: {0:d}========'.format(int(threadID)))
			print('Trip from {start:s} to {dest:s}'.format(start=start_a, dest=dest_a))
			print(result)
			gathered_info_per_start.append(result)
		gathered_info.append(gathered_info_per_start)

	print('Thread{0:d}: Finished.'.format(threadID))
	driver.close()
	return gathered_info

def get_travel_info_light(driver, start: str, dest: str, maxtry=5) -> object:
	'''
	This function is called by individual worker in parallel pool.
	:param driver:
		Web driver created by this worker.
	:param box_start:
		Box of input of start building located on web page.
	:param box_dest:
		Box of input of destination building located on web page.
	:param start:
		Start building identification. Could be full name or postal code.
	:param dest:
		Destination building identification. Could be full name or postal code.
	:param maxtry:
		Max number of retry before return False value.


	:return:
		If information is found, return the string containing travelling information.
		e.g.:
		'13 min\n1.0 km\nvia St George St\nThis route has restricted usage or private roads.\nMostly flat\nDETAILS'
	'''
	if start ==dest:
		return 'Same'

	target_url = google_map_URL + 'dir/' + start + '/' + dest + '/'
	print(target_url)
	driver.get(target_url)

	time.sleep(1)
	tryN = 0
	
	fail_flag = True
	retry_latency = .5  # in second.

	while tryN <= maxtry and fail_flag:
		try:
			list_of_plans = driver.find_element_by_class_name('section-listbox')
			obj_found = list_of_plans.find_element_by_class_name('section-directions-trip-description')
			info_found = obj_found.find_element_by_class_name('section-directions-trip-numbers')
			fail_flag = False # Success
		except:
			print('Driver failed to locate travel information item on page, will retry in {0:f} second. Try = {1:f}'.format(retry_latency, tryN))
			tryN += 1
			time.sleep(retry_latency)
	try:
		return info_found.text
	except NameError:
		warnings.warn('Failed to locate building, False is returned.')
		return False