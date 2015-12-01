from bs4 import BeautifulSoup
import sys
import time
import pandas as pd
from urllib2 import Request, urlopen
import numpy as np

def cleanup_dataframe(df):
    df = df.applymap(lambda x: np.nan if isinstance(x, basestring) and x.isspace() else x)
    df = df.fillna("__missing__value__")
    df = df.applymap(lambda x: str(x).strip())
    df = df.applymap(lambda x: str(x).strip("'"))
    df = df.applymap(lambda x: str(x).strip('"'))
    df = df.replace(r'__missing__value__', np.nan)
    return df 

## comvert to TIDY data format
all_data= []
def to_tidy(df):
    for idx, row in df.iterrows():
        values = row.to_dict()
        for value in values:
            keys = {'country': idx, 'year': value, 'indicator': df.index.name, 'observation': values[value]}
            all_data.append(keys)


# parse the html file to get the links and metadata
with open(sys.argv[1], 'rb') as f:
	page = f.read()
soup = BeautifulSoup(page)


rows = soup.find_all("tr")
all_rows= []
for row in rows:
    a = []
    for r in row.find_all("td"):
        if 'spreadsheets.google.com' in str(r):
    	    a.append(r.a.get('href'))
        else:
        	a.append(r.string)
    if len(a) == 5:
    	all_rows.append(a)

# get the table
# There are about 519  
df = pd.DataFrame(all_rows, columns=['indicator_name', 'data_provider', 'category', 'subcategory', 'link'], dtype='object')

for idx, row in df.head(10).iterrows():
    info = row.to_dict()
    print info
    indicator = info['indicator_name']
    link_to_download = info['link'] 
    # use Request to get the data (change the link to get the most recent file)
    request = Request(link_to_download)
    socket = urlopen(request)
    
    # load into a pandas dataframe
    xlsd = pd.ExcelFile(socket, dtype=object, index_col=False)
    df_sheet1 = xlsd.parse(0, index_col=0) # parse first sheet (converts ina dataframe)
    s = df_sheet1.iloc[:,0]
    df_sheet1.index.name = indicator

    df_sheet1 = cleanup_dataframe(df_sheet1)
    to_tidy(df_sheet1)


# print all the data
for i in all_data:
    print i
# write to excel
df =  pd.DataFrame(all_data)
writer = pd.ExcelWriter('test.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='tidy_format')
writer.save()
