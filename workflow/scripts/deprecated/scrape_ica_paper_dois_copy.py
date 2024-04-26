"""get ICA publication paper info"""

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
import sys

ICA_PAPER_DF = sys.argv[1]

def get_journal_and_urls():
	journals = [
		'Journal of Communication',
		'Human Communication Research',
		'Communication Theory',
		'Journal of Computer-Mediated Communication',
		'Communication, Culture and Critique',
	]
	j_urls = [
		'https://academic.oup.com/joc/issue',
		'https://academic.oup.com/hcr/issue',
		'https://academic.oup.com/ct/issue',
		'https://academic.oup.com/jcmc/issue',
		'https://academic.oup.com/ccc/issue',
	]
	url_j_dic = dict(zip(j_urls, journals))
	return journals, j_urls, url_j_dic 

def get_volume_and_issue():
	'''
	there are two "div.issue-info-pub". First is the left panel and second is 
		something like "Volume 72, Issue 3, June 2022"
		I am extracting the first one here
	Returns:
		- 'Volume 72'
		- 'Issue 3'
	'''
	volume_and_issue = wait.until(EC.presence_of_element_located((
		By.CSS_SELECTOR, "div.issue-info-pub"
	))).text
	split_text = volume_and_issue.split(', ')
	volume_num = split_text[0]
	issue_num = split_text[1]
	return volume_num, issue_num

def get_mo_and_yr():
	# get the issue date information from the left panel
	issue_date = wait.until(EC.presence_of_element_located((
		By.CSS_SELECTOR, "div.issue-info-date"
	))).text
	split_text = issue_date.split(' ')
	year = split_text[-1]
	# sometimes the issue_date is in the format of "1 March 2004"
	# for example: https://academic.oup.com/joc/issue/54/1
	if len(split_text) > 2:
		month = split_text[1]
	else:
		month = split_text[0]
	return month, year

def extract_paper_info(tuples, journal, volume_num, issue_num, month, year):
	# There are several sections. For example, 
	# in 'https://academic.oup.com/joc/issue/72/3?browseBy=volume'
	# there are four sections: articles, Corrigendum, correction, and book reviews
	sections = wait.until(EC.presence_of_all_elements_located((
			By.CSS_SELECTOR, "div.section-container > section"
		)))

	for section in sections:
		section_index = sections.index(section) + 1

		# the section name is the category, e.g., Articles
		category = section.find_element(
			By.CSS_SELECTOR, 'h4'
		).get_attribute('innerHTML')

		# all individual papers in each section
		papers = section.find_elements(
			By.CSS_SELECTOR, "div.al-article-items"
		)

		for paper in papers:

			paper_index = papers.index(paper) + 1

			# title

			title_link = paper.find_element(
				By.CSS_SELECTOR, "a.at-articleLink"
			)

			url = title_link.get_attribute('href')

			try:
				# if it has "get access", for example, https://academic.oup.com/hcr/issue/33/1
				#  the real title is within the first span
				title = title_link.find_element(
					By.CSS_SELECTOR, "span.access-title"
				).text 
			# if there is no such "span.access-title", then just get the title as usual
			except:
				title = title_link.text 

			# Sometimes, the title is weird, for example:
			# some of those in https://academic.oup.com/joc/issue/57/1
			if title not in [
				'German Abstract',
				'Chinese Abstract',
				'Korean Abstract',
				'Japanese Abstract',
				'French Abstract',
				'Russian Abstract',
				'Abrabic Abstract',
				'Spanish Abstract',
			]:

				# publication info (page numbers, doi, url)
				pub_info = paper.find_element(
					By.CSS_SELECTOR, ".pub-history-row.clearfix"
				).text

				pub_info_elements = pub_info.split(', ')
				for e in pub_info_elements:
					# JCMC is special as it does not contain pages information
					if journal != 'Journal of Computer-Mediated Communication':
						if "Pages" in e:
							pages = re.sub('Pages ', '', e)
						elif "Page" in e:
							pages = re.sub('Page ', '', e)
					else:
						pages = np.nan 
					if 'https://' in e:
						doi = re.sub('https://doi.org/', '', e)

				# abstract
				try:
					abstract_tab = WebDriverWait(paper, 2).until(
						EC.element_to_be_clickable((
							By.CSS_SELECTOR, "div.abstract-link > a"
					)))
					abstract_header = abstract_tab.text 
					# Sometimes, the header is 'Extract'
					if abstract_header == 'Abstract':
						abstract_tab.click()
						# sometimes, you can click the tab but there is no content in it
						try:
							abstracts = WebDriverWait(paper, 2).until(
								EC.presence_of_all_elements_located((
									By.CSS_SELECTOR, "p.chapter-para"
							)))
							# number of paragraphs when you open the abstract tab
							# this is to make sure I didn't omit anything
							abstract_para_num = len(abstracts)
							# if multiple paragraphs, include all of them 
							if abstract_para_num != 1:
								all_abstract_text = [i.text for i in abstracts]
								abstract = '\n\n'.join(all_abstract_text)
							# otherwise get the first and of course, the only one para
							else:
								abstract = abstracts[0].text 
						# there is tab and it is "Abstract", but abstract is empty:
						except:
							abstract = np.nan 
							abstract_para_num = 0
					# There is abstract_tab but it is "Extract", not "Abstract"
					else:
						abstract = np.nan 
						abstract_para_num = np.nan 
				# if there is no abstract_tab
				except (NoSuchElementException, TimeoutException):
					abstract = np.nan 
					abstract_para_num = np.nan

				tuples.append((
					journal,
					volume_num,
					issue_num,
					month,
					year,
					category,
					title,
					url,
					doi,
					pages,
					abstract,
					abstract_para_num,
				))
			time.sleep(0.1+random.uniform(0,0.1))
	# all sections done! print the completed journal-issue
	print(f'{journal} ({month} {year}) is done')
	time.sleep(0.1+random.uniform(0,0.1)) 

