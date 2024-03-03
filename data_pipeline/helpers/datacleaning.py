import pandas as pd
import awswrangler as wr


def drop_na(df):
    """Drop na values from dataframe

    Args:
        df (dataframe): sales data dataframe

    Returns:
        dataframe: sales data dataframe with na values dropped
    """
    clean_data = df.dropna()
    return clean_data


def rename_avg_price_to_price(df):
    """rename 'Avg_Price' column to 'Price'

    Args:
        df (dataframe): sales data dataframe

    Returns:
        dataframe: df with updated column name
    """
    df_renamed = df.rename(columns={"Avg_Price": "Price"})
    return df_renamed
