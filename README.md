# TwitterExtractionFashionProject
Scripts for extracting tweets for a friend's Phd Project on fashion tweets and saving locally. This process can be used for extracting files from any accounts, within the Twitter api limits. Their limits include certain number of extractions, then there is wait time of 15 minutes, besides connection errors, which can happen for a number of reasons. Some of them, though, are treated in the code by an argument that retries in case they happen.

For this process to work, you must obtain a developer license for twitter (https://developer.twitter.com/en/apply-for-access) and obtain four credentials to fill in into the credentials.csv file inside the credentials folder.

# Potential issues to be improved
- All files per month are created, necessarily, before the full extraction.
