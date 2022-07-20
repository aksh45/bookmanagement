
from app.main import app

import os
import configparser




if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = os.environ.get('MONGO_URI','')
    app.run()
