# ICA Journals

## Data

### Raw

- `/large/ror.json` is too large and therefore ignored here. You can get the most updated ROR data dump from Zenodo at [https://zenodo.org/communities/ror-data](https://zenodo.org/communities/ror-data).

### Plots

These data were created in the notebook of "Analysis_and_Plotting/2022-10-28-Analyze-Colla-Flows.ipynb". 

Datasets there are used to generate Figure 6 & 7 in the paper. 

### Interim

- `ica_paper_df.csv`, this file mainly contains dois for ica journal papers. I also included all other necessary information when it exists, for example, issue, and abstract. 

- `ica_paper_data.csv`, this file is created when I scrape each paper individually. It in fact does not contain any other useful information than in `ica_paper_df.csv`. It contains publication data, that might be the only useful thing. It only contains paperType but it seems all of them are 'ScholarlyArticle'. It also has 'keywords' but I am not sure where that data is from. 

- `ica_author_data.csv`: this is the scraped author data, which contains author names/positions and affiliations. 

- `ica_error_urls.txt`: this is the log of unavailable urls when scraping paper and author data. 

- `cat_issueURL_new.csv`: we obtained the list of all categories (e.g., Article, Intercom, Review Essays, etc.) with associated frequencies. For categories with a frequency of over 1, we only excluded those that are ABSOLUTELY non-research. For categories that only appeared once, I checked all of them. 

- `cat_class_raw.csv`: this is the result of our above mentioned checking. Basically, we added a column of `to exclude`. If a categoris is `to exclude`, we classify papers published with those categories as NON-RESEARCH. for others, we mannually coded them (after making sure our initial ICR is alright.)

- `author_with_gender.csv`: this is the result of `get_author_with_gender.py`. This data contains author gender prediction from genderize.io

- `author_with_pred_raw.csv`: this is the result of `get_author_with_pred_raw.py`. I obtained race and aff predictions as well (besides gender). I named it "raw" and put it in `interim` folder rather than `processed` because I'll process this data later. 

- `gscholar_data_manual.csv`: I obtained google scholar data through DOI search for 122 papers. Please see the section of "Google scholar data" for details.

- `gscholar_data_manual_checked.csv`: I manually checked & updated `gscholar_data_manual.csv`. Please see the section of "Google scholar data" for details.

#### Folders 

- `paper_classification_task`: The source files for three authors to code the paper classifcation. 

- `icr`: contains all files for intercoder reliability testing

- `gender_race_result`: this is pretty important as it contains the final result of gender and race (manual) coding. **NOTE THAT WE INTENTIONALLY DELETED THESE FILES FOR PRIVACY CONCERNS.**

- `gender_race_coding_task`: this is the source file for gender and race coding task. 

- `aff_task`: affiliation coding task source files

- `aff_result`: affiliation coding final results

- `api_reliance_checking`

  - `113_names_for_api_reliance_checking.csv`: I randomly selected 113 names from the final dataset of 11292 authors for one author to check how reliant we are on the automatic results from API. This is the result of `notebooks/workflow/workflow-notebooks/2023-02-10-get-113-names-to-see-reliance-on-api-automatic-results.ipynb`. Haley hand coded these 113 names and the result is in `113_names_for_api_reliance_checking_result.csv`.

### Processed

I first get `author_with_pred.csv`. Then the following:

- `ica_paper_df_with_type.csv`, type means research paper or not
- `author_with_pred_with_type.csv`, type means research paper or not
- `research_paper_df.csv`, papers that are research papers
- `research_author_with_pred.csv`, authors of research papers with all kinds of predictions (race, gender, aff)
- `authors_to_study.csv`, this is different from research authors because I removed those research papers whose affiliation is NaN
- `dois_to_study.csv`, research papers with valid aff information
- `papers_to_study.csv`, research papers with valid affiliation information

Then, after all the manual coding is done (race, gender, and aff), I generated `authorid_with_variables.csv`, i.e., author ID with the associated aff country, aff type, gender, and race. **NOTE THAT WE INTENTIONALLY DELETED THESE FILES FOR PRIVACY CONCERNS.**

Finally, I generated:

- `authors_to_study_expanded.csv` **NOTE THAT WE INTENTIONALLY REMOVED IDENTIFICATION INFORMATION FOR PRIVACY CONCERNS.**
- `papers_to_study_expanded.csv`

Those two files are the most complete ones.

- `gscholar_data_combined.csv`, this is the final google scholar data. For details of how I got this data, see the section of "Google scholar data".
