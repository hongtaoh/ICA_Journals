"""get paper and author data on ICA journal publications using BeautifulSoup"""

import sys
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import random
import time 
import requests
import re
import json

ICA_PAPER_DF = sys.argv[1]
ICA_AUTHOR_DF = sys.argv[2]
NO_AUTHOR_URLS = sys.argv[3]

def get_soup(url, idx):
	headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36" \
	"(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
	}
	response = requests.get(url=url, headers=headers)
	while response.status_code != 200:
		time.sleep(1)
		print(f"{idx} : {url} status code is {response.status_code}, retrying ...")
		response = requests.get(url=url, headers=headers)
	html = response.text 
	soup = BeautifulSoup(html, 'html.parser')
	return soup

def update_author_data(url, soup, no_author_urls, author_data_tuples):
	doi = url_doi_dic[url]
	journal = url_journal_dic[url]
	title = url_title_dic[url]
	year = url_year_dic[url]
	# this return a list
	# sometimes there is no authors: https://academic.oup.com/joc/article/33/4/20/4282700
	try:
		authors = soup.find(class_="al-authors-list").find_all(
			class_="al-author-name-more js-flyout-wrap")
		author_num = len(authors)
		for author in authors:
			author_position = authors.index(author) + 1
			'''author names
			'''
			try:
				fullname = author.find(class_="info-card-name").text.strip()
				fullname_split = fullname.split(' ')
				lastname = fullname_split[-1]
				if fullname_split:
					if len(fullname_split) == 2:
						firstname = fullname_split[0]
					# e.g., "M. J. Clarke"
					elif len(fullname_split) > 2 and len(fullname_split[0]) <= 2 and len(fullname_split[1]) <= 2:
						firstname = fullname_split[0]
					# e.g., "M. Jennifer Clarke"
					elif len(fullname_split) > 2 and len(fullname_split[0]) <= 2 and len(fullname_split[1]) > 2:
						firstname = fullname_split[1]
					# g.g., "Mike John Clarke"
					elif len(fullname_split) > 2 and len(fullname_split[0]) > 2:
						firstname = fullname_split[0]
					else:
						firstname = 'ERROR!'
			except:
				fullname = np.nan
				lastname = np.nan 
				firstname = np.nan
			'''author affiliations
			'''
			try:
				aff = author.find(class_="aff")
				# sometimes, there is no 'span': 
				# https://academic.oup.com/ccc/article/15/2/269/6561482
				if aff.find('span') is not None:
					aff.find('span').extract()
				aff = aff.text.strip()
			except:
				aff = np.nan
			'''author correspondence
			'''
			try:
				cor = author.find(class_="info-author-correspondence").text.strip()
			except:
				cor = np.nan
			'''google scholar link
			'''
			try:
				gscholar_link = author.find(
					class_="info-card-search info-card-search-google").find('a')['href']
			except:
				gscholar_link = np.nan
			'''update data tuples
			'''
			author_data_tuples.append((
				doi, url, journal, title, year,
				author_num, author_position, fullname,
				firstname, lastname, aff, cor, gscholar_link
			))
	except:
		no_author_urls.append(url)
		author_data_tuples.append((
			doi, url, journal, title, year
		))
		print(f'{url}')
	return author_data_tuples

if __name__ == '__main__':
	# read data
	ica_papers = pd.read_csv(ICA_PAPER_DF)
	
	# extract useful info
	paper_urls = ica_papers.url.tolist()
	paper_dois = ica_papers.doi.tolist()
	years = ica_papers.year.tolist()
	journals = ica_papers.journal.tolist()
	titles = ica_papers.title.tolist()
	
	# dics
	url_doi_dic = dict(zip(paper_urls, paper_dois))
	url_year_dic = dict(zip(paper_urls, years))
	url_title_dic = dict(zip(paper_urls, titles))
	url_journal_dic = dict(zip(paper_urls, journals))
	
	# initiate data tuples
	author_data_tuples = []

	# papers that do not have any author data
	# e.g., https://academic.oup.com/joc/article-abstract/38/4/2/4210505
	no_author_urls = []

	total_urls = len(paper_urls)
	print(f'Total number of URLs to crawl: {total_urls}')
	
	random_paper_urls = random.sample(paper_urls, 10)

	# for url in random_paper_urls:
	# 	idx = random_paper_urls.index(url) + 1
	for url in paper_urls:
		idx = paper_urls.index(url) + 1
		soup = get_soup(url, idx)
		update_author_data(url, soup, no_author_urls, author_data_tuples)
		print(f'{idx} is done')
		time.sleep(0.5 + random.uniform(0, 0.4))
	
	# build dataframe
	author_df = pd.DataFrame(author_data_tuples, columns=[
		'doi',
		'url',
		'journal',
		'title',
		'year',
		'numberOfAuthros',
		'authorPosition',
		'fullname',
		'firstname',
		'lastname',
		'affiliation',
		'correspondence',
		'googleScholarLink'
	])
	
	author_df.to_csv(ICA_AUTHOR_DF, index=False)
	with open(NO_AUTHOR_URLS, 'w') as f:
		for url in no_author_urls:
			f.write("%s\n" % url)
