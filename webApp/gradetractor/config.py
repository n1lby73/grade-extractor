from dotenv import load_dotenv
from gradetractor import app
import os

load_dotenv()

app.config["MONGO_URI"] = os.getenv('MONGO_URI')
