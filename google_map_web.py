from constants import *
from main import
import main


def parallel_walk_info(range_begin:int, range_end:int, source:list, Nthread=4) -> List[list]:
	assert type(Nthread) == int
	assert type(range_begin) == int
	assert type(range_end) == int

	name_list_full = list(abbr2full.keys())
	name_list_full.sort()
	name_list_abbr = list(abbr2full.values())
	name_list_abbr.sort()

	threadBreak = list(np.linspace(0, len(main.abbr2full) + 1, Nthread+1).astype(int))

	# Task allocation
	task = list()
	for i in range(Nthread):
		# threadID = i
		task.append((threadBreak[i], threadBreak[i + 1], i, source))

	with multiprocessing.Pool(Nthread) as parpool:
		thread_result = parpool.starmap(thread_walk_info, task)

	# Collect results
	output_result = list()
	for result_each_worker in thread_result: # Result from each parallel worker.
		output_result.append(list(br for br in result_each_worker)) # br stands for building result.

	with open(distance_DIR, 'w') as file:
		writer = csv.writer(file)
		for row_info in output_result:
			writer.writerow(row_info)

	return output_result # Result format: List[list]

def thread_walk_info(range_begin:int, range_end:int, source, threadID=0) -> List[list]:
	# This function is used for parallel multi-processing methods, so it won't write anything to any external file.
	# This function should be used by each worker in parallel taksing.

	assert type(range_begin) == int
	assert type(range_end) == int
	assert type(threadID) == int

	[abbr2full, full2abbr, abbr2postal, postal2abbr] = source

	gathered_info_per_start = list()
	gathered_info = list()

	# Initializing driver.
	driver = webdriver.Chrome()
	driver.get(google_map_URL)

	boxes = driver.find_elements_by_class_name('tactile-searchbox-input')
	box_start = boxes[0]
	box_dest = boxes[1]
	# Finished.

	name_list_abbr = list(abbr2full.keys())
	name_list_abbr.sort()

	for start in name_list_abbr[range_begin: range_end]:
		start_full = abbr2full[start]
		start_postal = abbr2postal[start]
		sp_exist = bool(len(start_postal) == 7)

		for dest in name_list_abbr[:30]:
			dest_full = abbr2full[dest]
			dest_postal = abbr2postal[dest]
			dp_exist = bool(len(dest_postal) == 7)

			result = get_travel_info_light(driver, box_start, box_dest, start_full, dest_full)
			if result == False:
				print('Failed to fetch information with full name search, now trying to fetch with postal code.')
				if sp_exist and dp_exist:
					result = get_travel_info_light(driver, box_start, box_dest, start_postal, dest_postal)
				elif sp_exist and not dp_exist:
					result = get_travel_info_light(driver, box_start, box_dest, start_postal, dest_full)
				elif dp_exist and not sp_exist:
					result = get_travel_info_light(driver, box_start, box_dest, start_full, dest_postal)
				else:
					print('Impossible to fetch with postal code. Travel information is left as False/Blank.')
			print('========Thread: {0:d}========'.format(int(threadID)))
			print('Trip from {start:s} to {dest:s}'.format(start=start, dest=dest))
			print(result)
			gathered_info_per_start.append(result)
		gathered_info.append(gathered_info_per_start)

	print('Finished.')
	driver.close()
	return gathered_info