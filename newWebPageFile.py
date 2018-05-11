from PDST_Data import getData
from flask import Flask,render_template,request
from flask_cors import CORS,cross_origin
from werkzeug.utils import secure_filename
import os
import json

UPLOAD_FOLDER = dir_path = os.path.dirname(os.path.realpath(__file__)) + '/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/angular")
def angular():
    return render_template('dist/index.html')

# @app.route("/getJson")
# def getJson():
#     return getContent()

# @app.route("/getIndexs")
# def getIndex():
#     return getIndexs()

@app.route('/upload',methods=['POST'])
def upload_file():
    
    if 'pdfFile' not in request.files:
        return 'Cannot find FILE'
    
    file = request.files['pdfFile']
    if file.filename == '':
        return 'File name not found'
    
    if file and allowed_file(file.filename):
        print('------------------------')
        print(app.config['UPLOAD_FOLDER'])
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        json_obj = getData(filename)
        return render_template('data.html',data=json_obj)


if __name__ == "__main__":
    app.run()