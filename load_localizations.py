import pandas as pd


def load_localizations(cursor):
    # load resellers data
    resellers_df = pd.read_csv('data/reseller.csv', sep='\t')

    # keep the 3 columns that we need and drop duplicates
    localizations_df = resellers_df.loc[:, ["Country-Region", "State-Province", "City"]].drop_duplicates()


    # add column localization_key
    localizations_df = localizations_df.reset_index(drop=True).reset_index().rename(columns={'index': 'LocalizationKey'})
    localizations_df['LocalizationKey'] += 1

    

    # Convert data to load it in postgres
    localizations_df["LocalizationKey"] = localizations_df["LocalizationKey"].astype(str)

    # convert dataframe in records
    records = list(localizations_df.to_records(index=False))

    # insert records in table Localization_dim
    query = 'INSERT INTO "Localization_dim" (id_localization, country, state, city) VALUES (CAST(%s AS INTEGER), %s, %s, %s)'
    cursor.executemany(query, records)


