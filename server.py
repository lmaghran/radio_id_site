
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
import flask_excel as excel
import pandas as pd
import openpyxl as openpyxl
from jinja2 import StrictUndefined
from server_functions import read_year_data, read_month_data, format_file, merged_df

app = Flask(__name__)
app.secret_key= "ABC"

@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        whole_file= request.get_array(field_name='file')
        df= format_file()
        year_data=read_year_data()
        month_data=read_month_data()
        merged_frame= merged_df(df, year_data, month_data)
        # merged_frame['Year']= pd.to_datetime(merged_frame['Year'], format='%Y')
        # merged_frame['Month']= pd.to_datetime(merged_frame['Month'], format='%B')
        # merged_frame['Latest possible year']= pd.to_datetime(merged_frame['Latest possible year'], format='%Y')
        merged_frame=merged_frame.to_excel("output.xlsx", sheet_name='Sheet_name_1')
        return render_template("index.html", merged_frame=merged_frame)
    return render_template("index.html")


@app.route("/download", methods=['GET'])
def download_file():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv")


@app.route("/export", methods=['GET'])
def export_records():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name="export_data")


@app.route("/download_file_named_in_unicode", methods=['GET'])
def download_file_named_in_unicode():
    return excel.make_response_from_array([[1, 2], [3, 4]], "csv",
                                          file_name=u"中文文件名")


# insert database related code here
if __name__ == "__main__":
    app.debug = True
    excel.init_excel(app)
    DebugToolbarExtension(app)
    app.run(host="0.0.0.0")