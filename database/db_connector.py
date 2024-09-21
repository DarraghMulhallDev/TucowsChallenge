import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

def get_db_connection():
    try:
        # Retrieve database connection details from environment variables
        connection = psycopg2.connect(
            dbname= os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432")  
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None