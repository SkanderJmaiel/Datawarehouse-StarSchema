import psycopg2
from config import *

def db_connect():
    try:
        connection = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT)
        print("Database connected successfully")
        return connection
        
    except:
        print("Database not connected successfully")
    

