import psycopg2
from db_connection import *

def create_tables():
   
    commands = (
        """
        DROP TABLE IF EXISTS "Sales_facts" CASCADE;
        DROP TABLE IF EXISTS "Product_dim" CASCADE;
        DROP TABLE IF EXISTS "Reseller_dim" CASCADE;
        DROP TABLE IF EXISTS "Localization_dim" CASCADE;
        DROP TABLE IF EXISTS "Date_dim" CASCADE;
        """,
        """
        CREATE TABLE "Sales_facts" (
          "unit_price" decimal,
          "cost" decimal,
          "quantity" int,
          "id_reseller" int,
          "id_product" int,
          "id_date" date,
          "id_localization" int
        )
        """,
        """
        CREATE TABLE "Product_dim" (
          "id_product" int PRIMARY KEY,
          "product_name" varchar,
          "category" varchar,
          "subcategory" varchar,
          "color" varchar
        )
        """,
        """
        CREATE TABLE "Reseller_dim" (
          "id_reseller" int PRIMARY KEY,
          "reseller_name" varchar,
          "business_type" varchar
        )
        """,
        """
        CREATE TABLE "Localization_dim" (
          "id_localization" int PRIMARY KEY,
          "country" varchar,
          "state" varchar,
          "city" varchar
        )
        """,
        """
        CREATE TABLE "Date_dim" (
          "id_date" date PRIMARY KEY,
          "year" int,
          "quarter" int,
          "month" int,
          "day" int,
          "day_of_the_week" varchar
        )
        """,
        """
        ALTER TABLE "Sales_facts" ADD FOREIGN KEY ("id_reseller") REFERENCES "Reseller_dim" ("id_reseller");
        ALTER TABLE "Sales_facts" ADD FOREIGN KEY ("id_product") REFERENCES "Product_dim" ("id_product");
        ALTER TABLE "Sales_facts" ADD FOREIGN KEY ("id_date") REFERENCES "Date_dim" ("id_date");
        ALTER TABLE "Sales_facts" ADD FOREIGN KEY ("id_localization") REFERENCES "Localization_dim" ("id_localization");
        """
    )
    
    try:
        # DB Connection
        connection = db_connect()

        # init cursor
        cursor = connection.cursor()

        # create tables
        for command in commands:
            cursor.execute(command)
        
        cursor.close()
        connection.commit()
        connection.close()
        print("Tables sucessfully created.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
   


create_tables()
