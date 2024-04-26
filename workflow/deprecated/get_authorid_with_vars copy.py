"""in this script, I processed the gender, race and aff coded data
and return basically dictionaries through a dataframe

"""

import sys
import pandas as pd
import json
import numpy as np

ROR_RAW_DATA = sys.argv[1]
HONGTAO_AFF_RESULT = sys.argv[2]
KRISTEN_AFF_RESULT = sys.argv[3]
HALEY_GR_RESULT = sys.argv[4]
JAEMIN_GR_RESULT = sys.argv[5]
JONGMIN_GR_RESULT = sys.argv[6]
MATTHEW_GR_RESULT = sys.argv[7]
JEFF_GR_RESULT = sys.argv[8]
MICHELLE_GR_RESULT = sys.argv[9]
AUTHORID_WITH_VARS = sys.argv[10]

def filter_aff_df(source, cutoff_year):
	'''filter for aff results

	INPUT:
		- source: either HONGTAO_AFF_RESULT, or KRISTEN_AFF_RESULT
		- cutoff_year

	OUTPUT:
		- a dataframe
	'''
	df = pd.read_csv(source)
	df = df[df.year >= cutoff_year][
		['authorID', 'country_code', 'aff_type', 'ROR_ID']]
	return df 

def filter_gr_df(source, cutoff_year, wanted_cols):
	'''filter for gender and race data
	'''
	return source[source.year >= cutoff_year][wanted_cols]

def load_ror_dataset(ROR_RAW_DATA):
	'''read in ROR_DATA
	Output:
		a list of dictionaries (in fact, json objects)
	'''
	with open(ROR_RAW_DATA, 'r') as myfile:
		data=myfile.read()
	data = json.loads(data)
	return data

def update_two_dicts(ror, ror_cntry_dic, ror_afftype_dic):
	'''update the two dicts using data from ror
	'''
	for i in ror:
		ror_id = i['id']
		cntry = i['country']['country_code']
		try:
			afftype = i['types'][0]
			if afftype == 'Education':
				afftype = afftype
			else:
				afftype = 'Non Education'
		except:
			afftype = None
		ror_cntry_dic[ror_id] = cntry
		ror_afftype_dic[ror_id] = afftype
	# Chinese Academy of Social Sciences
	# should be edu in this case. Professor Weishan Miao
	ror_afftype_dic['https://ror.org/05bxbmy32'] = 'Education'

def get_new_cntry_code(row):
	'''if I have added the country code manually, use that
	otherwise, use the ror data (through the updated dic)
	'''
	if pd.isnull(row['country_code']):
		new_country_code = ror_cntry_dic[row['ROR_ID']]
	else:
		new_country_code = row['country_code']
	return new_country_code

def get_new_afftype(row):
	'''if I have added the affiliation type code manually, use that
	otherwise, use the ror data (through the updated dic)
	'''
	if pd.isnull(row['aff_type']):
		new_afftype = ror_afftype_dic[row['ROR_ID']]
	elif row['aff_type'] == '1':
		new_afftype = 'Education'
	elif row['aff_type'] == '0':
		new_afftype = 'Non Education'
	return new_afftype

def recode_race(row):
	race_txt = 'race_prediction'
	if row[race_txt] == 0:
		return 'White'
	elif row[race_txt] == 1:
		return 'Black'
	elif row[race_txt] == 2:
		return 'Asian'
	elif row[race_txt] == 3:
		return 'Hispanic'
	elif row[race_txt] == 4:
		return 'Middle Eastern'
	elif row[race_txt] == 5:
		return 'Indigenous'

if __name__ == '__main__':
	cutoff_year = 2000

	######### AFF
	df1 = filter_aff_df(HONGTAO_AFF_RESULT, cutoff_year)
	df2 = filter_aff_df(KRISTEN_AFF_RESULT, cutoff_year)

	ror = load_ror_dataset(ROR_RAW_DATA)

	# initiate two dicts
	ror_cntry_dic = {}
	ror_afftype_dic = {}

	update_two_dicts(ror, ror_cntry_dic, ror_afftype_dic)

	df1['new_country_code'] = df1.apply(get_new_cntry_code, axis = 1)
	df1['new_afftype'] = df1.apply(get_new_afftype, axis = 1)
	df2['new_country_code'] = df2.apply(get_new_cntry_code, axis = 1)
	df2['new_afftype'] = df2.apply(get_new_afftype, axis = 1)
	aff_df = pd.concat([df1, df2], ignore_index = True)
	aff_df = aff_df[['authorID', 'new_country_code', 'new_afftype']]

	########### Gender and Race
	haley = pd.read_csv(HALEY_GR_RESULT)
	matthew = pd.read_csv(MATTHEW_GR_RESULT)
	michelle = pd.read_csv(MICHELLE_GR_RESULT)
	jeff = pd.read_csv(JEFF_GR_RESULT)
	jongmin = pd.read_csv(JONGMIN_GR_RESULT)
	jaemin = pd.read_csv(JAEMIN_GR_RESULT)

	gr_wanted_cols = ['authorID', 'gender_prediction', 'race_prediction']
	haley = filter_gr_df(haley, cutoff_year, gr_wanted_cols)
	matthew = filter_gr_df(matthew, cutoff_year, gr_wanted_cols)
	michelle = filter_gr_df(michelle, cutoff_year, gr_wanted_cols)
	jeff = filter_gr_df(jeff, cutoff_year, gr_wanted_cols)
	# Temporary, DElete later!!!!!!!!!
	# jeff = jeff[
	# 	(jeff.gender_prediction.notnull()) & (
	# 		jeff.race_prediction.notnull())]
	jongmin = filter_gr_df(jongmin, cutoff_year, gr_wanted_cols)
	jaemin = filter_gr_df(jaemin, cutoff_year, gr_wanted_cols)

	gr_df = pd.concat(
		[haley, jeff, michelle, matthew, jaemin, jongmin], ignore_index = True)
	gr_df['gender_prediction'] = [
		x.upper() for x in gr_df.gender_prediction]
	gr_df['race'] = gr_df.apply(recode_race, axis = 1)

	assert len(aff_df) == len(gr_df), 'aff_df and gr_df do not have the same number of rows!'
	assert set(aff_df.authorID) == set(gr_df.authorID), 'authorID in aff_df and gr_df differ!'

	df = pd.merge(aff_df, gr_df, on = 'authorID')
	df.to_csv(AUTHORID_WITH_VARS, index = False)
