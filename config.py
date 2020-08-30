class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "1234567890"
    #SESSION_COOKIE_SECURE = True  ## habilitar esto cuanto tengamos https, no sirve de otro modo
    UPLOAD_FOLDER = "/tmp"
    FIREBASE_SERVICE_ACCOUNT_PATH = "/home/daniel/budget_flask/service_account.json"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    FIREBASE_SERVICE_ACCOUNT_PATH = "/home/daniel/Projects/firebase/service_account.json"

class TestingConfig(Config):
    TESTING = True
    SESSION_COOKIE_SECURE = False