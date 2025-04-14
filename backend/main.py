import os
from dotenv import load_dotenv
load_dotenv() 

from app.flask_app import app

if __name__ == "__main__":
    app.run(port=5000, debug=False, use_reloader=False)
