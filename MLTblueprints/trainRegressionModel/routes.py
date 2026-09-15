from flask import Blueprint, request, render_template
from MLTblueprints.HelperFunctions.trainHelper import trainHelper, getImportedData
trainRegressionModel = Blueprint('trainRegressionModel', __name__, template_folder = 'templates')

@trainRegressionModel.route('/')
def index():
    return "hello"

def getDataSet(dataSetRequest):
    match dataSetRequest:
        case 'fetch_california_housing':
            #return "ca"
            from sklearn.datasets import fetch_california_housing
            X, y = fetch_california_housing(return_X_y = True)
            return X, y
        case 'load_diabetes':
            from sklearn.datasets import load_diabetes
            X, y = load_diabetes(return_X_y = True)
            return X, y
    return "ER"     #The front end handles most incorrect user input. So, not much needs to be done to here

def getModel(model):
    match model:
        case 'Kneighbors':
            from sklearn.neighbors import KNeighborsRegressor
            knn = KNeighborsRegressor()
            if request.form.get('knn_totalNeighbors') != "": #since this is from a text box, if the user doesn't type anything in, it will be "" instead of empty
                knn.n_neighbors = int(request.form.get('knn_totalNeighbors'))
            if request.form.get('knn_modelWeight') != None: #since the type is radio, if the user doesn't select an option, it will be empty
                knn.weights = request.form.get('knn_modelWeight')
            return knn
        case 'RandomForest':
            from sklearn.ensemble import RandomForestRegressor
            rfr = RandomForestRegressor()
            if request.form.get('rfr_n_estimators') != "":
                rfr.n_estimators = int(request.form.get('rfr_n_estimators'))
            if request.form.get('rfr_max_depth') != "":
                rfr.max_depth = int(request.form.get('rfr_max_depth'))
            if request.form.get('rfr_min_samples_split') != "":
                rfr.min_samples_split = int(request.form.get('rfr_min_samples_split'))
            if request.form.get('rfr_min_samples_leaf') != "":
                rfr.min_samples_leaf = int(request.form.get('rfr_min_samples_leaf'))
            if request.form.get('rfr_max_features') != "":
                rfr.max_features = int(request.form.get('rfr_max_features'))
            return rfr     
    return "No valid model chosen"  #The front end handles most incorrect user input. So, not much needs to be done to here

@trainRegressionModel.route('/train', methods = ['GET', 'POST'])
def train():
    if request.method == 'GET':
        return render_template('trainRegressionModel/regressionData.html', error = None)
    if request.method == 'POST':      
        if str(request.form.get('dataChoice')) == "Sklearn Data":
            X, y = getDataSet(request.form.get('defaultDatasets'))
            #return str(request.form.get('defaultDatasets'))
        elif str(request.form.get('dataChoice')) == "User Imported Data":
            try:
                X, y = getImportedData() #the function will use "importedDataset" to get the data #Since this function is used elsewhere, to reduce duplicate code, it is imported
            except Exception:
                return render_template('trainRegressionModel/regressionData.html', error = "The dataset uploaded was invalid. Either the data was formatted improperly, or the wrong dataset was selected. Please upload a valid dataset next time.")
        else:
            return "no valid data choosen"

        model = getModel(request.form.get('MLmodel')) #reads the model selected by the user in the form and loads it into the model variable
        if getModel(request.form.get('MLmodel')) == "No valid model chosen":
            return "No valid model chosen"

        return trainHelper(model, X, y) #the code for training a regession model beyond this point would be the same as a classification model
                                        #So, to reduce duplicate code, a function from another file is called that both classification and regression can use