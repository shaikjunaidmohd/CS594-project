# importing libraries
import numpy as np
import pandas  as pd
import os

# Converting PLT file to DataFrame
def convertPltToDf(filename,user):
    df = pd.read_csv(filename, sep=",", skiprows=6, header = None, 
                       names = ['latitude','longtitude',3,4,5,'Date','Time'],
                       usecols=['latitude','longtitude','Date','Time'])
    df['User'] = [user]*len(df)
    return df.sample(min(50,len(df)))
    
# Merging  all dataframes PlT files into main DataFrame 
def loadUserData(userFolder,mainDf,user):
    userFolder = userFolder+'\\Trajectory'
    plt_list = os.listdir(userFolder)
    for plt in plt_list:
        path = userFolder+'\\'  + plt
        print(path)
        mainDf = pd.concat([mainDf , convertPltToDf(path,user)])
    return mainDf

# Main Load function that iterates through the all users and form the dataframe
def loadData():
    path = os.getcwd()+'\\Geolife Trajectories 1.3\\Data'
    mainDf = pd.DataFrame(columns = ['latitude','longtitude','Date','Time','User'])
    for user in os.listdir(path):
        if(int(user)>11):
            break
        filename = path + '\\' + user
        mainDf = loadUserData(filename,mainDf,int(user))
    return mainDf


# Making the function call
maindf = loadData()

# Reseting the index of dataframe and printing the stats of data
maindf = maindf.reset_index(drop = True)
maindf.describe()

# Storing the dataframe into pickle
maindf.to_pickle("./data.pkl")







