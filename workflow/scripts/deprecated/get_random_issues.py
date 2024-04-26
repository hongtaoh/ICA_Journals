"""get 50 random issueURLs to check the frequency of special issues """

import pandas as pd
import random 
import sys

ICA_PAPER_DF = sys.argv[1]
RANDOM_ISSUES = sys.argv[2]

num_of_random_issues = 50

if __name__ == '__main__':
	df = pd.read_csv(ICA_PAPER_DF)
	dedupped_issues = list(set(df.issueURL))
	dedupped_issues.sort()
	print(f'There are {len(dedupped_issues)} issues.')
	random.seed(1234)
	random_issues = random.sample(dedupped_issues, num_of_random_issues)

	with open(RANDOM_ISSUES, 'w') as f:
		for issue in random_issues:
			f.write("%s\n" % issue)

