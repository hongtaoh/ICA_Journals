"""get the dataframe to check for all issues containing the categories to keep """

import pandas as pd
from collections import Counter
import sys

CAT_CLASSIFICATION = sys.argv[1]
ICA_PAPER_DF = sys.argv[2]
CAT_KEEP_TO_CHECK = sys.argv[3]

if __name__ == '__main__':
	cat_issues = pd.read_csv(CAT_CLASSIFICATION)
	cats_to_keep = cat_issues[cat_issues.TO_EXCLUDE == False].category

	df = pd.read_csv(ICA_PAPER_DF)
	df_keep = df[df.category.isin(cats_to_keep)]

	dedup_issue_cat = df_keep[['issueURL', 'category']].drop_duplicates(
		).reset_index(drop=True)

	counter = Counter(dedup_issue_cat.category)
	repeated_cats = [k for k,c in dict(counter.items()).items() if c > 1]

	cats_keep_to_check = dedup_issue_cat[dedup_issue_cat.category.isin(repeated_cats)].reset_index(
		drop = True)[['category', 'issueURL']].sort_values(
		'category')

	print(cats_keep_to_check.shape)

	cats_keep_to_check.to_csv(CAT_KEEP_TO_CHECK)

