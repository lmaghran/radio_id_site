
from flask import Flask, request, jsonify, render_template, send_file
from flask_debugtoolbar import DebugToolbarExtension
import flask_excel as excel
import pandas as pd
import openpyxl as openpyxl
from jinja2 import StrictUndefined
import os
from server_functions import read_year_data, read_month_data, format_file, merged_df, drop_cols

app = Flask(__name__)
app.secret_key= "ABC"

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        whole_file= request.get_array(field_name='file')
        df= format_file()
        columns=df.columns
        year_data=read_year_data()
        month_data=read_month_data()
        merged_frame= merged_df(df, year_data, month_data)
        merged_frame= drop_cols(merged_frame)
        
        try:
            open('output.xlsx', 'w')
            merged_frame=merged_frame.to_excel("output.xlsx", sheet_name='Sheet_name_1')
            send_file('output.xlsx', attachment_filename='output.xlsx')
            import os
            os.remove('output.xlsx')
            return render_template("index.html")
        except Exception as e:
            return str(e)

    return render_template("index.html")


if __name__ == "__main__":
    app.debug = True
    excel.init_excel(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")