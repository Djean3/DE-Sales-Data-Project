import os

import awswrangler as wr
from helpers.datacleaning import drop_na, assign_region, extract_state, drop_bad_addresses

def process_sales_function(event, context):
    df = wr.s3.read_csv(
        "s3://de-sales-data-project-raw-data-146479615822/Online_Shopping_Dataset.csv"
    )
    df = drop_na(df)
    df = drop_bad_addresses(df)
    df = extract_state(df)
    df = assign_region(df)    
    table_name = "sales_data"
    wr.s3.to_parquet(
        df, 
        path = f"s3://de-sales-data-project-data-lake-146479615822/{table_name}/",
                dataset=True,
                mode="overwrite",
                table=table_name,
                database="data_lake",
                #mode="overwrite_partitions",
                #partition_cols=["Year", "Month"],
                )
    #run this is a jupyter notebook and make the new tables
    return {"status": "success", "message": "hello world"}


    
    