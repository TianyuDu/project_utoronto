# Draft on Nov. 6, YYZ Terminal 1.

#Listing of Program/ Subject Areas
import selenium
from selenium.webdriver.common.by import By

URL = 'https://fas.calendar.utoronto.ca/listing-program-subject-areas'

web = selenium.webdriver.Chrome()
web.get(URL)

subjects = web.find_elements(By.TAG_NAME, 'td')
# Clean Data
for i in range(len(subjects)):
	text = subjects[i].get_property('innerText')

def generate_subject_areas(web, area_url_DIR:str) -> list:
	URL = 'https://fas.calendar.utoronto.ca/listing-program-subject-areas'
	web.get(URL)
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

a = generate_subject_areas(web, subject_area_url_DIR)

def generate_course_list(web, target_area_url_list: list, course_list_DIR: str) -> None:
	clean_course = list()
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

	with open(course_list_DIR, 'w') as csvfile:
		writer = csv.writer(csvfile)
		for item in clean_course:
			writer.writerow(item)

	print('Done.')









