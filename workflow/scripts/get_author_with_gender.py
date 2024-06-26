"""get predictions for gender. I make this step seperate because there is a rate limit for genderize.io.

I only need to run this script once and later no matter what changes I want to make, the gender 

predictions stay the same and can be found in gender_with_author.csv. 

"""

import sys
import pandas as pd
import json
import numpy as np
import requests
import re
from genderize import Genderize

ICA_AUTHOR_DATA = sys.argv[1]
AUTHOR_WITH_GENDER = sys.argv[2]

def get_firstname_list(AUTHOR_DATA):
	"""
	Purpose:
		get the deduplicated list of all author first names
		remove nan and '' from the list
	Input:
		author df
	Oputput:
		firstname as a list
	"""
	firstname = list(set(AUTHOR_DATA.firstName))
	firstname_list = [x for x in firstname if str(x) != 'nan' and x != '']
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

if __name__ == '__main__':
	author_data = pd.read_csv(ICA_AUTHOR_DATA)
	firstname_list = get_firstname_list(author_data)
	firstname_df = get_firstname_df(firstname_list)
	low_accuracy_names = get_low_accuracy_names(firstname_df)
	authorWithGender = merge_gender_df(
		firstname_df, author_data, low_accuracy_names
	)
	authorWithGender.to_csv(AUTHOR_WITH_GENDER, index=False)
