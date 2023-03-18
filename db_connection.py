import psycopg2

# Start pgsql server : c
DB_NAME = "postgres"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASS = "password"

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
    

#regions = pd.read_csv('data/region.csv', sep='\t')
#sales = pd.read_csv('data/sales.csv', sep='\t')
#resellers = pd.read_csv('data/reseller.csv', sep='\t')
#products = pd.read_csv('data/product.csv', sep='\t')



