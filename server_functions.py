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
                'year:':'Year'}
    data = pd.read_csv("year_from_site.txt", sep=" ", header=[0])
    data.rename(columns=col_dict, inplace=True)
    col_lst= ['Second_Letter', 'Year']
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
    data['Month_part'].replace('First', 1, inplace=True)
    data['Month_part'].replace('Last', 15, inplace=True)
    data['Day']= data['Month_part']
    return data

def merged_df(df, data, month_data):
     merged= pd.merge(df, data,
        left_on= 'Second_Letter',
        right_on= 'Second_Letter',
        how='left')
     merged_df= pd.merge(merged, month_data,
        left_on= 'Third_Letter',
        right_on= 'Third Letter',
        how='left')
     merged_df['Manufacture_date']= pd.to_datetime(((merged_df['Year']*10000)+(merged_df['Month']*100)+merged_df['Day']).astype(str).str.split('.', expand = True)[0], format='%Y%m%d')
     return merged_df

def drop_cols(merged_df):
    merged_df=merged_df.drop(['Second_Letter', 'Year', 'Third_Letter', 'Third Letter', 'Month_part', 'Month', 'Day'], axis=1)
    return merged_df