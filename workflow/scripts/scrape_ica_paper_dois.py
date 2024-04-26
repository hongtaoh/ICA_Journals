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

def extract_paper_info(tuples, journal, volume_num, issue_num, issue_text, month, year, issue_url):
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
					issue_url,
					volume_num,
					issue_num,
					issue_text,
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
	time.sleep(0.1+random.uniform(0,0.1)) 

def click_browse_by_volume():
	browse_volume_link = wait.until(EC.element_to_be_clickable((
		By.CSS_SELECTOR, "div.issue-browse-volume-link > a"
	)))
	browse_volume_link.click()

def get_volume_option_texts():
	'''
	get all volume options
	'''
	volume_options = driver.find_elements(
		By.CSS_SELECTOR, '.issue-browse-year-list.issue-browse-select > option')
	volume_option_texts = [v.text for v in volume_options]
	return volume_option_texts

def get_issue_option_texts():
	issue_options = driver.find_elements(
		By.CSS_SELECTOR, '.issue-browse-issues-list > option'
	)
	issue_option_texts = [i.text for i in issue_options]
	return issue_option_texts

def get_issue_num_year_and_month(issue_text):
	''' to extract issue number, year, and month information from an issue text 
	  such as  "Issue 1, March 1981, Pages 3–240"
	'''
	issue_info_list = issue_text.split(', ')
	# example issue_num: issue 2
	issue_num = issue_info_list[0]
	# year and month:
	yr_n_mo = issue_info_list[1]
	split_text = yr_n_mo.split(' ')
	year = split_text[-1]
	# sometimes the issue_date is in the format of "1 March 2004"
	# for example: https://academic.oup.com/joc/issue/54/1
	if len(split_text) > 2:
		month = split_text[1]
	else:
		month = split_text[0]
	return issue_num, month, year 

if __name__ == '__main__':
	driver = webdriver.Firefox()
	wait = WebDriverWait(driver, 5)
	journals, j_urls, url_j_dic = get_journal_and_urls()


	tuples = []

	for j_url in j_urls:
		start_str = j_url
		end_str = "?browseBy=volume"
		journal = url_j_dic[j_url]
		print(f"{journal} has started")
		driver.get(j_url)
		click_browse_by_volume()
		# check total number of vlumes 
		volume_option_texts = get_volume_option_texts()
		total_volume = int(volume_option_texts[0])
		print(f'Total volume in {journal}: {total_volume}')
		# for each volume
		# for v in reversed(range(10, 12)):
		for v in reversed(range(1, total_volume+1)):
			volume_num = f'Volume {v}'
			print(f'{volume_num} has started!')
			'''
			to go to the first issue of the current volume
			this is to make sure that get_issue_option_texts() returns issues of the current 
			volume, rather than the previous volume
			'''
			current_volume_url = f'{start_str}/{v}/1{end_str}'
			driver.get(current_volume_url)
			issue_texts = get_issue_option_texts()
			for issue_text in reversed(issue_texts):
				# issue_text example: "Issue 1, March 2006, Pages 1–234"
				# reversed because most recent issues should be crawled first
				# issue eample: "Issue 1, March 1981, Pages 3–240"
				issue_num, month, year = get_issue_num_year_and_month(issue_text)
				# this is to prevent error when issue text is "Issue suppl_1, August 2006" (joc)
				issue = issue_num.split(' ')[1]
				issue_url = f'{start_str}/{v}/{issue}{end_str}'
				driver.get(issue_url)
				extract_paper_info(tuples, journal, volume_num, issue_num, issue_text, month, year, issue_url)
				print(f'({volume_num}, {issue_text}) is done')
		print(f"{journal} is done")
		time.sleep(1+random.uniform(0,1))
	print('Everything is done!')
	driver.close()
	driver.quit()
	
	df = pd.DataFrame(
		list(tuples), 
		columns = [
			'journal', 'issueURL', 'volumn', 'issue', 'issueText',
			'month', 'year', 'category', 'title', 
			'url', 'doi', 'pages',  
			'abstract', 'abstract_para_num',
		])

	df.to_csv(ICA_PAPER_DF, index = False)


