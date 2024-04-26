"""get predictions for gender, race, and affiliations

Note on 2022-07-26: I am no longer using this file because although it's convenient and cool to
complete all tasks in one script, this may come with some prices. For example, every time I want to 
re-arrange the column order in the output, I need to run the whole thing again, which involves gender
prediction, which has a limit on how many names I can predict. 

Therefore, I decided to split this script into several small steps so that I don't need to run the 
previous parts again if I only want to change the final output. 
"""

import sys
import pandas as pd
import numpy as np
import re
from genderize import Genderize
from ethnicolr import census_ln, pred_census_ln

ICA_AUTHOR_DATA = sys.argv[1]
AUTHOR_WITH_PRED = sys.argv[2]

def get_firstname_list(AUTHOR_DATA):
	"""
	Purpose:
		get the deduplicated list of all author first names
		remove nan from the list
	Input:
		author df
	Oputput:
		firstname as a list
	"""
	firstname = list(set(AUTHOR_DATA.firstName))
	firstname_list = [x for x in firstname if str(x) != 'nan']
	return firstname_list 


def get_firstname_df(FIRSTNAME_LIST):
	'''
	Purpose:
		get the gender prediction from genderize.io
		put the results into a dataframe
	Input:
		deduplicated author firstname list
	Output:	
		a dataframe containing author first name, gender prediction
			prediction probability, and prediction basedon
	'''
	API_KEY = '486f33235ec473d0d2ceef6273dca789'
	genderize = Genderize(
		user_agent='GenderizeDocs/0.0',
		api_key=API_KEY,
		timeout=5.0)
	name_gender_results = genderize.get(FIRSTNAME_LIST)
	firstname_df = pd.DataFrame(name_gender_results)
	firstname_df.columns = [
		'firstName', 
		'genderize', 
		'genderize_prob', 
		'genderize_basedon'
	]
	return firstname_df

def get_low_accuracy_names(FIRSTNAME_DF):
	'''
	'''
	low_accuracy_names_df = FIRSTNAME_DF[
		(FIRSTNAME_DF.genderize_basedon.astype(int) <= 2000) | 
		(FIRSTNAME_DF.genderize_prob.astype(float) <= 0.80)
	]
	low_accuracy_names = low_accuracy_names_df.firstName.tolist()
	return low_accuracy_names

def merge_gender_df(FIRSTNAME_DF, AUTHOR_DATA, LOW_ACCURACY_NAMES):
	'''
	Purpose:
		merge the firstname_df with the AUTHOR_DATA
		get the column of 'genderAccuracy'
	Input:
		firstname_df, AUTHOR_DATA
	Output:
		authorWithGender
	'''
	authorWithGender = AUTHOR_DATA.merge(
		FIRSTNAME_DF, 
		on = "firstName", 
		how = "left"
	)
	authorWithGender['genderAccuracy'] = np.where(
		authorWithGender.firstName.isin(LOW_ACCURACY_NAMES),
		'Low',
		'High'
	)
	return authorWithGender

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

if __name__ == '__main__':
	author_data = pd.read_csv(ICA_AUTHOR_DATA)
	firstname_list = get_firstname_list(author_data)
	firstname_df = get_firstname_df(firstname_list)
	low_accuracy_names = get_low_accuracy_names(firstname_df)
	authorWithGender = merge_gender_df(
		firstname_df, author_data, low_accuracy_names
	)
	race_pred = get_race_pred(authorWithGender)
	race_pred.to_csv(AUTHOR_WITH_PRED, index=False)

	
