"""add multiple variables to authors to study and papers to study

Returns: authors_to_study_expanded and papers_to_study_expanded

"""

import sys
import pandas as pd
import numpy as np

AUTHORID_WITH_VARS = sys.argv[1]
AUTHORS_TO_STUDY = sys.argv[2]
PAPERS_TO_STUDY = sys.argv[3]
AUTHORS_TO_STUDY_EXPANDED = sys.argv[4]
PAPERS_TO_STUDY_EXPANDED = sys.argv[5]

def get_cross_and_num_stuff_dic(df):
	'''cross country, cross type, cross gender, and cross race
		number of countries, number of races, and with us authors

	Input: 
		authors
	
	Returns:
		seven dicts
	'''
	cross_country_dic = {}
	cross_type_dic = {}
	cross_gender_dic = {}
	cross_race_dic = {}
	num_country_dic = {}
	num_race_dic = {}
	with_us_authors_dic = {}
	# cross race or not, if not, what race?
	cross_race_details_dic = {}
	# cross gender ot not, if not, what gender?
	cross_gender_details_dic = {}
	for group in df.groupby('doi'):
		DOI = group[0]
		# counry:
		country_codes = group[1]['countrypred'].tolist()
		num_of_cntry = len(list(set(country_codes)))
		num_country_dic[DOI] = num_of_cntry
		if num_of_cntry != 1:
			cross_country_dic[DOI] = True
		else:
			cross_country_dic[DOI] = False
		if 'US' in country_codes:
			with_us_authors_dic[DOI] = True 
		else:
			with_us_authors_dic[DOI] = False
		
		# afftypes
		types = group[1]['afftypepred'].tolist()
		num_of_types = len(list(set(types)))
		if num_of_types != 1:
			cross_type_dic[DOI] = True
		else:
			cross_type_dic[DOI] = False
		
		# genders
		genders = group[1]['genderpred'].tolist()
		num_of_genders = len(list(set(genders)))
		if num_of_genders != 1:
			cross_gender_dic[DOI] = True
			cross_gender_details_dic[DOI] = 'cross gender'
		else:
			cross_gender_dic[DOI] = False
			cross_gender_details_dic[DOI] = genders[0] + ' ' + 'only'
		
		# races
		races = group[1]['racepred'].tolist()
		num_of_races = len(list(set(races)))
		num_race_dic[DOI] = num_of_races
		if num_of_races != 1:
			cross_race_dic[DOI] = True
			cross_race_details_dic[DOI] = 'cross race'
		else:
			cross_race_dic[DOI] = False
			cross_race_details_dic[DOI] = races[0] + ' ' + 'only'
				
	return cross_country_dic,\
			cross_type_dic,\
			cross_gender_dic,\
			cross_race_dic,\
			num_country_dic,\
			num_race_dic,\
			with_us_authors_dic,\
			cross_race_details_dic,\
			cross_gender_details_dic

def get_first_author_stuff_dic(df):
	first_author_gender_dic = {}
	first_author_race_dic = {}
	first_author_country_dic = {}
	first_author_afftype_dic = {}
	for group in df.groupby('doi'):
		DOI = group[0]
		group[1].sort_values(by='authorPosition', ascending = True)
		first_author_gender = group[1].iloc[0, :]['genderpred'][0]
		first_author_gender_dic[DOI] = first_author_gender
		
		first_author_race = group[1].iloc[0, :]['racepred']
		first_author_race_dic[DOI] = first_author_race
		
		first_author_country = group[1].iloc[0, :]['countrypred']
		first_author_country_dic[DOI] = first_author_country
		
		first_author_afftype = group[1].iloc[0, :]['afftypepred']
		first_author_afftype_dic[DOI] = first_author_afftype
		
	return first_author_gender_dic, \
		first_author_race_dic, \
		first_author_country_dic, \
		first_author_afftype_dic

if __name__ == '__main__':
	cutoff_year = 2000

	# import and filter
	aid_df = pd.read_csv(AUTHORID_WITH_VARS)
	authors = pd.read_csv(AUTHORS_TO_STUDY)
	papers = pd.read_csv(PAPERS_TO_STUDY)
	authors = authors[authors.year >= cutoff_year]
	papers = papers[papers.year >= cutoff_year]

	# number of authors dic
	num_author_dic = dict(zip(authors.doi, authors.numberOfAuthors))

	# dics based on authorid
	id_country_dict = dict(zip(aid_df.authorID, aid_df.new_country_code))
	id_gender_dict = dict(zip(aid_df.authorID, aid_df.gender_prediction))
	id_afftype_dict = dict(zip(aid_df.authorID, aid_df.new_afftype))
	id_race_dict = dict(zip(aid_df.authorID, aid_df.race))

	authors['countrypred'] = [id_country_dict[x] for x in authors.authorID]
	authors['genderpred'] = [id_gender_dict[x] for x in authors.authorID]
	authors['racepred'] = [id_race_dict[x] for x in authors.authorID]
	authors['afftypepred'] = [id_afftype_dict[x] for x in authors.authorID]

	cross_country_dic,\
	cross_type_dic,\
	cross_gender_dic,\
	cross_race_dic,\
	num_country_dic,\
	num_race_dic,\
	with_us_authors_dic,\
	cross_race_details_dic,\
	cross_gender_details_dic = get_cross_and_num_stuff_dic(authors)

	first_author_gender_dic,\
	first_author_race_dic,\
	first_author_country_dic,\
	first_author_afftype_dic = get_first_author_stuff_dic(authors)

	papers['cross_country'] = [cross_country_dic[x] for x in papers.doi]
	papers['cross_type'] = [cross_type_dic[x] for x in papers.doi]
	papers['cross_gender'] = [cross_gender_dic[x] for x in papers.doi]
	papers['cross_race'] = [cross_race_dic[x] for x in papers.doi]
	papers['num_race'] = [num_race_dic[x] for x in papers.doi]
	papers['num_country'] = [num_country_dic[x] for x in papers.doi]
	papers['cross_gender_and_race'] = papers['cross_gender'] & papers['cross_race']
	papers['cross_gender_and_country'] = papers['cross_gender'] & papers['cross_country']
	papers['cross_country_and_race'] = papers['cross_country'] & papers['cross_race']
	papers['cross_gender_race_and_country'] = papers[
		'cross_country'] & papers['cross_gender'] & papers['cross_race']
	papers['numberOfAuthors'] = [num_author_dic[x] for x in papers.doi]
	papers['first_author_gender'] = [first_author_gender_dic[x] for x in papers.doi]
	papers['first_author_race'] = [first_author_race_dic[x] for x in papers.doi]
	papers['first_author_country'] = [first_author_country_dic[x] for x in papers.doi]
	papers['first_author_afftype'] = [first_author_afftype_dic[x] for x in papers.doi]
	papers['with_us_authors'] = [with_us_authors_dic[x] for x in papers.doi]
	papers['cross_race_details'] = [cross_race_details_dic[x] for x in papers.doi]
	papers['cross_gender_details'] = [cross_gender_details_dic[x] for x in papers.doi]
	
	papers.to_csv(PAPERS_TO_STUDY_EXPANDED, index = False)
	authors.to_csv(AUTHORS_TO_STUDY_EXPANDED, index = False)
