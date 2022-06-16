# TwitterExtractionFashionProject

Scripts for extracting tweets for a friend's Phd Project on fashion tweets and saving locally. This process can be used for extracting files from any accounts, within the Twitter api limits. Their limits include certain number of extractions, then there is wait time of 15 minutes, besides connection errors, which can happen for a number of reasons. Some of them, though, are treated in the code by an argument that retries in case they happen.

For this process to work, you must obtain a developer license for twitter (https://developer.twitter.com/en/apply-for-access) and obtain four credentials to fill in into the credentials.csv file inside the credentials folder.

## To run the project

The first step is to obtain the twitter credentials and fill in the csv file, which is just a template.

The whole process can be run by executed **main.py**, after the required libraries are installed. It extracts the tweets in two steps (because of API limitations) and then converts all extracted csv files into txt files with a specific format. The identification is kept as well.

The script **twitter_save_each_csv_as_txt** is similar to main.py but includes only the conversion (the rest is commented).

The whole process might take more than 1 hour, including the API wait time of 15 minutes each time, but the script simply pauses and continues until the end.

# Potential issues to be improved

- All files per month are created, necessarily, before the full extraction.
