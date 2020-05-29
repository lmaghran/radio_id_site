from flask import request
import pandas as pd

def format_file():
    whole_file= request.get_array(field_name='file')
    df = pd.DataFrame(whole_file[1:], columns=whole_file[0])
    df["Second_Letter"]= df['Radio Serial Number'].astype(str).str[4]
    df["Third_Letter"]= df['Radio Serial Number'].astype(str).str[5]
    return df

def read_year_data():
    col_lst=[]
    col_dict={'Letter':'Second_Letter',
                'is':'Earliest possible year', 
                'year:':'Latest possible year'}
    data = pd.read_csv("year_from_site.txt", sep=" ", header=[0])
    data.rename(columns=col_dict, inplace=True)
    col_lst= ['Second_Letter', 'Earliest possible year', 'Latest possible year']
    data=data[col_lst]
    return data

def read_month_data():
    col_dict= {'The':'Third Letter', 
        'third':'Month_part',
        'the':'Month'}
    data = pd.read_csv("Month_from_site.txt", sep=" ", header=[0])
    data.rename(columns= col_dict, 
                inplace=True)
    col_lst= ['Third Letter', 'Month_part', 'Month']
    data=data[col_lst]
    return data

def merged_df(df, data):
     merged_df= pd.merge(df, data,
        left_on= 'Second_Letter',
        right_on= 'Second_Letter',
        how='left')
     return merged_df