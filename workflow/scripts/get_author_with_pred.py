"""get author_with_pred, here, I simply re-arrange the column of author_with_pred_raw

"""

import sys
import pandas as pd
import urllib.parse

AUTHOR_WITH_PRED_RAW = sys.argv[1]
AUTHOR_WITH_PRED = sys.argv[2]

if __name__ == '__main__':
	df = pd.read_csv(AUTHOR_WITH_PRED_RAW)
	# This guy used an anonymous name: https://academic.oup.com/ct/article/8/4/381/4201775
	# I need to change it
	anonymous_name_index = df[df.authorFullName == ' Anonymous'].index[0]
	df.at[anonymous_name_index, 'authorFullName'] = 'Craig R. Scott'
	df.at[anonymous_name_index, 'firstName'] = 'Craig'
	df.at[anonymous_name_index, 'lastName'] = 'Scott'
	df.at[anonymous_name_index, 'genderize'] = 'male'
	df.at[anonymous_name_index, 'gscholarLink'] = 'https://scholar.google.com/scholar?hl=en&as_sdt=0%252C50&q=Craig+R.+Scott'
	# add a column called authorID
	df['authorID'] = df['doi'] + '+' + df['authorPosition'].astype(str)
	# add google search
	google_string = 'https://www.google.com/search?q='
	df['googleSearch'] = df.apply(
		lambda row: google_string + urllib.parse.quote_plus(
			str(row['authorFullName']) + ' ' + str(row['affProcessed'])), axis=1)

	cols_to_keep = [
		'authorID',
		'doi',
		'url',
		'year',
		'title',
		'journal',
		'numberOfAuthors',
		'authorPosition',
		'authorFullName',
		'firstName',
		'lastName',
		'affiliation',
		'gscholarLink',
		'googleSearch',
		'genderize',
		'genderize_prob',
		'genderize_basedon',
		'genderAccuracy',
		'authorFullName',
		'firstName',
		'lastName',
		'affiliation',
		'gscholarLink',
		'googleSearch',
		'race',
		'racePredAccuracy',
		'api',
		'black',
		'hispanic',
		'white',
		'raceHighest',
		'raceSecondHighest',
		'raceDiff',
		'affProcessed',
		'affiliation',
		'ROR_AFFNAME',
		'matchMethod',
		'ROR_ID',
	]

	df[cols_to_keep].to_csv(
		AUTHOR_WITH_PRED, index=False)
