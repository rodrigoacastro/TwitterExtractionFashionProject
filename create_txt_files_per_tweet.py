# write txt files according to template

# https://www.geeksforgeeks.org/reading-writing-text-files-python/

import pandas as pd
import os
from os import path
import glob
# import re
from datetime import date

# import all functions from all_functions.py
from all_functions import *

# get all csv files
csv_files = glob.glob("extracted_tweets/*/*.csv")
csv_files = sorted(csv_files)
# print(csv_files)

# new txt files
new_txt_files = [item.replace('extracted_tweets', 'extracted_tweets_txt_files') for item in csv_files]
new_txt_files = [item.split("\\")[-1] for item in new_txt_files]
new_txt_files = [item.replace('.csv', '') for item in new_txt_files]
# print(new_txt_files)

# get all filenames
filenames = []

for item in csv_files:
    filenames.append(item.split("\\")[-1])
#print("\n")    
#print(f"filenames: {filenames}", end = "\n\n")

# get all usernames
all_usernames = []

for item in filenames:
    all_usernames.append(item.split("_")[0])
    
# print(f"usernames: {all_usernames}", end = "\n\n")

# get all years and months

all_monthyears = []

for item in filenames:
    all_monthyears.append(item.split("_")[1])
    
#print(f"all month-years: {all_monthyears}", end = "\n\n")

# get all years
all_years = []

for item in all_monthyears:
    all_years.append(item [-4:])
    
#print(f"all years: {all_years}", end = "\n\n")

# get all months

all_months = []

for item in all_monthyears:
    all_months.append(item [:-4])

# accounts = ["CHANEL"]#,"nike", "forever21"] # fill later

accounts = ["CHANEL", "VictoriasSecret", "marcjacobs", "hm", "burberry", "dior", 
                "louisvuitton", "gucci", "nike", "forever21", 
                # "BoF", "Fashionista_com", "Refinery29", "ELLEmagazine", "TheCut",
                # "chrissyteigen" 
                "voguemagazine", "KendallJenner", "victoriabeckham",
                "GiGiHadid", "Caradelevingne", "tyrabanks", "giseleofficial"]

# sort list in a case-insensitive way
accounts = sorted(accounts, key = lambda s: s.casefold()) 
print(f"accounts: {accounts}", end='\n\n') 

# get today date
collection_date = date.today().strftime("%d/%m/%Y")

# create folder if it doesn't exist
create_folder("extracted_tweets_txt_files")
change_directory_to(f".\extracted_tweets_txt_files\\")

# counter
row_count = 0
total_txt_file_count = 1

# extract txt files for each row of each file
#for account in accounts: 
        
    # read each file and extract variable values
for file_index in range(0,len(csv_files)-1):
        
    #if file_index == 0:
    # keeping track of each file is being processed
    # print(f"Processing file {total_txt_file_count} from 172738")
    print(f"Processing file {total_txt_file_count}")
    print (f"processing csv file {file_index} from {len(csv_files)}\n")             

    full_filename = f"C:/Users/Rodrigo/Desktop/Python - tweet extraction/FashionTweetsExtraction/{csv_files[file_index]}"
    #print(f"full filename: {full_filename}", end="\n\n")
    temp = pd.read_csv(full_filename, sep=";", encoding="UTF-8")
  
    # for each row, read values
        
    # each row is a tweet
    for row in temp.index: 
                        
        # define the variables
        publication_date = datetime.datetime.strptime(temp.loc[row, 'Tweet Datetime'] [0:19], '%Y-%m-%d %H:%M:%S').date().strftime("%d/%m/%Y")
            
        number_followers = temp.loc[row,'Users Current Following Count']
        number_posts = temp.loc[row, 'Users Tweet Count']
            
        # if there is no link, leave field empty
        if pd.isnull (temp.loc[row, 'URL in Bio']):
            link = ""
        else:
            link = temp.loc[row, 'URL in Bio']          
        #print(link)
            
        post_content = temp.loc[row, 'Tweet Text']
            
        #post_filename = f"{full_filename}_file{cont}.txt"
        post_filename = f"{new_txt_files[file_index]}_tweet{row+1}.txt"
        
        # message to show which file is being processed
        #print(f"Processing file: {post_filename}",end='\n\n')
            
        account = post_filename.split('_')[0]
            
        # save file
        save_txt_by_template (username=account, number_followers=number_followers, 
                        number_posts=number_posts, publication_date=publication_date,
                        link=link, post_content=post_content, filename = post_filename)
            
        # updates total file count
        total_txt_file_count += 1    
    
    #print(f"All tweets saved from username '{account}'", end = '\n\n')
    
# back to main folder, two folders above
#change_directory_to(f"..\..")
    
print("All extractions complete")
# print(f"Total: {row_count} rows extracted")
print(f"Total: {total_txt_file_count} txt files extracted")
# 172738 files            
            
