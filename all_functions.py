# All Functions

# Libraries
import tweepy
import pandas as pd
import time
import os
from os import path
import calendar
import datetime
import pytz


# Authentication in Twitter

credentials_df = pd.read_csv('./credentials/credentials.csv',header=None,names=['name','key'])

#credentials_df

consumer_key = credentials_df.loc[credentials_df['name']=='consumer_key','key'].iloc[0]
consumer_secret = credentials_df.loc[credentials_df['name']=='consumer_secret','key'].iloc[0]
access_token = credentials_df.loc[credentials_df['name']=='access_token','key'].iloc[0]
access_token_secret = credentials_df.loc[credentials_df['name']=='access_secret','key'].iloc[0]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, 
                 wait_on_rate_limit=True, # wait_on_rate_limit=True necessary to avoid api limit
                wait_on_rate_limit_notify=True, retry_errors=set([401, 404, 500, 502, 503, 504])
            )



# FUNCTIONS

# Function created to extract coordinates from tweet if it has coordinate info
# Tweets tend to have null so important to run check
# Make sure to run this cell as it is used in a lot of different functions below
def extract_coordinates(row):
    if row['Tweet Coordinates']:
        return row['Tweet Coordinates']['coordinates']
    else:
        return None

# Function created to extract place such as city, state or country from tweet if it has place info
# Tweets tend to have null so important to run check
# Make sure to run this cell as it is used in a lot of different functions below
def extract_place(row):
    if row['Place Info']:
        return row['Place Info'].full_name
    else:
        return None



def scrape_username_tweets_by_date (username, 
                              result_type = 'recent', 
                              max_tweets = 2000, language='en',
                              since_date = '2018-01-01', until_date = '2021-01-31',
                              filename='advancedqueries-tweets.csv',
                              export_file = True,
                              filename_type = 'csv'):
    # important if using this function alone or for testing
    if export_file == True and filename_type not in ['csv']:
        print('Filename type must be "csv"!')
        return()
        
    # dates: format 'YYYY-MM-DD'
    # result_type - other options: 'popular' or 'mixed'

    
    # Creation of query method using parameters
    
    # extracts tweets
    
    tweets = tweepy.Cursor(api.user_timeline, 
                            id=username, result_type = result_type, 
                            # since = since_date, until = until_date, 
                            language=language,
                            tweet_mode='extended',
                            count=100).items(max_tweets)
    
    '''
    if search_key is not None:
    
        tweets = tweepy.Cursor(api.search, q=search_key, 
                               id=username, #result_type = result_type, 
                           since = since_date, until = until_date, language=language,
                           count=100).items(max_tweets)
    else:
        tweets = tweepy.Cursor(api.search, 
                               id=username, #result_type = result_type, 
                           since = since_date, until = until_date, language=language,
                           count=100).items(max_tweets)
    '''
    
    # defining initial and final twitter date to filter
    
    #import datetime

    # convert string to date
    startDate = datetime.datetime.strptime(since_date, '%Y-%m-%d')#.date()
    endDate = datetime.datetime.strptime(until_date, '%Y-%m-%d')#.date()
    
    # convert date to datetime
    #startDate_datetime = datetime.datetime(startDate.year, startDate.month, startDate.day)
    #endDate_datetime = datetime.datetime(endDate.year, endDate.month, endDate.day)
    startDate_datetime = datetime.datetime.strptime(since_date, '%Y-%m-%d')#.date()
    endDate_datetime = datetime.datetime.strptime(until_date, '%Y-%m-%d')#.date()
    
    #print (f"start date obj = {since_date_obj}")
    #print (f"end date obj = {until_date_obj}")
   
   # Printing dates for Testing
    #print(f'Start date: {startDate}')
    #print(f'End date: {endDate}')
    
    # convert datetime to aware to compare (dates must be either 'naive' or 'aware' to be compared)
    #import pytz
    # utc = pytz.UTC

    # startDate_datetime = utc.localize(startDate_datetime) 
    # endDate_datetime = utc.localize(endDate_datetime)  
    
     
    # filtering tweets by date
    filtered_tweets = []
    # tmpTweets = api.user_timeline(username)
    for tweet in tweets:
        # converting from format "2021-02-16 16:05:20+00:00" to "2021-02-16 16:05:20"
        tweet_creation_datetime = datetime.datetime.strptime(str(tweet.created_at)[0:19], '%Y-%m-%d %H:%M:%S')

        #print(f"tweet.created_at: {tweet.created_at}")
        #if tweet.created_at >= startDate_datetime and tweet.created_at <= endDate_datetime:
        #    filtered_tweets.append(tweet)
        if tweet_creation_datetime >= startDate_datetime and tweet_creation_datetime <= endDate_datetime:
            filtered_tweets.append(tweet)
            
            
    '''
    while (tweets[-1].created_at > startDate):
        tweets = api.user_timeline(username, max_id = tweets[-1].id)
        for tweet in tweets:
            if tweet.created_at < endDate and tweet.created_at > startDate:
                filtered_tweets.append(tweet)
    ''' 
        
    # List comprehension pulling chosen tweet information from tweets iterable object
    # Add or remove tweet information you want in the below list comprehension
    tweets_list = [[tweet.full_text, tweet.created_at, 
                    tweet.retweet_count, tweet.favorite_count, 
                    tweet.user.screen_name,# tweet.user.id_str, 
                    tweet.user.location, tweet.user.url, 
                    #tweet.user.verified, 
                    tweet.user.followers_count,
                    tweet.user.friends_count, 
                    tweet.user.statuses_count, #tweet.user.default_profile_image, 
                    tweet.lang] for tweet in filtered_tweets]

    # Creation of dataframe from tweets_list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list,columns=['Tweet Text', 'Tweet Datetime', 
                                                  'Tweet Retweet Count', 'Tweet Favorite Count', 
                                                  'Twitter @ name', #'Twitter User Id', 
                                                  'Twitter User Location', 'URL in Bio',
                                                  #'User Verified Status', 
                                                  'Users Current Following Count',
                                                 'Number of accounts user is following', 'Users Tweet Count',
                                                 #'Profile Image URL',
                                                 'Tweet Language'])
    # create filename
    full_csv_filename = f"{filename}.csv"
    
    if export_file == True: #and filename_type == 'csv':
        try:
            tweets_df.to_csv(full_csv_filename, sep=';', index = False)
            
            print( f"file '{full_csv_filename}' created successfully")
            
            # return (tweets_df)
        # these commands on the except are important if the function is to be used separately or for testing it
        # otherwise, we can use 'pass'
        except:
            print( f"file '{full_csv_filename}' was not created successfully")
            #pass
            #full_csv_filename = f"{filename}.csv"
            # print( f"file '{full_csv_filename}' could not be created")
    elif export_file == False:
        print(f"file '{full_csv_filename}' was not exported")
    else:
        print("export_file must be either True or False")
    
    return (tweets_df)
    
