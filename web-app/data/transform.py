from os import path, getcwd
import pandas as pd


readPath = path.join(getcwd(), 'data', 'NYPD_Complaint_Data_Historic.csv')

# the columns we're interested in
usecols = ['LAW_CAT_CD', 'OFNS_DESC', 'BORO_NM', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM', 'VIC_SEX', 'VIC_RACE','VIC_AGE_GROUP', 'SUSP_SEX', 'SUSP_RACE', 'SUSP_AGE_GROUP']

# load csv and combine complaint date and time into one column
df = pd.read_csv(
    readPath,
    parse_dates= {'Date and Time': ['CMPLNT_FR_DT', 'CMPLNT_FR_TM']},
    usecols= usecols,
    # nrows= 10_000,
    low_memory= False
    )

# Make column names more user friendly
colnames = {'LAW_CAT_CD':'Offense Category', 'OFNS_DESC': 'Offense', 'BORO_NM': 'Borough'}
df.columns = df.columns.to_series().replace(colnames)

# Convert Date and Time column to datetime object
df['Date and Time'] = pd.to_datetime(df['Date and Time'], errors= 'coerce')


writePath = path.join(getcwd(), 'data', 'data_subset.csv')
df.to_csv(
    writePath,
)