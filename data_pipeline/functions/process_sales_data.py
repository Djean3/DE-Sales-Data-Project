import os

import awswrangler as wr
from helpers.datacleaning import drop_na, rename_avg_price_to_price, remove_trailing_zeros_from_df, update_online_spend_with_quantity, total_spend

def process_sales_function(event, context):
    df = wr.s3.read_csv(
        "s3://de-sales-data-project-raw-data-146479615822/Online_Shopping_Dataset.csv"
    )
    df = drop_na(df)
    df = rename_avg_price_to_price(df)
    df = df.drop(columns=["Unnamed: 0", "Date"])
    df = remove_trailing_zeros_from_df(df)
    df = update_online_spend_with_quantity(df)
    df = total_spend(df)
    wr.s3.to_parquet(df, "s3://de-sales-data-project-data-lake-146479615822/sales_data/processed_file.parquet")
    return {"status": "success", "message": "hello world"}


    
    