from flask import render_template, Blueprint, request, send_file
from pathlib import Path

core = Blueprint('core', __name__, template_folder = 'templates')

@core.route('/')
def index():
    return render_template('core/index.html')

@core.route('/testFiles', methods = ['GET', 'POST'])
def testFiles():
    if request.method == 'GET':
        return render_template('core/upload_file.html', calculation_result = None)

    if request.method == 'POST':
        from joblib import load
        try:
            MLmodel = load(request.files.get('MLmodel'))
            testingData = load(request.files.get('testingData'))
            X_test = testingData["X_test"]
            y_test = testingData["y_test"]
            return render_template("core/upload_file.html", calculation_result = " Model score: " + str(MLmodel.score(X_test, y_test)))
        except Exception as error:
            return render_template("core/upload_file.html", calculation_result = f"It is likely that the data uploaded was invalid. The following error occurred: {error}")



        
