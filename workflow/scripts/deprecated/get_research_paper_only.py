"""with this script, I tries to get two files: ica_paepr_df_with_type, and 
	research_author_with_pred. The first one adds one column to the original ica_paper_df,
	i.e., type ('R' (research), or 'M' (Miscellaneous))

	The research_author_with_pred is only a subset of the original author_with_pred. I 
	only chose those who wrote research papers. 

"""

import sys
import pandas as pd
import numpy as np
import re 

CAT_CLASSIFICATION = sys.argv[1]
DOIS_TO_DELETE = sys.argv[2]
DOIS_TO_KEEP = sys.argv[3]
ICA_PAPER_DF = sys.argv[4]
AUTHOR_WITH_PRED = sys.argv[5]

ICA_PAPER_DF_WITH_TYPE = sys.argv[6]
RESEARCH_AUTHOR_WITH_PRED = sys.argv[7]

if __name__ == '__main__':
	### categories to exclude
	cat_df = pd.read_csv(CAT_CLASSIFICATION)[
		['category', 'issueURL', 'TO_EXCLUDE']
	]
	to_exclude_cat = cat_df[cat_df.TO_EXCLUDE == True][
		'category']
	num_to_exclude_cat = len(to_exclude_cat)
	print(f'There are {num_to_exclude_cat} categories to exclude.')

	### DOIS to keep
	dois_to_keep = pd.read_csv(DOIS_TO_KEEP, header = None).iloc[:,0]
	print(f'There are {len(dois_to_keep)} dois to keep')

	## TO EXCLUDE DOIS 1
	papers = pd.read_csv(ICA_PAPER_DF)
	to_exclude_dois_1 = papers[
		(papers.category.isin(to_exclude_cat)) & (
			~papers.doi.isin(dois_to_keep))].doi.tolist()
	print(f'There are {len(to_exclude_dois_1)} dois to exclude')

	### to exclude dois 2
	to_exclude_dois_2 = pd.read_csv(DOIS_TO_DELETE, header=None).iloc[:, 0]
	to_exclude_dois_2 = [
		re.sub('https://doi.org/', '', x) for x in to_exclude_dois_2]
	print(f'There are {len(to_exclude_dois_2)} dois to exclude')

	### DOIS to delete all
	to_exclude_dois_all = to_exclude_dois_1 + to_exclude_dois_2
	print(f'There are in total {len(to_exclude_dois_all)} dois to delete')

	### Process papers
	papers['type'] = np.where(
		papers.doi.isin(to_exclude_dois_all), 
    	'M', 
    	'R')
	print(f'papers shape: {papers.shape}')
	research_papers = papers[papers.type == 'R']
	print(f'research papers shape: {research_papers.shape}')
	papers.to_csv(ICA_PAPER_DF_WITH_TYPE, index=False)

	### Process authors
	research_paper_dois = research_papers.doi 
	authors = pd.read_csv(AUTHOR_WITH_PRED)
	print(f'Authors shape: {authors.shape}')
	research_authors = authors[authors.doi.isin(research_paper_dois)]
	print(f'Research authors shape: {research_authors.shape}')

	missing_author_info = research_authors[
		research_authors.numberOfAuthors.isnull()]
	print(f'{len(missing_author_info)} authors do not even have info for num of authors')
	research_authors = research_authors[
		research_authors.numberOfAuthors.notnull()]
	research_authors.to_csv(
		RESEARCH_AUTHOR_WITH_PRED, index=False)
	