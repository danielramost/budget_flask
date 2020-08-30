from flask import Flask

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = '/tmp'
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

from budget import routes