##########################################################


##################################################################################
def sample_df_rows (dataframe, sample_size=15, replace=False, seed = 1):
    if dataframe is not None:
        sampled_df = dataframe.sample(n = sample_size, replace=replace,random_state = seed)
        return (sampled_df) 
##################################################################################

##################################################################################
def save_dataframe_as_csv_file (dataframe, filename = "sampled_file.csv", separator=";", index=False):
    dataframe.to_csv(filename, sep=separator, index=index)
##################################################################################

##################################################################################

def save_txt_by_template (username, number_followers, 
                          number_posts, publication_date,
                          link, post_content, filename = 'myfile.txt',
                          encoding="UTF-8"):
    
    import datetime
    collection_date = str(datetime.datetime.now().date().strftime("%d/%m/%Y"))
        
    file = open(filename,"w+", encoding= encoding) 

    file.write(f"<Twitter {username}\n\n") 
    file.write(f"Twitter link: https://twitter.com/{username}/\n\n")
    file.write(f"{number_followers} followers\n")
    file.write(f"{number_posts} posts\n\n")
    file.write(f"Retrieved at {collection_date}\n\n")
    file.write(f"Published at {publication_date}\n\n")
    file.write(f"Direct link: {link}\n\n")
    file.write(f"Post:> \n\n{post_content}")

    file.close() #to change file access modes
##################################################################################

# try to automate extraction per month using function

##################################################################################
def per_month_extraction (username,month='January',year=2020, result_type = 'popular',
                          sample=False,sample_size=15, export_file = True, filename_type = 'csv'): 


    # YYYY-MM-DD
    initial_day = create_date (year=year, month_year=month, day='01')
    
    # months with 30 or 31 days
    if month in ['January', 'March', 'May', 'July', 'August', 'October', 'December']:
        last_day ='31'
    if month in ['February']:
        # check if leap year (calendar library)
        if calendar.isleap(year):
            last_day = 29
        else:
            last_day = 28 
    else:
        last_day = '30'
        
    final_day = create_date (year=year, month_year=month, day=last_day)
    
    filename = f"{username}_{month}{year}_popularTweets"

