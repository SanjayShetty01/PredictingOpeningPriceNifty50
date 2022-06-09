# import libraries
import os
import pandas as pd
import numpy as np


# import newspaper data
os.chdir('/home/sanjaya/Personal not your shit/H./Online Classes/Projects/Sentimental_Analysis')

headerList = ('Headlines','Link','Date_Time','unnamed', 'unnamed1')

newsHeadline = pd.read_csv('pulse.csv', error_bad_lines= False, names = headerList, index_col= None)

#Cleaning the dataset. 
newsHeadline = newsHeadline.drop(['unnamed', 'unnamed1'], axis = 1) # remove two empty column

newsHeadline.describe()
newsHeadline.info()
newsHeadline = newsHeadline.drop('Link', axis = 1)

# Clean the Date_Time to convert it to 'Data Time' format

newsHeadline['Date_Time'] = pd.to_datetime(newsHeadline.Date_Time,format = '%d/%m/%Y %H:%M.%f')

# Remove all the links
newsHeadline['Date_Time'] = newsHeadline['Date_Time'].replace(to_replace=r'^https?:\/\/.*[\r\n]*',value= np.nan,regex=True)

#Remove all the Alpabetical entries
newsHeadline['Date_Time'] = newsHeadline['Date_Time'].replace(to_replace=r'[a-zA-Z]',value= np.nan,regex=True)


# Save it as CSV file

newsHeadline.to_csv('News_Headlines.csv')
