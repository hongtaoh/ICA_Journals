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
INITIAL_DF = sys.argv[10]
AUTHORID_WITH_VARS = sys.argv[11]

def subset_aff_df(source):
	'''subset aff results

	INPUT:
		- source: either HONGTAO_AFF_RESULT, or KRISTEN_AFF_RESULT

	OUTPUT:
		- a dataframe
	'''
	df = pd.read_csv(source)
	df = df[['authorID', 'country_code', 'aff_type', 'ROR_ID']]
	return df 

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
	# 'University of Georgia'
	ror_cntry_dic['https://ror.org/02bjhwk41'] = 'US'

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
	elif row['aff_type'] == 1:
		new_afftype = 'Education'
	elif row['aff_type'] == 0:
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

def fill_gender(DF):
	'''if genderpred_api is nan, use gender_prediction; otherwise, use genderize result
	This is because Haley/Michelle wrote '1' if the result is the same as the API result

	Inputs:
		DF: either haley or michelle

	Output: 
		a numpy array
	'''
	genderpred = np.where(
		DF.genderpred_api.isnull(), DF["gender_prediction"], DF.genderize)
	genderpred[genderpred == 'female'] = 'F'
	genderpred[genderpred == 'male'] = 'M'
	return genderpred 

def fill_race(DF):
	'''if racepred_api is nan, use race_prediction; otherwise, use race automatic result
	This is because Haley/Michelle wrote '1' if the result is the same as the API result

	Inputs:
		DF: either haley or michelle

	Output: 
		a numpy array
	'''
	racepred = np.where(
		DF.racepred_api.isnull(), DF["race_prediction"], DF.race)
	racepred[racepred == 'api'] = 2
	racepred[racepred == 'hispanic'] = 3
	racepred[racepred == 'white'] = 0
	return racepred 

if __name__ == '__main__':

	######### AFF
	df1 = subset_aff_df(HONGTAO_AFF_RESULT)
	df2 = subset_aff_df(KRISTEN_AFF_RESULT)

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
	# to correct the results of Jaemin
	jaemin['gender_prediction'] = jaemin[
		'gender_prediction'].str.replace(' M', 'M')

	########### Upperclass Matthew's gender prediction coding
	matthew_upperclass_dict = {
		'm': 'M',
		'n': 'N',
		'f': 'F'
	}
	'''https://stackoverflow.com/a/68046167
	'''
	for old, new in matthew_upperclass_dict.items():
		matthew[
			'gender_prediction'] = matthew['gender_prediction'].str.replace(old, new, regex=False)

	######### Add Coder variable
	haley['Coder'] = 'Haley'
	matthew['Coder'] = 'Matthew'
	michelle['Coder'] = 'Michelle'
	jaemin['Coder'] = 'Jaemin'
	jongmin['Coder'] = 'Jongmin'
	jeff['Coder'] = 'Jeff'

	############ Fill gender and race result for Haley and Michelle
	haley['gender_prediction'] = fill_gender(haley)
	michelle['gender_prediction'] = fill_gender(michelle)
	haley['race_prediction'] = fill_race(haley)
	michelle['race_prediction'] = fill_race(michelle)

	######### Subset gender and race data
	gr_wanted_cols = [
		'Coder', 
		'firstName', 
		'genderize', 
		'authorID', 
		'doi', 
		'gender_prediction', 
		'race_prediction'
	]
	haley = haley[gr_wanted_cols]
	matthew = matthew[gr_wanted_cols]
	michelle = michelle[gr_wanted_cols]
	jongmin = jongmin[gr_wanted_cols]
	jaemin = jaemin[gr_wanted_cols]
	jeff = jeff[gr_wanted_cols]

	gr_df = pd.concat(
		[haley, michelle, matthew, jaemin, jongmin, jeff], ignore_index = True)

	### Check gender prediction null results
	first_try_nan = gr_df[gr_df.gender_prediction.isnull()]
	print(f'There are {first_try_nan.shape[0]} names that do have not gender prediction result, initially')

	########## Initial df
	initial_df = pd.read_csv(INITIAL_DF)
	# get the first try authorID and gender_prediction result
	authorid_gender_dict = dict(
		zip(gr_df.authorID, gr_df.gender_prediction))
	# get the initial df authorid gender prediction dict
	initial_df_authorid_gender_dict = dict(
		zip(initial_df.authorID, initial_df.gender_prediction))
	# update the original one
	authorid_gender_dict.update(initial_df_authorid_gender_dict)

	######## Update gr_df
	gr_df['gender_prediction'] = [
		authorid_gender_dict[x] for x in gr_df['authorID']]
	missing_gender_prediction = gr_df[gr_df.gender_prediction.isnull()]
	
	# print(f'There are {missing_gender_prediction.shape[0]} names that do not have gender prediction results in gr_df')
	gr_df['race'] = gr_df.apply(recode_race, axis = 1)

	assert len(aff_df) == len(gr_df), 'aff_df and gr_df do not have the same number of rows!'
	assert set(aff_df.authorID) == set(gr_df.authorID), 'authorID in aff_df and gr_df differ!'

	df = pd.merge(aff_df, gr_df, on = 'authorID')

	to_delete_dois = list(set(missing_gender_prediction.doi))
	to_keep_dois = list(set([x for x in df.doi.tolist() if x not in to_delete_dois]))
	to_delete_authors = df.query('doi == @to_delete_dois')
	to_keep_authors = df.query('doi == @to_keep_dois')

	print(f"""{missing_gender_prediction.shape[0]} people scattered in {len(to_delete_dois)} papers
		do not have gender predictions. So I had to delete all {len(to_delete_authors)} authors in these papers.
		The final result consists of {len(to_keep_authors)} authors scattered in {len(to_keep_dois)} papers. 
		""")

	to_keep_authors.to_csv(AUTHORID_WITH_VARS, index = False)
