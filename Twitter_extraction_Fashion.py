# Script to automate tweeter extractions of fashion tweets

import tweepy
import pandas as pd
#import time
import os
from os import path

# import all functions from all_functions.py
from all_functions import *

# list of 23 accounts for extraction

account_list = ["CHANEL", "Victoriassecret", "marcjacobs", "hm", "burberry", "dior", 
                "louisvuitton", "gucci", "nike", "forever21", "BoF", "Fashionista_com", 
                "Refinery29", "ELLEmagazine", "TheCut", "VogueMagazine", "KendallJenner", 
                "GiGiHadid", "Caradelevingne", "chrissyteigen", "tyrabanks", "giseleofficial", 
                "victoriabeckham"]
                


# To extract just a few, run this
#account_list = ["Victoriassecret", "victoriabeckham"]

# Authenticating
# authentication done in all_functions.py

# main folder
change_directory_to('.\extracted_tweets\\')

extraction_years = [2018, 2019, 2020]
cont = 1
# saves files in each folder
for account in account_list:
    
    print (f'Extracting tweets from account {account}: {cont} de {len(account_list)}', end = '\n\n')
    
    # set directory
    dir_results = f'.\{account}\\'
    #print(dir_results, end='\n')
    create_folder (folder_name=dir_results)
    change_directory_to(dir_results)
    
    # saving file in the folder


    # creating extracting path
    
    for extraction_year in extraction_years:        
        
        full_extraction_file = full_extraction (account, year=extraction_year, sample=True,sample_size=15)

        # modified here
        #full_filename = f"./full_extractions/{account}_full_extraction_{extraction_year}.csv"
        full_filename = f"{account}_full_extraction_{extraction_year}.csv"

        #save_dataframe_as_csv_file (full_extraction, "forever21_full_extraction_2020.csv", separator=";")
        
        if full_extraction_file is not None:
            
            # set directory
            dir_full_extractions = './full_extractions/'
            #print(dir_results, end='\n')
            create_folder (folder_name=dir_full_extractions)
            change_directory_to(dir_full_extractions)
            
            save_dataframe_as_csv_file (full_extraction_file, full_filename, separator=";")
            
            # back to previous folder
            change_directory_to('..\\')
        
        # comment later
        # print(f'file saved in {dir_results}',end='\n')
        
        # updates count
        cont += 1
        
    print (f'Tweets extracted from account {account}', end='\n\n')
        
    # back to main folder
    change_directory_to('..\\')




# MELHORIAS

# EVITAR SALVAR ARQUIVOS MENSAIS