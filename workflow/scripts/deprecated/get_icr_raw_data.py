"""get 200 random rows to check intercoder reliability """

import pandas as pd
import sys

RESEARCH_AUTHOR_WITH_PRED = sys.argv[1]
ICR_RAW_DATA = sys.argv[2]

if __name__ == '__main__':
	df = pd.read_csv(RESEARCH_AUTHOR_WITH_PRED)
	df_icr = df.sample(200, random_state = 1234)
	df_icr.to_csv(ICR_RAW_DATA, index=False)


