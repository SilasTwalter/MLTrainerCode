from flask import request, render_template, redirect, url_for, Blueprint, send_file

trainML = Blueprint('trainML', __name__, template_folder = 'templates')

@trainML.route('/')
def index():
    return render_template('trainML/index.html')

def getDataSet(dataSet):
    match dataSet:
        case "iris":
            from sklearn.datasets import load_iris
            X, y = load_iris(return_X_y = True)
            return X, y
    return "There was a problem with selecting a data set"

@trainML.route('/Kneighbors', methods = ['Get', 'POST'])
def Kneighbors():
    if request.method == 'GET':
        return render_template('trainML/Kneighbors.html')
    if request.method == 'POST':
        from sklearn.model_selection import train_test_split #allows you to split the data into a training and testing portion
        from sklearn.preprocessing import StandardScaler #has the mean of data be 0 with a standard deviation of 1
        from sklearn.neighbors import KNeighborsClassifier #
        from io import BytesIO
        from zipfile import ZipFile, ZIP_DEFLATED
        import joblib


        X, y = getDataSet("iris")

        testingSize = float(request.form.get('testingSize'))
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = testingSize)

        scaler = StandardScaler() #way the data is organized
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        totalNeighbors = int(request.form.get('totalNeighbors'))
        modelWeight = request.form.get('modelWeight')
        knn = KNeighborsClassifier(
            n_neighbors = totalNeighbors,
            weights = modelWeight
        ) #how the data is judged
        knn.fit(X_train_scaled, y_train)


        #now that the model has finished training, it needs to be downloaded to the user's computer
        zip_buffer = BytesIO()#BytesIO is temporary storage

        with ZipFile(zip_buffer, "w", ZIP_DEFLATED) as zip_file: #creates a zip in the buffer. "w" is a a sign to write to it. ZIP_DEFLATED compresses it and as zip_file allows it to be a variable so that it can be used
            with zip_file.open("knn_model_score " + str(knn.score(X_test_scaled, y_test)) +".joblib", "w") as model_file: #.open is used to open the existing zip file in the buffer so that it can be written on
                joblib.dump(knn, model_file)#dump is used to put the model in the model_file variable
            with zip_file.open("testing_data.joblib", "w") as testing_data:
                joblib.dump({
                            "X_test": X_test_scaled,
                            "X_test_unscalled": X_test,
                            "y_test": y_test,
                            "X_train": X_train_scaled,
                            "X_train_unscalled": X_train,
                            "y_train": y_train
                            }, testing_data)
            
        zip_buffer.seek(0) #the temporary storage needs to be put back at 0 so that it can be read

        return send_file(
            zip_buffer,
            as_attachment=True, #this makes it download as a file rather then just showing the file on the page
            download_name="Model and Testing Data.zip",
            mimetype= "application/zip" #specifies the data that is exported
        )
    
