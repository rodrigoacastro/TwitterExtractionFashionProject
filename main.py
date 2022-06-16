# Script to automate tweeter extractions of fashion tweets
# Extraction done in two parts because the API has limitations

import time
# extracting tweets and saving in the "extracted_tweets" folder - first part
from twitter_extraction_Fashion_part1 import *

time.sleep(900) # Sleep for 900 seconds (15 minutes)

# extracting tweets and saving in the "extracted_tweets" folder - second part
from twitter_extraction_Fashion_part2 import *

# saving each tweet in a text file in the "extracted_tweets_txt_files" files
from create_txt_files_per_tweet import *

print("\n")
print ("All Files extracted and all tweets saved as txt files according to the template.")