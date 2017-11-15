import selenium
import time
import datetime
import numpy as np
import csv
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import multiprocessing
from typing import List

from constants import *
from main import *
from utoronto_web import *
from google_map_web import *

def generate_building_list(building_list_DIR: str) -> None:
	driver = webdriver.Chrome()
	driver.get(ut_building_list_URL)

	buildingList = driver.find_element_by_class_name('buildinglist')

	with open(building_list_DIR, 'w') as file:
		writer = csv.writer(file)

		buildingInfo = buildingList.find_elements_by_css_selector('dl')

		for buil in buildingInfo:
			clean_info = buil.text.replace('\n', ',').replace(' | ', ',') + '\n'
			print(clean_info)
			file.write(clean_info)

	driver.close()

def generate_abbr2full(file_dir: str) -> dict:
	with open(file_dir, 'r') as csvfile:
		full_names = list()
		abbrs = list()

		reader = csv.reader(csvfile)
		for row in reader:
			full_names.append(row[0])
			abbrs.append(row[1])

		assert len(full_names) == len(abbrs)

		result = dict((abbrs[i], full_names[i]) for i in range(len(full_names)))

		return result

def generate_abbr2postal(file_dir: str) -> dict:
	with open(file_dir, 'r') as csvfile:
		abbrs = list()
		postal = list()

		reader = csv.reader(csvfile)
		for row in reader:
			abbrs.append(row[1])
			postal.append(row[3].strip())

		assert len(abbrs) == len(postal)

		result = dict((abbrs[i], postal[i]) for i in range(len(abbrs)))

		return result