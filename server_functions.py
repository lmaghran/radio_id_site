from flask import request
import pandas as pd

def format_file():
    whole_file= request.get_array(field_name='file')
    df = pd.DataFrame(whole_file[1:], columns=whole_file[0])
    df["Second_Letter"]= df['Radio Serial Number'].astype(str).str[4]
    df["Third_Letter"]= df['Radio Serial Number'].astype(str).str[5]
    return df

def read_year_data():
    data = pd.read_csv("year_from_site.txt", sep=" ", header=[0])
    data.rename(columns={'Second':'Junk', 
                        'Letter':'Second_Letter',
                        'is':'Earliest possible year', 
                        'the':'Junk', 
                        'year:':'Latest possible year'}, 
                inplace=True)
    return data