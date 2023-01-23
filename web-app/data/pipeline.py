from os import path, getcwd
import pandas as pd


readPath = path.join(getcwd(), 'data', 'NYPD_Complaint_Data_Historic.csv')

# the columns we're interested in
usecols = ['LAW_CAT_CD','OFNS_DESC', 'BORO_NM', 'CMPLNT_FR_DT', 'CMPLNT_FR_TM',
        #    'VIC_SEX', 'VIC_RACE','VIC_AGE_GROUP', 'SUSP_SEX', 'SUSP_RACE', 'SUSP_AGE_GROUP'
           ]


###########################
temp = ', '.join(usecols)
print(f'...Extracting: {temp} \n...from {readPath}')
###########################

# load csv and combine complaint date and time into one column
df = pd.read_csv(
    readPath,
    parse_dates= {'Date and Time': ['CMPLNT_FR_DT', 'CMPLNT_FR_TM']},
    usecols= usecols,
    # nrows= 1_000,
    low_memory= False
    )


###########################
print('...Making column names more user friendly')
###########################

# Make column names more user friendly
colnames = {'LAW_CAT_CD':'Offense Category', 'OFNS_DESC': 'Offense', 'BORO_NM': 'Borough'}
df.columns = df.columns.to_series().replace(colnames)


###########################
print('...Changing the date and time columns to datetime objects (Takes a very long time)')
###########################

# Convert Date and Time column to datetime object
df['Date and Time'] = pd.to_datetime(df['Date and Time'], errors= 'coerce')


###########################
print('...Separating month, day of the week and year, and appending to the dataset')
###########################

df['Year'] = df['Date and Time'].dt.year
df['Month'] = df['Date and Time'].dt.month
df['Day of the Week'] = df['Date and Time'].dt.day_name()


###########################
print('...Filtering out years before 2006')
###########################

df = df[df['Date and Time'].dt.year >= 2006]


###########################
print('...Removing nulls')
###########################

df.dropna(inplace= True)


writePath = path.join(getcwd(), 'data', 'data_subset.csv')
###########################
print(f'...Writing dataset \nTo: {writePath}')
###########################

df.to_csv(
    writePath,
    # index= False,
)

###########################
print('...Program complete')