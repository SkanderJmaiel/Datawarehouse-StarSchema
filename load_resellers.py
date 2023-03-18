import pandas as pd

def load_resellers(cursor):
    # load resellers data
    resellers_df = pd.read_csv('data/reseller.csv', sep='\t')

    # keep the 3 columns that we need
    resellers_df = resellers_df.loc[:, ["ResellerKey", "Business Type", "Reseller"]]



    # Convert data to load it in postgres
    resellers_df["ResellerKey"] = resellers_df["ResellerKey"].astype(str)


    # convert dataframe in records
    records = list(resellers_df.to_records(index=False))

    # insert records in table Reseller_dim
    query = 'INSERT INTO "Reseller_dim" (id_reseller, business_type, reseller_name) VALUES (CAST(%s AS INTEGER), %s, %s)'
    cursor.executemany(query, records)

