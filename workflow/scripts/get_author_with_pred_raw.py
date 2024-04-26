"""get predictions for race, and affiliations. I name the output as raw because I do not

change their column order here. I output the raw file and later I'll change the column order. 

This way, I don't need to run the whole file again which takes some time. 

"""

import sys
import pandas as pd
import json
import numpy as np
import requests
import re
from ethnicolr import census_ln, pred_census_ln

AUTHOR_WITH_GENDER = sys.argv[1]
ROR_RAW_DATA = sys.argv[2]
AUTHOR_WITH_PRED_RAW = sys.argv[3]

def get_race_pred(authorWithGender):
	'''
	Purpose:
		get race predictions with 'racePredAccuracy'
	Input:
		authorWithGender
	Output:
		race_pred
	'''
	race_pred = pred_census_ln(authorWithGender, 'lastName', year=2010)
	race_pred_sub = race_pred[['api', 'black', 'hispanic', 'white']]
	# axis = 1 means row-wise
	# get the highest prob
	raceHighest = race_pred_sub.apply(
		lambda row: row.nlargest(2).values[0], axis = 1)
	# get the second highest prob
	raceSecondHighest = race_pred_sub.apply(
		lambda row: row.nlargest(2).values[-1], axis = 1)
	raceDiff = raceHighest - raceSecondHighest
	race_pred['raceHighest'] = raceHighest
	race_pred['raceSecondHighest'] = raceSecondHighest
	race_pred['raceDiff'] = raceDiff
	race_pred['racePredAccuracy'] = np.where(
		(race_pred['raceHighest'] >= 0.80) & (race_pred['raceDiff'] >= 0.30),
		'High',
		'Low'
	)
	return race_pred

def notNaN(aff):
	'''returns True if it is not nan
	'''
	return aff == aff

def process_affiliation_text(aff):
	'''process aff text: lower case, remove content within (), keep only characters
	'''
	if notNaN(aff):
		aff = aff.lower()
		# delete anything between ()
		aff = re.sub(r'\(.*?\)', '', aff)
		# remove anything other than characters
		aff = re.sub('[^a-z ]+', ' ', aff)
		aff = ' '.join(aff.split())
		return aff
	else:
		return np.nan

def get_deduplicated_affs_to_predict(race_pred):
	'''deduplicate the column of affProcessed, remove nan and '', and return the 
	list of dedup_affs_to_predict
	'''
	affs = race_pred.affProcessed
	# deduplicate
	affs = list(set(affs))
	# remove nan
	affs = [x for x in affs if str(x) != 'nan' and x != '']
	print(f'There are in total {len(affs)} deduplicated affiliations to predict')
	return affs

def load_ror_dataset(ROR_RAW_DATA):
	'''read in ROR_DATA
	Output:
		a list of dictionaries
	'''
	with open(ROR_RAW_DATA, 'r') as myfile:
		data=myfile.read()
	data = json.loads(data)
	return data

def get_ror_dics(rorData):
	'''dictionaries of 
		1. ror aff name in lower case and its corresponding affname in upper case
		2. ror aff name (upper case) and it corresponding ror id
	Note that these two dics contain ALL affiliations in rorData
	'''
	ror_lower_upper_dic = {}
	ror_upper_id_dic = {}
	for i in rorData:
		upper_affname = i['name']
		lower_affname = i['name'].lower()
		ror_lower_upper_dic[lower_affname] = upper_affname
		ror_upper_id_dic[upper_affname] = i['id']
	return ror_lower_upper_dic, ror_upper_id_dic

def get_select_ror_affnames(rorData, target_str, to_remove_affs):
	'''
	ror has A LOT of affiliations. I only select some of them. 

	In the selected ones, some obviously will lead to wrong (exact) match later, 
		so I delete them here. 

	The select affnames are in lower case. 
	'''
	select_ror_affnames = []
	for i in rorData:
		affname = i['name'].lower()
		if any(x in affname for x in target_str):
			select_ror_affnames.append(affname)
	select_ror_affnames = [x for x in select_ror_affnames if x not in to_remove_affs]
	print(f'There are a total of {len(select_ror_affnames)} select ror affnames')
	return select_ror_affnames

def get_exact_match_list(dedup_affs_to_predict, select_ror_affnames):
	"""for each aff in dedup_affs_to_predict, check whether any of its substring 
	can be exactly matched with any of the aff in select_ror_affnames


	Output:
		a dictionary where key is aff_to_predict, and value is the matched 
		aff in select ror affnames
	"""
	total = len(dedup_affs_to_predict)
	exact_match_dic = {}
	exact_match = 0
	for aff_to_predict in dedup_affs_to_predict:
		exact_match_list = []
		for x in select_ror_affnames:
			if x in aff_to_predict:
				exact_match += 1
				exact_match_list.append(x)
			# if multiple exact matches, use the longest string
			if exact_match_list:
				result = max(exact_match_list, key=len)
				exact_match_dic[aff_to_predict] = result
	print(f'{exact_match} out of {total} affiliations have been exactly matched')
	return exact_match_dic

