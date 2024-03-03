import os

import awswrangler as wr
from aws_lambda_powertools import Logger
from helpers.datacleaning import drop_na, rename_avg_price_to_price


logger = Logger(level=os.environ["LOG_THRESHOLD"])


def process_sales_data(event, context):
    df = wr.s3.read_csv(
        "s3://de-sales-data-project-raw-data-146479615822/Online_Shopping_Dataset.csv"
    )
    df = drop_na(df)
    df = rename_avg_price_to_price(df)
    df = df.drop(columns=["Unnamed: 0", "Date"])
    return {"status": "success", "message": "hello world"}
