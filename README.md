# ICA AUTHORS

This project contains my codes to scrape ICA Annaual conference data and also some exploratory codes about ICA journal data from web of science and also openalex. 

<!-- ## TODO!

- In `2022-12-08-check-authors-without-only-initials.ipynb`, I found one author without first name. I need to remove that paper `10.1111/j.1460-2466.1980.tb02015.x` and the two authors
- There are 157 authors scattered in 70 papers whose first names are initials only. -->

## Notebooks

These are exploratory notebooks

## Figures

Those are figures used in our paper.

## Workflow

This project uses snakemake.

### Workflow notebooks

These are notebooks used for the workflow. 
 
### Scripts

(More details can be found in `workflow/Snakefile` and also in each specific `py` file)

- `scrape_ica_paper_dois.py`: obtain ICA publication paper info (dois, title, and abstracts) from the official websites of the five ICA journals we analyze. For example, [https://academic.oup.com/joc/issue](https://academic.oup.com/joc/issue).

- `scrape_ica_author_data.py`: get paper and author data from each ICA journal publication

- `get_author_with_gender.py`: get gender raw predictions. This is to prevent me from having to do it again, which requires quota from genderize.io.

- `get_author_with_pred_raw.py`: get race and affiliations. "Raw" because I'll change column order later

- `get_author_with_pred.py`: rearrange colomn order

- `get_paper_and_author_with_type.py`: add 'type' to paper df and author data, and subsequently get research paper/author, and authors/papers to study. 

- `get_authorid_with_vars.py`: in this script, I processed the gender, race and aff coded data
and return basically dictionaries through a dataframe. 

- `get_authors_and_papers_expanded.py`: get all variables needed in analysis.

- `get_gscholar_data.py` and `get_gscholar_data_combined.py`: get gscholar data.

## Data

### Raw

- `/large/ror.json` is too large and therefore ignored here. You can get the most updated ROR data dump from Zenodo at [https://zenodo.org/communities/ror-data](https://zenodo.org/communities/ror-data).

<!-- `to_delete_dois.csv`: these are the non-research papers that I need to delete. The categories that they belong to are considered to be "research", just that they are the first papers that introduce other papers in the issue and therefore should be deleted. 

`category-classification.csv` is the result category classification directly from Google Sheet.  -->

### Plots

These data were created in the notebook of "Analysis_and_Plotting_2022-10-28-Analyze-Colla-Flows.ipynb". 

Datasets here are used to generate Figure 6 & 7 in the paper. 

### Interim

- `ica_paper_df.csv`, this file mainly contains dois for ica journal papers. I also included all other necessary information when it exists, for example, issue, and abstract. 

- `ica_paper_data.csv`, this file is created when I scrape each paepr individually. It in fact does not contain any other useful information than in `ica_paper_df.csv`. It contains publication data, that might be the only useful thing. It only contains paperType but it seems all of them are 'ScholarlyArticle'. It also has 'keywords' but I am not sure where that data is from. 

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

- `gender_race_result`: this is pretty important as it contains the final result of gender and race (manual) coding

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

Then, after all the manual coding is done (race, gender, and aff), I generated `authorid_with_vars.csv`, i.e., author ID with the associated aff country, aff type, gender, and race.

Finally, I generated:

- `authors_to_study_expanded.csv`
- `papers_to_study_expanded.csv`

Those two files are the most complete ones.

- `gscholar_data_combined.csv`, this is the final google scholar data. For details of how I got this data, see the section of "Google scholar data".

## Misc.

### About Google Scholar data

I scraped citation data from Google Scholar. I queried title + journal + first author name. I then compared the original title and the title shown on Google Scholar to make sure my data is accurate. Among all 5,718 papers (The full dataset contains 5719 papers, so `10.1111/j.1083-6101.1996.tb00178.x` is missing in gscholar data. I dind't know what happened.), onåly 293 papers have differences in titles. I then investigated these 293 papers. I compared the similarity (using python's difflib) between the two titles. More than half of them have a similarity score of 0.95. For these, I considered them as accurate. For the 122 papers, I collected their data on Google Scholar by searching their DOIs (instead of titles). In this case, searching by DOI yeilds a much better result (`data/interim/gscholar_data_manual.csv`). Still, there are some mismatches. I updated this dataset in https://docs.google.com/spreadsheets/d/14y72p5I9RvzueNOb5x1cE23M0N__A8rCaCRudckxU5U/edit#gid=1256132535 (or see `google_sheets/gscholar_manual.xlsx`). The resulting data is `interim/gscholar_data_manual_checked.csv`

Then, I combined the two datasets through `combine_gscholar_data.py`

>I thought about redoing scraping google scholar citation data by searching the DOI (right now, the majority of the data came from searching the title). However, after checking the result of data now (trying searching DOI for papers with strings like `[PDF]` and `CITATION`), I found that they are the same. So I probably won't do it again; I'll keep the data for now for my analysis.   

#### Redoing GScholar data on 2023-06-07

I scraped citation data from Google Scholar. I queried title + journal + first author name. I then compared the original title and the title shown on Google Scholar to make sure my data is accurate. Among all 5,718 papers `10.1111/j.1083-6101.1996.tb00178.x` is missing in gscholar data. This is because one paper happend twice in the gscholar data. But I dind't know what happened. Only 289 papers have differences in titles. I then investigated these 289 papers. I compared the similarity (using python's difflib) between the two titles. More than half of them have a similarity score of 0.95. For these, I considered them as accurate. For the 123 papers, I collected their data on Google Scholar by searching their DOIs (instead of titles). Note that '10.1111/j.1460-2466.1952.tb00171.x' is not available on Google Scholar so I had to remove it. 

I then manually checked these results at https://docs.google.com/spreadsheets/d/14y72p5I9RvzueNOb5x1cE23M0N__A8rCaCRudckxU5U/edit#gid=261290178 (or see `google_sheets/gscholar_manual_2.xlsx`). There, I added 10.1111/j.1083-6101.1996.tb00178.x. These results are at `data/interim/gscholar_data_manual.csv`

In all, these papers are not availabe on google Scholar:
 - 10.1111/j.1460-2466.1977.tb02133.x
 - 10.1111/j.1460-2466.1952.tb00171.x

Then, I combined the two datasets through `combine_gscholar_data.py`. The final dataset should contain 5717 papers. 

### Classification and Inter-coder reliability

#### Paper classification ICR

First, with `2022-08-20-new-cat-issueurl.ipynb`, we get the list of all categories with associated frequencies. Then in this the dataset, we reclassified categories: https://docs.google.com/spreadsheets/d/1E2dgJCpv5FrxKv41QZuNsv7MjJs3IcBxFbZze_5rnjU/edit#gid=2060805888 (or see `data/interim/cat_class_raw.csv`)

After we classified these categories as either "to exclude" or not, I put the raw result into `data/interim/cat_class_raw.csv`

- `data/interim/icr/paper_classification_icr_test_2022-08-27.csv` is the randomly selected 100 rows to test paper classification intercoder reliability. This dataset is generated by `2022-08-27-GET-100-random-papers-to-classify-types-for-ICR.ipynb`. 

<!-- - This is the raw result: https://docs.google.com/spreadsheets/d/1POuzorD6B2r8uO9gdpBgt1U1ZksJhbCTzaolnAKQpmU/edit#gid=1585704198 -->

- `interim/icr/paper_cla_ica_compa_results_2022-08-29.csv` is the aggregated results. This result is computed by `2022-08-29-calculate-paper-cla-icr.ipynb`. Krippendorff alpha: 0.831

- Then, We did all the classification here: https://docs.google.com/spreadsheets/d/1uslTqfe269jf0KHJ8E70XHru2jag8y-iiRRb94HQA9s/edit#gid=349722970 (or see data sheets in the folder of `interim/paper_classification_task`), which is created by `2022-08-29-randomly-split-ica-paper-df-for-paper-classification.ipynb`

<!-- - We tested final icr here: https://docs.google.com/spreadsheets/d/1KvPvm5DWAP9ndPbB4yfEWyet5WIu0rfKsqM_FL2kbP8/edit?usp=sharing (or see `interim/icr/paper_classification_final_icr_agg_result.csv`)
  - This is created by `2022-09-12-GET-100-random-papers-to-classify-types-for-final-ICR.ipynb`
  - Result: `2022-09-13-calculate-paper-classification-final-icr.ipynb`. 
  - Final ICR: .79 -->

<!-- ## with type

- With `2022-09-14-get-paper-and-author-with-type.ipynb`, I add `type` to ica paper df and author data with pred. I also outputed research paper df and research author with pred.  -->

#### race and gender 

- With `2022-09-14-get-100-names-for-initial-gender-race-icr.ipynb`, I randomly selected 100 names for initial icr for race and gender. 

<!-- - This is where they coded: https://docs.google.com/spreadsheets/d/1ZgDutpqsO23PqssScUaACHdWuu32mzO1SmNOkbsq-jA/edit#gid=112686513 (or see `interim/icr/gender_initial_icr_results.csv`).  -->

- Here is the aggregated results for initial gender coding: https://docs.google.com/spreadsheets/d/1ZgDutpqsO23PqssScUaACHdWuu32mzO1SmNOkbsq-jA/edit#gid=1431889162 (or see `interim/icr/gender_initial_icr_results.csv`).

<!-- And there is the data for Matthew: https://docs.google.com/spreadsheets/d/1VS7iTtfS640PA56o8DnPh3DJm4Dx5UJfubvkbXd7IwI/edit#gid=0 I put it separately here because in the above url, we have all people's data but Matthew created a new sheet for that. -->

- I calculated race and gender ICR in `2022-09-19-calculate-initial-gender-icr.ipynb`.The initial gender ICR is 0.94. 

<!-- ### Post ICR

- With `2022-12-02-get-100-names-for-final-gender-race-icr.ipynb`, I obtained 100 names for final ICR for gender and race. Resulting data is `data/interim/icr/2022-12-02-race-gender-post-icr-100names.csv`

- This is where they coded:  -->

##### Redo Race

- Gender is okay but we need to redo race. Now I used `2022-09-20-get-100-names-for-race-icr.ipynb` to get another 100 random names for race ICR. 

- Here is the aggregated result after coding: https://docs.google.com/spreadsheets/d/1Fe_w078ZxqOV8HxmjuqJav5ff-PM4bElJr9CgSwZHHw/edit#gid=1729958890 (or see `interim/icr/race_initial_icr_results.csv`).

<!-- Here is where we coded the race: https://docs.google.com/spreadsheets/d/1Fe_w078ZxqOV8HxmjuqJav5ff-PM4bElJr9CgSwZHHw/edit?usp=sharing -->

- I calculated the ICR here: `2022-09-23-calculate-initial-race-icr.ipynb`. The initial ICR is 0.91. 

### ACTUAL CODING

#### author affiliation

With `2022-09-16-split-aff-task.ipynb` I split the dataset. Here is where we coded: https://docs.google.com/spreadsheets/d/1DA7EZ1SmvdaMihPzNqcp1aHmZ_N6PQpxB5YUjI_jNoY/edit#gid=393854720 (or see `interim/aff_results`.)

#### Gender and Race

I did it here: `2022-09-23-split-race-gender-task.ipynb`. There datasets are deposited in `data/interim/gender_race_coding_task`

Note that I found one person who uses anonymous name: https://academic.oup.com/ct/article/8/4/381/4201775. I then updated the script of `get_paper_and_author_with_type.py` in the workflow. Now this issue is solved. 

There are 84 scholars whose first name is initials only. With `2022-12-09-create-initials_df.ipynb`, I created a spreadsheet for coders to check the results. 



