
from app.main import app

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()