# extract tweets
    tweets = scrape_username_tweets_by_date (username=username,
                            language = 'en',
                            #search_key = 'tip',
                            result_type = result_type,
                            since_date = initial_day,
                            until_date = final_day, 
                            max_tweets = 2000,
                            filename = filename,
                            export_file = export_file,
                            filename_type = filename_type)
    
    try:                         
        if sample:
            sampled_tweets = sample_df_rows ( tweets, sample_size = sample_size, replace = False, seed = 1)                      
            return(sampled_tweets)
        else:
            return(tweets)
    except ValueError:
        pass
        #print("Search returned no results.")

# nike_example1 = per_month_extraction ('nike',month='December',year=2020, 
#                          sample=True,sample_size=15)

##################################################################################


####################################
def change_directory_to (target_path):
    os.chdir(target_path)
    # print(f"Directory changed to {target_path}") 
#####################################

##########################################################
def create_subfolder_paths_2 (folder_name, subfolder_names):
    
    # create subfolders  
    all_subfolders = []
    for item in folder_name:
        # print(f"item: {item}")

        for subfolder in subfolder_names:
            # create path
            new_subfolder = f"./{item}/{subfolder}/"
            
            # replace double bars by single bars if necessary
            new_subfolder = new_subfolder.replace("//","/") 
            
            #print(f"new_subfolder: {new_subfolder}/")
            all_subfolders.append(new_subfolder)

    return (all_subfolders)
##########################################################

##########################################################
def create_full_subfolder_paths (folder_name, subfolder_names, sub_subfolder_names):
    
    # create subfolders  
    all_subfolders = []
    for item in folder_name:
        # print(f"item: {item}")
        for subfolder in subfolder_names:
            for sub_subfolder in sub_subfolder_names:            
            
                # create path
                paths_to_create = f"./{item}/{subfolder}/{sub_subfolder}"
                
                # replace double bars by single bars if necessary
                paths_to_create = paths_to_create.replace("//","/") 
                
                #print(f"path_to_create: {path_to_create}/")
                all_subfolders.append(paths_to_create)

    return (all_subfolders)
##########################################################
def create_folder (folder_name='my_folder'):
    
    # if path does not exist, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

##########################################################
def create_all_subfolders (subfolders_paths):
    # set current directory to folder name
    
    # create paths for subfolders
    for path in subfolders_paths:
        
#        current_folder = path#.split("/")[2]
#        print(f"current_folder: {current_folder}", end="\n")
    
#        os.chdir(current_folder)      
        
        #print(path, end="\n")
        create_folder(path)
        print(f"Created folder: {path}",end="\n")
##########################################################


#############################################################
def create_date (year=2020, month_year="January", day="01"):
    import calendar
    
    # 
    month_number_dict = {month: index for index, month in enumerate(calendar.month_name) if month}
    month = month_year
    month_number = month_number_dict[month]
    year = year
    day=day

    # all_months = list(month_number_dict.keys())
    last_months = ['October','November','December'] 
    # starting_months = [item for item in all_months if item not in last_months]

    # sets up string
    if month in last_months:
        date_output = f"{year}-{month_number}-{day}".replace("010|011|012","0")
    else:
        date_output = f"{year}-0{month_number}-{day}".replace("010|011|012","0")
    return(date_output)
###################################################################################





