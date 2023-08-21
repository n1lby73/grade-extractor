from dotenv import load_dotenv
from gradetractor import app
import os

app.config["MONGO_URI"] = os.getenv('MONGO_URI')
