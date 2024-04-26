"""add 'type' to paper_df and author_data

In this scripe, I outputed a lot of stuff, including authors to study
and papers to study. See Snakefile for details

"""

import sys
import pandas as pd
import numpy as np

PAPER_CLASSIFICATION_HONGTAO = sys.argv[1]
PAPER_CLASSIFICATION_JEFF = sys.argv[2]
PAPER_CLASSIFICATION_KRISTEN = sys.argv[3]
ICA_PAPER_DF = sys.argv[4]
AUTHOR_WITH_PRED = sys.argv[5]
ICA_PAPER_DF_WITH_TYPE = sys.argv[6]
AUTHOR_WITH_PRED_WITH_TYPE = sys.argv[7]
RESEARCH_PAPER_DF = sys.argv[8]
RESEARCH_AUTHOR_WITH_PRED = sys.argv[9]
AUTHORS_TO_STUDY = sys.argv[10]
DOIS_TO_STUDY = sys.argv[11]
PAPERS_TO_STUDY = sys.argv[12]

if __name__ == '__main__':
	hongtao = pd.read_csv(PAPER_CLASSIFICATION_HONGTAO)
	jeff = pd.read_csv(PAPER_CLASSIFICATION_JEFF)
	kristen = pd.read_csv(PAPER_CLASSIFICATION_KRISTEN)
	hongtao_r = hongtao[hongtao.type == 1].doi.tolist()
	jeff_r = jeff[jeff.type == 'R'].doi.tolist()
	kristen_r = kristen[kristen.type == 'R'].doi.tolist()
	print('set of type:\n')
	set(hongtao.type), set(jeff.type), set(kristen.type)
	print('number of research papers:\n')
	len(hongtao_r), len(jeff_r), len(kristen_r)
	all_r = hongtao_r + jeff_r + kristen_r

	# paper with type
	paper = pd.read_csv(ICA_PAPER_DF)
	paper['year'] = np.where(paper.year == 'Progress)', '2022', paper.year)
	paper['type'] = np.where(paper.doi.isin(all_r), 'R', 'M')
	paper.to_csv(ICA_PAPER_DF_WITH_TYPE, index = False)

	# author with type
	author = pd.read_csv(AUTHOR_WITH_PRED)
	author['year'] = np.where(author.year == 'Progress)', '2022', author.year)
	author['type'] = np.where(author.doi.isin(all_r), 'R', 'M')
	author.shape, author[author.type=='R'].shape
	author.to_csv(AUTHOR_WITH_PRED_WITH_TYPE, index = False)
	paper[paper.type == 'R'].to_csv(RESEARCH_PAPER_DF, index=False)
	author[author.type == 'R'].to_csv(RESEARCH_AUTHOR_WITH_PRED, index=False)

	## papers to study and authors to study
	dois_to_exclude = list(set(
		author[(author.type =='R') & (author['affiliation.2'].isnull())].doi))
	dois_to_study = [x for x in all_r if x not in dois_to_exclude]
	papers_to_study = paper[paper.doi.isin(dois_to_study)]
	authors_to_study = author[author.doi.isin(dois_to_study)]
	authors_to_study.to_csv(AUTHORS_TO_STUDY, index=False)
	with open(DOIS_TO_STUDY, 'w') as f:
		for doi in dois_to_study:
			# %s mean adds s, but what is s? that after the second %
			f.write("%s\n" % doi)
	papers_to_study.to_csv(PAPERS_TO_STUDY, index=False)
	print(f'authors shape:  {authors_to_study.shape}')
	print(f'papers shape:  {papers_to_study.shape}')




