from MLTblueprints.app import create_app

flask_app = create_app() #gets the other packages from app.py

if __name__ == '__main__':
    flask_app.run(host = '127.0.0.1', port = 5554, debug = True) #in the final version turn off debug mode by setting it to false
    #host = '0.0.0.0' makes it run on the web

"""
To Do:
1. sort things to be in the proper folder
2. Add a user guide
"""