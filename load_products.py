import pandas as pd

def load_products(cursor):
    # load products data
    products_df = pd.read_csv('data/product.csv', sep='\t')

    # keep the columns that we need
    products_df = products_df.loc[:, ["ProductKey", "Product", "Category", "Subcategory", "Color"]]

    # handle NaN values in color column
    products_df["Color"].fillna("Other", inplace=True)

    # Convert data to load it in postgres
    products_df["ProductKey"] = products_df["ProductKey"].astype(str)

    # convert dataframe in records
    records = list(products_df.to_records(index=False))

    # insert records in table Reseller_dim
    query = 'INSERT INTO "Product_dim" (id_product, product_name, category, subcategory, color) VALUES (CAST(%s AS INTEGER), %s, %s, %s, %s)'
    cursor.executemany(query, records)
    


