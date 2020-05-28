
from flask import Flask, request, jsonify, render_template
from flask_debugtoolbar import DebugToolbarExtension
import flask_excel as excel
import pandas as pd

app = Flask(__name__)
app.secret_key= "ABC"


@app.route("/", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        whole_file= request.get_array(field_name='file')
        df = pd.DataFrame(whole_file[1:], columns=whole_file[0])
        df["Second_letter"]= df['Radio Serial Number'].astype(str).str[1]
        print(df["Second_letter"])
        return jsonify({"result":whole_file})
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

    # if __name__ == "__main__": 

    # # app.debug = True #pragma: no cover
    # # connect_to_db(app) #pragma: no cover
    # # DebugToolbarExtension(app) #pragma: no cover
    # # app.run(host="0.0.0.0")