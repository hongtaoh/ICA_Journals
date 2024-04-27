# ICA Journals

## Data

### papers_to_study_expanded.csv

This data contains information about each paper article. 

1. **journal**: The name of the journal where the paper is published.
2. **issueURL**: The URL to the journal issue containing the paper.
3. **volumn**: The volume of the journal in which the paper appears.
4. **issue**: The specific issue of the journal in which the paper is published.
5. **issueText**: Description of the issue, usually includes the month, year, and page numbers.
6. **month**: The month when the journal issue was published.
7. **year**: The year when the journal issue was published.
8. **category**: Category of the content, e.g., Articles, Reviews.
9. **title**: The title of the paper.
10. **url**: URL to the specific paper.
11. **cross_gender_race_and_country**: Boolean indicating if the paper involves cross-gender, race, and country analysis.
12. **numberOfAuthors**: The number of authors of the paper.
13. **first_author_gender**: The gender of the first author.
14. **first_author_race**: The race of the first author.
15. **first_author_country**: The country of the first author.
16. **first_author_afftype**: The type of affiliation of the first author (i.e., Education, Non-Education).
17. **with_us_authors**: Boolean indicating if there are U.S. authors involved.
18. **cross_race_details**: Details about the race diversity among the authors.
19. **cross_gender_details**: Details about the gender diversity among the authors.
20. **gscholar_citation**: The number of citations the paper has according to Google Scholar.

### authors_to_study_expanded.csv

1. **authorIndex**: author index
2. **year**: the year when the paper associated with this paper was published
3. **journal**: the journal where the paper associated with this paper was published
4. **authorPosition**: author position
5. **countrypred**: which country was this author based when the paper was published
6. **genderpred**: gender of this author
7. **racepred**: race of this author
8. **afftypepred**: the affiliation type of this author's affiliation when the paper was published.

### author_chord_gr_from_firstauthors.csv 

This is data for Figure 7. 

### cntry_chord_from_firstauthor.csv

This is data for Figure 6. 

## Figures

Those are the figures in our study. 

## Replication

To replicate our study, you'll need our scripts to crawl, process, and analyze data. 

### Crawling and Processing data 

We used snakemake to automate the crawling and processing. The folder of `workflow/scripts` contains the scripts and the file of `workflow/Snakefile` specifies the details. 

**PLEASE NOTE THAT SINCE UNNECESSARY FILES AND DATA CONTAINING AUTHOR IDENTIFICATION INFO HAVE BEEN DELETED, THE SNAKEFILE IS NO LONGER EXECUTABLE. HOEWVER, YOU CAN STILL USE THE FOLLOWING SCRIPTS INDIVIDUALLY BY YOURSELF IF YOU DECIDE TO SCRAP THE PUBLIC ICA JOURNAL AND AUTHOR DATA.**

- `scrape_ica_paper_dois.py`: obtain ICA publication paper info (dois, title, and abstracts) from the official websites of the five ICA journals we analyze. For example, [https://academic.oup.com/joc/issue](https://academic.oup.com/joc/issue).

- `scrape_ica_author_data.py`: get paper and author data from each ICA journal publication

- `get_author_with_gender.py`: get gender raw predictions. This is to prevent me from having to do it again, which requires quota from genderize.io.

- `get_author_with_pred_raw.py`: get race and affiliations. "Raw" because I'll change column order later

- `get_author_with_pred.py`: rearrange colomn order

- `get_paper_and_author_with_type.py`: add 'type' to paper df and author data, and subsequently get research paper/author, and authors/papers to study. 

- `get_authorid_with_vars.py`: process the gender, race and aff coded data and return basically dictionaries through a dataframe. 

- `get_authors_and_papers_expanded.py`: get all variables needed in analysis.

- `get_gscholar_data.py` and `get_gscholar_data_combined.py`: get gscholar data.

### Analyzing data

All replicable and executable notebooks for our data analysis are available at the folder of `Analaysis_and_Plotting`. 

**NOTE THAT THE NOTEBOOK OF `Methods.ipynb` IS NOT EXECUTABLE AS THE DATA USED THERE WAS REMOVED TO PROTECT THE PRIVACY OF AUTHORS ANALYZED.** 