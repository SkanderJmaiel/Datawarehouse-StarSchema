import pandas as pd


def load_sales(cursor):
    # load sales data
    sales_df = pd.read_csv('data/sales.csv', sep='\t')

    # load resellers data
    resellers_df = pd.read_csv('data/reseller.csv', sep='\t')

    # keep the columns that we need
    sales_df = sales_df.loc[:, ["Quantity", "Unit Price", "Cost", "ProductKey", "ResellerKey", "OrderDate"]]

    # remove $ sign from price and cost columns
    sales_df["Unit Price"] = sales_df["Unit Price"].str.replace(",", "").str.replace("$", "").astype(float)
    sales_df["Cost"] = sales_df["Cost"].str.replace(",", "").str.replace("$", "").astype(float)

    # the cost column represent the cost of the quantity sold
    # we modify it to get the cost per unit
    sales_df["Cost"] /= sales_df["Quantity"]

    # date format dd/mm/yyy
    sales_df["OrderDate"] = pd.to_datetime(sales_df["OrderDate"]).dt.strftime('%d/%m/%Y')


    # keep the 3 columns that we need and drop duplicates
    localizations_df = resellers_df.loc[:, [ "Country-Region", "State-Province", "City"]].drop_duplicates()

    # add column localization_key
    localizations_df = localizations_df.reset_index(drop=True).reset_index().rename(columns={'index': 'LocalizationKey'})
    localizations_df['LocalizationKey'] += 1


    # merge resellers and localizations
    df_merged = resellers_df.merge(localizations_df, on=["City", "State-Province", "Country-Region"], how="left")
    # merge sales and the merged_df to add localizationkey
    sales_df = sales_df.merge(df_merged[['ResellerKey', 'LocalizationKey']], on='ResellerKey', how='left')

    # add SaleKey column to sales_df
    sales_df = sales_df.reset_index(drop=True).reset_index().rename(columns={'index': 'SaleKey'})
    sales_df['SaleKey'] += 1

    # Convert data to load it in postgres
    sales_df["Quantity"] = sales_df["Quantity"].astype(str)
    sales_df["Unit Price"] = sales_df["Unit Price"].astype(str)
    sales_df["Cost"] = sales_df["Cost"].astype(str)
    sales_df["ProductKey"] = sales_df["ProductKey"].astype(str)
    sales_df["ResellerKey"] = sales_df["ResellerKey"].astype(str)
    sales_df["LocalizationKey"] = sales_df["LocalizationKey"].astype(str)
    sales_df["SaleKey"] = sales_df["SaleKey"].astype(str)

    # convert dataframe in records
    records = list(sales_df.to_records(index=False))
    

    # insert records in table Sales_facts
    query = 'INSERT INTO "Sales_facts" (id_sale, quantity, unit_price, cost, id_product, id_reseller, id_date, id_localization) VALUES (CAST(%s AS INTEGER), CAST(%s AS INTEGER), CAST(%s AS DECIMAL), CAST(%s AS DECIMAL), CAST(%s AS INTEGER),CAST(%s AS INTEGER), %s, CAST(%s AS INTEGER))'
    cursor.executemany(query, records)






