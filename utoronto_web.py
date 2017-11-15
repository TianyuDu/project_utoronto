import numpy as np
import multiprocessing

def generate_subject_areas(web, target_URL:str, area_url_DIR:str) -> list:
	web.get(target_URL)
	result_list = list() # List of lists, [name, url]
	potential = web.find_elements(By.TAG_NAME, 'a')
	for potential_item in potential:
		text = potential_item.get_property('innerText')
		if re.search(r'\n', text) == None:
			dest_url = potential_item.get_attribute('href')
			if text != '' and dest_url != None:
				result_list.append([text, dest_url])
				print([text, dest_url])

	with open(area_url_DIR, 'w') as csvfile:
		writer = csv.writer(csvfile)
		for item in result_list:
			writer.writerow(item)
	return result_list

def generate_course_list(web, target_area_url_list: list, course_list_DIR: str, parallel=True, Nthread=4) -> None:
	clean_course = list()
	if parallel:
		print('Parallel Chrome Webdrivers are initializing...')
		# task allocation.
		threadBreak = list(np.linspace(0, len(target_area_url_list) + 1, Nthread+1).astype(int))
		task = list()
		for i in range(Nthread):
			task.append(\
				(threadBreak[i], threadBreak[i + 1], target_area_url_list)\
				)
		with multiprocessing.Pool(Nthread) as parpool:
			threadResult = parpool.starmap(work_task_function, task)

	elif not parallel:
		for area in target_area_url_list:
			area_name = area[0]
			area_url = area[1]

			web.get(area_url)
			courses = web.find_elements(By.TAG_NAME, 'h3')

			clean_course_partial = list() # Format: [Code, Name]

			for course in courses:
				text = course.get_property('innerText')
				try:
					re_result = re.search(r'...[1234]\d{2}[HFY].', text)
					code = re_result.group()
					name = text[re_result.end() + 3:]
					clean_course_partial.append([code, text])
				except AttributeError:
					print('Attribute Error Caught.')
			clean_course.extend(clean_course_partial)
	else:
		raise Warning('Invalid parallel option provided, should be a bool variable.')

	# Write to CSV file.
	with open(course_list_DIR, 'w') as csvfile:
		writer = csv.writer(csvfile)
		for item in clean_course:
			writer.writerow(item)

	print('Done.')

def work_task_function(begin:int, end:int, target_area_url_list:list) -> list:

	web = webdriver.Chrome()
	worker_target = target_area_url_list[begin:end]
	thread_clean_course

	for area in worker_target:
		area_name = area[0]
		area_url = area[1]
		web.get(area_url)
		courses = web.find_elements(By.TAG_NAME, 'h3')

		clean_course_thread = list()

		for course in courses:
			text = course.get_property('innerText')
			try:
				re_result = re.search(r'...[1234]\d{2}[HFY].', text)
				code = re_result.group()
				name = text[re_result.end() + 3:]
				clean_course_partial.append([code, text])
			except AttributeError:
				print('Attribute Error Caught.')

			clean_course_thread.extend(clean_course_partial)

	return clean_course_thread










