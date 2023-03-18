from db_connection import *
from load_dates import *
from load_localizations import *
from load_products import *
from load_resellers import *
from load_sales import *


# connect to DB
connection = db_connect()
# init cursor
cursor = connection.cursor()

#load data
load_dates(cursor = cursor)
load_localizations(cursor = cursor)
load_products(cursor = cursor)
load_resellers(cursor = cursor)
load_sales(cursor = cursor)


connection.commit()
cursor.close()
connection.close()
