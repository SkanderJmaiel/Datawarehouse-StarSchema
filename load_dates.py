import pandas as pd

# get the quarter from the month
def get_quarter(month):
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4

def load_dates(cursor):
    # load sales data
    sales_df = pd.read_csv('data/sales.csv', sep='\t')

    # get unique dates
    dates = sales_df.OrderDate.unique()

    # transform to datetime format
    dates = pd.to_datetime(dates)

    #create de the dataframe
    dates_df = pd.DataFrame({'day': dates.day,
                            'month': dates.month,
                            'year': dates.year,
                            'day_of_the_week': dates.day_name()})

    # add date_id column
    dates_df['date_id'] = dates.strftime('%d/%m/%Y')

    # add quarter column
    dates_df['quarter'] = dates_df['month'].apply(get_quarter)

    
    # Convert data to load it in postgres
    dates_df["day"] = dates_df["day"].astype(str)
    dates_df["month"] = dates_df["month"].astype(str)
    dates_df["year"] = dates_df["year"].astype(str)
    dates_df["quarter"] = dates_df["quarter"].astype(str)

    # convert dataframe in records
    records = list(dates_df.to_records(index=False))

    # insert records in table Date_dim
    query = 'INSERT INTO "Date_dim" (day, month, year, day_of_the_week, id_date, quarter) VALUES (CAST(%s AS INTEGER), CAST(%s AS INTEGER), CAST(%s AS INTEGER), %s, CAST(%s AS date), CAST(%s AS INTEGER))'
    cursor.executemany(query, records)


    




