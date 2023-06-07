from dotenv import load_dotenv
from mongoengine import connect
import os
import cloudinary

# Load environment variables from .env file
load_dotenv()

db_name = "uitcommerce"

# Define the default connection
connect(
    db=db_name,
    host=os.getenv("MONGO_URL"),
)

# Setup cloudinary
cloudinary.config( 
  cloud_name = os.getenv("CLOUD_NAME"), 
  api_key = os.getenv("API_KEY"), 
  api_secret = os.getenv("API_SECRET"), 
)
