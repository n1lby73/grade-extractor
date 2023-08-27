from dotenv import load_dotenv
from gradetractor import app
import os

load_dotenv()

app.config["MONGO_URI"] = os.getenv('MONGO_URI')
app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
app.config['ALLOWED_EXTENSIONS'] = os.getenv('ALLOWED_EXTENSION')