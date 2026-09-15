from flask import request, send_file
def getImportedData():
    import pandas as pd
    if request.form.get('headOrNo') == "header":
        headOrNo = 0
    else:
        headOrNo = None
    df = pd.read_csv(request.files.get('importedDataset'), sep = ' ', header = headOrNo)
    X = df.iloc[:, :-1] #this uses every column for features except the last one
    y = df.iloc[:, -1] #only uses the last column as the target    
    return X, y

def trainHelper(model, X, y):
    from sklearn.model_selection import train_test_split #allows you to split the data into a training and testing portion
    from sklearn.preprocessing import StandardScaler #has the mean of data be 0 with a standard deviation of 1

    #these below are used to help put the model in a downloadable file
    from io import BytesIO
    from zipfile import ZipFile, ZIP_DEFLATED
    import joblib

    if request.form.get('testingSize') != "":
        testingSize = float(request.form.get('testingSize'))
    else:
       testingSize = 0.2
        
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = testingSize)
    scaler = StandardScaler() #the data is scaled to prevent some features from becoming overly dominant just because they have a higher number
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)   


    model.fit(X_train_scaled, y_train) #the model gets trained on the data

    #now that the model has finished training, it needs to be downloaded to the user's computer
    zip_buffer = BytesIO()#BytesIO is temporary storage

    with ZipFile(zip_buffer, "w", ZIP_DEFLATED) as zip_file: #creates a zip in the buffer. "w" is a a sign to write to it. ZIP_DEFLATED compresses it and as zip_file allows it to be a variable so that it can be used
        with zip_file.open("knn_model_score " + str(model.score(X_test_scaled, y_test)) +".joblib", "w") as model_file: #.open is used to open the existing zip file in the buffer so that it can be written on
            joblib.dump(model, model_file)#dump is used to put the model in the model_file variable
        with zip_file.open("testing_data.joblib", "w") as testing_data:
            joblib.dump({
                        "X_test": X_test_scaled,
                        "X_test_unscalled": X_test,
                        "y_test": y_test,
                        "X_train": X_train_scaled,
                        "X_train_unscalled": X_train,
                        "y_train": y_train
                        }, testing_data)
        with zip_file.open("hyperparameters.txt", "w") as file:
            file.write(str(model.get_params()).encode("utf-8"))
            
    zip_buffer.seek(0) #the temporary storage needs to be put back at 0 so that it can be read

    return send_file(
        zip_buffer,
        as_attachment=True, #this makes it download as a file rather then just showing the file on the page
        download_name="Model and Testing Data.zip",
        mimetype= "application/zip" #specifies the data that is exported
    )      