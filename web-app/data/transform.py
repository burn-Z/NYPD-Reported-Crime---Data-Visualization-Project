import numpy as np
import pandas as pd
from datetime import datetime

df = pd.read_csv('NYPD_Complaint_Data_Historic.csv',
                 low_memory= False,
                )

df = df.loc[~df['CMPLNT_FR_DT'].isnull()]

df = df.loc[:, ~df.columns.isin(['CMPLNT_NUM', 'LAW_CAT_CD', 'OFNS_DESC', 'BORO_NM', 'CMPLNT_FR_DT'])]

def extract_year(mydat):
    temp = int(str(mydat[-4:])) if len(mydat) == 10 else -1
    return temp if temp >= 2006 else None

def extract_month(mydat):
    temp = int(str(mydat[:2])) if len(mydat) == 10 else None
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    return month[temp-1]

def extract_day(x):
    if not isinstance(x,float) and str(x) != 'nan':
        temp = datetime.strptime(x, "%m/%d/%Y")
    else:
        fake = '01/01/2001'
        temp = datetime.strptime(str(fake), "%m/%d/%Y")

    return  temp.strftime('%A')

# extract the year from the complaint date
# and if its before 2006, replace with None
df['year'] = df['CMPLNT_FR_DT'].apply(extract_year)
df['month'] = df['CMPLNT_FR_DT'].apply(extract_month)
df['day'] = df['CMPLNT_FR_DT'].apply(extract_day)

# drop years before 2006
df.dropna(inplace= True)

#######################################################
# change column type
col_types = {
    'year':'int64'
}

df = df.astype(col_types, errors = 'ignore')


#######################################################
# Rename columns
df.columns = df.columns.to_series().replace({'CMPLNT_NUM': 'id', 'LAW_CAT_CD':'category', 'OFNS_DESC': 'offense', 'CMPLNT_FR_DT': 'date', 'BORO_NM': 'borough'})


# create csv for subsetted data
df.to_csv('data\\data_subset.csv',index= False)