def get_to_api_query_list(dedup_affs_to_predict, exact_match_dic):
	"""affs in dedup_affs_to_predict that are not exactly matched
	"""
	to_api_query_list = [
		x for x in dedup_affs_to_predict if x not in exact_match_dic.keys()]
	print(f'{len(to_api_query_list)} affiliations were not exactly matched. Will use API to query')
	return to_api_query_list

def get_api_query_match_dic(to_api_query_list):
	'''For affs not exactly matched, query through ror api and get the first result
	Output:
		a dictionary where keys are aff in to_api_query_list and value is 
		the matched ror affname in lower case
	'''
	api_query_match_dic = {}
	api_query_matched = 0
	# for aff in to_api_query_list[0:10]:
	for aff in to_api_query_list:
		idx = to_api_query_list.index(aff) + 1
		response = requests.get('https://api.ror.org/organizations?query='+aff)
		j = response.json()
		try:
			j = j['items'][0]
			ror_matched_affname = j['name'].lower()
			api_query_matched += 1
		except:
			ror_matched_affname = np.nan
		api_query_match_dic[aff] = ror_matched_affname
		print(f'{idx}/{len(to_api_query_list)} is done')
	print(f'{api_query_matched} out of {len(to_api_query_list)} have been identified and matched on ROR')
	return api_query_match_dic

def get_match_method(aff_processed, exact_match_dic, api_query_match_dic):
	"""add a column called "matchMethod" in race_pred
	The match method should be either 'Exact', 'API_QUERY', or np.nan
	"""
	if aff_processed in exact_match_dic.keys():
		return 'Exact'
	elif aff_processed in api_query_match_dic.keys():
		# print('good')
		return 'API_QUERY'
	else:
		return np.nan

def get_matched_ror_affname(aff_processed, combined_dic, ror_lower_upper_dic):
	"""get corresponding ror affname in upper case
	"""
	try:
		lower_ror_affname = combined_dic[aff_processed]
		return ror_lower_upper_dic[lower_ror_affname]
	except:
		return np.nan

def get_ror_id(ror_affname, ror_upper_id_dic):
	"""get associated ror id
	"""
	try:
		return ror_upper_id_dic[ror_affname]
	except:
		return np.nan

def get_gscholarLink(row):
	# add google scholar link
	gscholar_str = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%252C50&q='
	if str(row['firstName']) != 'nan' and str(row['lastName']) != 'nan':
		gscholarLink = gscholar_str + str(row['firstName']) + '+' + str(row['lastName'])
	else:
		gscholarLink = np.nan
	return gscholarLink

def update_race_pred(race_pred, exact_match_dic, api_query_match_dic):
	race_pred['matchMethod'] = race_pred['affProcessed'].apply(
		get_match_method, 
		args=(exact_match_dic, api_query_match_dic)
	)
	combined_dic = dict(
		list(exact_match_dic.items()) + list(api_query_match_dic.items()))
	race_pred['ROR_AFFNAME'] = race_pred['affProcessed'].apply(
		get_matched_ror_affname, 
		args=(combined_dic, ror_lower_upper_dic)
	)
	race_pred['ROR_ID'] = race_pred['ROR_AFFNAME'].apply(
		get_ror_id,
		args=(ror_upper_id_dic, )
	)
	race_pred['gscholarLink'] = race_pred.apply(get_gscholarLink, axis = 1)
	return race_pred

if __name__ == '__main__':
	authorWithGender = pd.read_csv(AUTHOR_WITH_GENDER)
	# note that race_pred contains both gender and race predictions
	race_pred = get_race_pred(authorWithGender)
	# create a column of "affiliation processed":
	race_pred['affProcessed'] = [
		process_affiliation_text(aff) for aff in race_pred.affiliation]
	dedup_affs_to_predict = get_deduplicated_affs_to_predict(race_pred)

	rorData = load_ror_dataset(ROR_RAW_DATA)
	ror_lower_upper_dic, ror_upper_id_dic = get_ror_dics(rorData)
	target_str = [
		'university', 
		'school',
		'college', 
		"universität", 
		"université", 
		"inc.", 
		"company", 
		'coorporation',
		'institute',
		'center',
		'centre',
	]
	to_remove_affs = [
		'he university',
		'ege university',
		'ces university',
		'coe college',
		'kes college',
		'ie university',
		'health center',
		'cancer institute',
		'rk university',
		'air university',
	]
	select_ror_affnames = get_select_ror_affnames(
		rorData, target_str, to_remove_affs)

	exact_match_dic = get_exact_match_list(
		dedup_affs_to_predict, select_ror_affnames)
	to_api_query_list = get_to_api_query_list(
		dedup_affs_to_predict, exact_match_dic)

	api_query_match_dic = get_api_query_match_dic(
		to_api_query_list)

	update_race_pred(race_pred, exact_match_dic, api_query_match_dic)

	race_pred.to_csv(AUTHOR_WITH_PRED_RAW, index=False)
