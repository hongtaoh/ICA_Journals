"""get ICA publication paper info, specifically, I got all paper dois, title, and abstracts """

import pandas as pd
import numpy as np
import time 
import random
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.support.ui import Select
import sys

AUTHORS_TO_STUDY = sys.argv[1]
GSCHOLAR_DATA = sys.argv[2]

def get_vars(df):
	'''df here is AUTHORS_TO_STUDY
	'''
	# get only the first author dataset
	dff = df[df.authorPosition == 1]
	# original paper title 
	titles = dff.title.tolist()
	dois = dff.doi.tolist()
	years = dff.year.tolist()
	# query strings
	query = dff.title + ', ' + dff.journal + ', ' + dff.authorFullName
	papers = query.tolist()
	return titles, dois, years, papers 

def update_gscholar_dict_list(paper, titles, dois, years, idx):
	orig_title = titles[idx]
	doi = dois[idx]
	year = years[idx]
	query_string = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C50&q='
	driver.get(query_string + paper + '&btnG=')
	gs_paper_e = wait.until(EC.presence_of_element_located((
			By.CSS_SELECTOR, 'h3.gs_rt')))
	gs_paper_title = gs_paper_e.text
	gs_citation_e = wait.until(
		EC.presence_of_element_located((By.XPATH, '//div[@class="gs_fl"]//child::a[3]'
	)))
	citation_link = gs_citation_e.get_attribute('href')
	citation_count_string = gs_citation_e.get_attribute('innerHTML')
	if 'Cited by' in citation_count_string:
		gs_citation_count = int(re.findall(r'\d+', citation_count_string)[0])
	else:
		gs_citation_count = 0
	# if citation_count_string == "Related articles":
	#     gs_citation_count = 0
	# elif 'versions' in citation_count_string:
	# 	gs_citation_count = 0
	# else:
	#     gs_citation_count = int(re.findall(r'\d+', citation_count_string)[0])
	gscholar_dict = {
		'Original Title': orig_title,
		'Title on Google Scholar': gs_paper_title,
		'DOI': doi,
		'Year': year,
		'Citation Link': citation_link,
		'Citation Counts on Google Scholar': gs_citation_count,
	}
	gscholar_dict_list.append(gscholar_dict)
	print(f'paper {idx + 1} is done!')

def update_gscholar_dict_list_random(paper, titles, dois, years, idx, cur_idx):
	'''this is for random 
	'''
	orig_title = titles[idx]
	doi = dois[idx]
	year = years[idx]
	query_string = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%2C50&q='
	driver.get(query_string + paper + '&btnG=')
	gs_paper_e = wait.until(EC.presence_of_element_located((
			By.CSS_SELECTOR, 'h3.gs_rt')))
	gs_paper_title = gs_paper_e.text
	gs_citation_e = wait.until(
		EC.presence_of_element_located((By.XPATH, '//div[@class="gs_fl"]//child::a[3]'
	)))
	citation_link = gs_citation_e.get_attribute('href')
	citation_count_string = gs_citation_e.get_attribute('innerHTML')
	if 'Cited by' in citation_count_string:
		gs_citation_count = int(re.findall(r'\d+', citation_count_string)[0])
	else:
		gs_citation_count = 0
	gscholar_dict = {
		'Original Title': orig_title,
		'Title on Google Scholar': gs_paper_title,
		'DOI': doi,
		'Year': year,
		'Citation Link': citation_link,
		'Citation Counts on Google Scholar': gs_citation_count,
	}
	gscholar_dict_list.append(gscholar_dict)
	print(f'paper {cur_idx + 1} is done!')

if __name__ == '__main__':
	AUTHORS_TO_STUDY = pd.read_csv(AUTHORS_TO_STUDY)
	titles, dois, years, papers = get_vars(AUTHORS_TO_STUDY)
	random_papers = random.sample(papers, 10)

	driver = webdriver.Firefox()
	wait = WebDriverWait(driver, 90)

	gscholar_dict_list = []

	for paper in papers:
	    idx = papers.index(paper)
	    update_gscholar_dict_list(paper, titles, dois, years, idx)
	    time.sleep(0.2+random.uniform(0,0.2))

	# for paper in random_papers:
	# 	idx = papers.index(paper)
	# 	cur_idx = random_papers.index(paper)
	# 	update_gscholar_dict_list_random(paper, titles, dois, years, idx, cur_idx)
	# 	time.sleep(0.2+random.uniform(0,0.2))

	print('Everything done!')
	driver.close()
	driver.quit()

	pd.DataFrame(gscholar_dict_list).to_csv(GSCHOLAR_DATA, index = False)

