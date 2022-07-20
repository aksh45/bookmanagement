
from app.main import app

import os
import configparser




if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
