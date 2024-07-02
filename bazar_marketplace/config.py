import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+mysqlconnector://root:password@localhost:3306/bazar_marketplace")
