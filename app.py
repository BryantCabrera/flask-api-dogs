from flask import Flask
#we have to register the API on our flask application, 1st import it
from resources.dogs import dogs_api
import models
#separating config into separate file modularizes code
import config
# DEBUG = True
# PORT = 8000

#__init__.py is blank but it's for the resources directory

app = Flask(__name__)
#we have to register the API
#we can prefix the api route
app.register_blueprint(dogs_api, url_prefix='/api/v1')

#ROUTES
@app.route('/')
def hello_world():
    return 'Hello World'

if __name__ == '__main__':
    models.initialize()
    app.run(debug=config.DEBUG, port=config.PORT)