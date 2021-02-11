import os

#acc_list = ['nike','adidas']
acc_list = ["CHANEL", "Victoriassecret", "marcjacobs", "hm", "burberry", "dior", 
                "louisvuitton", "gucci", "nike", "forever21", "BoF", "Fashionista_com", 
                "Refinery29", "ELLEmagazine", "TheCut", "VogueMagazine", "KendallJenner", 
                "GiGiHadid", "Caradelevingne", "chrissyteigen", "tyrabanks", "giseleofficial", 
                "marcjacobs", "victoriabeckham"]

subfolders = ['2019','2020']
extraction_months = ['september', 'november', 'december','january','february','march']


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


'''
####################################
def create_extraction_folders (current_directory,
                                      folder_names = ['september', 'november', 'december',
                                                    'january','february','march']):
    os.chdir(current_directory)
    map (create_folder, folder_names)
#####################################
'''
all_paths = create_full_subfolder_paths (acc_list, subfolders, extraction_months)

print(all_paths,end="\n")

# set directory to "extracted_tweets"
os.chdir("extracted_tweets")

create_all_subfolders (all_paths)

# creating month folders for each year
#subfolder_paths2 = create_subfolder_paths (subfolder_paths, extraction_months)  
#print(subfolder_paths2)

#create_all_subfolders (subfolder_paths2)


