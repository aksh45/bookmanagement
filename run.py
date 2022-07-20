
from app.main import app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI','')
    app.run()
else:
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI','')
    app.run()