def check_for_previous_tab():
	try:
		previous_tab = wait.until(EC.element_to_be_clickable((
			By.CSS_SELECTOR, "span.issue-link--prev  > a"
		)))
		tab_exists = True
		previous_url = previous_tab.get_attribute('href')
	except:
		tab_exists = False 
		previous_url = np.nan 
	return tab_exists, previous_url

def click_browse_by_volume():
	browse_volume_link = wait.until(EC.element_to_be_clickable((
		By.CSS_SELECTOR, "div.issue-browse-volume-link > a"
	)))
	browse_volume_link.click()

def extract_first_url(j_url, tuples, journal):
	driver.get(j_url)
	click_browse_by_volume()
	volume_num, issue_num = get_volume_and_issue()
	month, year = get_mo_and_yr()
	extract_paper_info(tuples, journal, volume_num, issue_num, month, year)
	tab_exists, previous_url = check_for_previous_tab()
	return tab_exists, previous_url

def extract_previous_url(previous_url, tuples, journal):
	driver.get(previous_url)
	volume_num, issue_num = get_volume_and_issue()
	month, year = get_mo_and_yr()
	extract_paper_info(tuples, journal, volume_num, issue_num, month, year)
	tab_exists, previous_url = check_for_previous_tab()
	return tab_exists, previous_url

if __name__ == '__main__':
	driver = webdriver.Firefox()
	wait = WebDriverWait(driver, 3)
	journals, j_urls, url_j_dic = get_journal_and_urls()

	tuples = []

	for j_url in [j_urls[-1]]:
		journal = url_j_dic[j_url]
		journal_index = j_urls.index(j_url)
		if journal_index < 4:
			journal_next = url_j_dic[j_urls[journal_index + 1]]
		tab_exists, previous_url = extract_first_url(j_url, tuples, journal)
		while tab_exists:
			tab_exists, previous_url = extract_previous_url(
				previous_url, tuples, journal)
		print(f"{journal} completed; {journal_next} begins.")
		time.sleep(1+random.uniform(0,1))
	
	df = pd.DataFrame(
		list(tuples), 
		columns = [
			'journal', 'volumn', 'issue', 
			'month', 'year', 'category', 'title', 
			'url', 'doi', 'pages',  
			'abstract', 'abstract_para_num',
		])

	df.to_csv(ICA_PAPER_DF, index = False)