###############################################################################################
def full_extraction (username, year, sample=False,sample_size=15):#, 
                     #export_full_file = True, export_individual_files = False):
    
    september_extraction = per_month_extraction (username,month='September',year=year, 
                          sample=sample,sample_size=sample_size, 
                          #export_file = export_individual_files,
                          filename_type = 'csv')
    # print(f'september extraction: {september_extraction}', end='\n')
    # print(september_extraction, end = '\n\n')
    #if september_extraction is None:
        # print('It is None')
    october_extraction = per_month_extraction (username,month='October',year=year, 
                          sample=sample,sample_size=sample_size, 
                          #export_file = export_individual_files, 
                          filename_type = 'csv')
    # print(f'october extraction: {october_extraction}', end='\n')
    #print(october_extraction, end = '\n\n')
    #if october_extraction is None:
        # print('It is None')
    december_extraction = per_month_extraction (username,month='December',year=year, 
                          sample=sample,sample_size=sample_size, 
                          #export_file = export_individual_files, 
                          filename_type = 'csv')
    # print(f'december extraction: {december_extraction}', end='\n')
    #print(december_extraction, end = '\n\n')
    #if december_extraction is None:
        # print('It is None')
    january_extraction = per_month_extraction (username,month='January',year=year, 
                          sample=sample,sample_size=sample_size, 
                          #export_file = export_individual_files, 
                          filename_type = 'csv')
    #print(january_extraction, end = '\n\n')
    #if january_extraction is None:
        # print('It is None')
    # print(f'january extraction: {january_extraction}', end='\n')
    
    february_extraction = per_month_extraction (username,month='February',year=year, 
                          sample=sample,sample_size=sample_size, 
                          #export_file = export_individual_files, 
                          filename_type = 'csv')
    # print(february_extraction, end = '\n\n')
    
    #if february_extraction is None:
    #    print('It is None')

    # print(f'february extraction: {february_extraction}', end='\n')
    
    march_extraction = per_month_extraction (username,month='March',year=year, 
                          sample=sample,sample_size=sample_size, 
                          #export_file = export_individual_files, 
                          filename_type = 'csv')
    # print(f'march extraction: {march_extraction}', end='\n')
    #print(march_extraction, end = '\n\n')
    #if march_extraction is None:
    #    print('It is None')

    #filenames = ['september_extraction', 'october_extraction', 'december_extraction',
    #                             'january_extraction', 'february_extraction', 'march_extraction']
    
    # create list of dataframes
    #all_month_extractions = []
    #all_month_extractions.extend(value for name, value in locals().items() if name.endswith('extraction'))
    
    #all_month_extractions = [september_extraction, october_extraction, december_extraction,
    #                                    january_extraction, february_extraction, march_extraction]
    #try:
    
    #print(f"all month extrations: {all_month_extractions}", end="\n\n")
    '''
    unified_df = pd.DataFrame(columns=all_month_extractions[0].columns)
    if export_full_file == True:
        
        for extracted_file in all_month_extractions: # for each file
            for row in extracted_file.index: # for each row
                each_row = extracted_file.iloc(0)
                unified_df.append(each_row)
                
        print(unified_df)
    '''    
        
    '''    
        from functools import reduce
        unified_df = reduce(lambda df1, df2: september_extraction.merge(october_extraction, "outer"), 
                            all_month_extractions)
        
        unified_df = reduce(lambda df1, df2: unified_df.merge(december_extraction, "outer"), 
                            all_month_extractions)
        
        unified_df = reduce(lambda df1, df2: unified_df.merge(january_extraction, "outer"), 
                            all_month_extractions)
        
        unified_df = reduce(lambda df1, df2: unified_df.merge(february_extraction, "outer"), 
                            all_month_extractions)
        
        unified_df = reduce(lambda df1, df2: unified_df.merge(march_extraction, "outer"), 
                            all_month_extractions)
        
        '''
    '''
        
        #try:
    
            # using list comprehension to remove None values in list 
        valid_month_extractions = [i for i in all_month_extractions if i is not None] #len(i) >= 0] 
        #print(valid_month_extractions)    
            # concatenate valid
            #try:
        full_extractions = pd.concat(all_month_extractions, axis=0, ignore_index=True)
        '''
    '''
        full_extractions = pd.concat([september_extraction, october_extraction,
                                          december_extraction, january_extraction, 
                                          february_extraction, march_extraction],
                                          axis=0, ignore_index=True)
        
        
            #print(f"full extractions: {full_extractions}") 
        '''    
        #return(unified_df)   
        #return(full_extractions)
        #except: ValueError: All objects passed were None
        #    pass
    '''    
    elif export_full_file == False:
        
        if export_individual_files == False:
            print("Full file was not exported. Individual extractions were not exported", end = "\n\n")        
        elif export_individual_files ==True:
            print("Full file was not exported. Individual extractions were exported", end = "\n\n")        
        else:
            print("export_individual_files must be either True or False")
    '''        
            #return (all_month_extractions)
    #except:
    #    print("It was not possible to concatenate all empty dataframes.")
    # ORIGINAL 
    #full_extractions = pd.concat([september_extraction, october_extraction, december_extraction,
    #
    # january_extraction, february_extraction, march_extraction], axis=0)
    
    #except ValueError:
    #    pass
    
    
###############################################################################################
