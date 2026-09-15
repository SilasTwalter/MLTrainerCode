from flask import Flask

def create_app():
    app = Flask(__name__, template_folder = 'templates', static_folder = 'static')  #template_folder is where the folders it needs to look for html files.
                                                                                    #static_folder are things that flask does not need to dirrectly handle like css.

    #import and register all blueprints
    from MLTblueprints.core.routes import core
    from MLTblueprints.trainML.routes import trainML #trainML is the blueprint in the following line: trainML = Blueprint('trainML', __name__, template_folder = 'template')
    from MLTblueprints.trainClassificationModel.routes import trainClassificationModel

    from MLTblueprints.trainRegressionModel.routes import trainRegressionModel
    #this set the default URL for the different parts of the application
    app.register_blueprint(core, url_prefix = '/')
    app.register_blueprint(trainML, url_prefix = '/trainML')
    app.register_blueprint(trainRegressionModel, url_prefix = '/Train Regression Model')
    app.register_blueprint(trainClassificationModel, url_prefix = '/Train Classification Model')

    return app    