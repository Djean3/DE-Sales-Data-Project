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


def remove_trailing_zeros_from_df(df):
    """remove trailing zeros from float columns in dataframe

    Args:
        df (_type_): The DataFrame from which trailing zeros in float columns will be removed. It is modified in place.


    Returns:
        _type_: The DataFrame with trailing zeros removed from float columns. Note that this is the same DataFrame object passed as the argument, modified in place.
    """
    for col in df.columns:
        # Check if the column is a float dtype
        if df[col].dtype == float:
            # Use apply to convert float to int if it's an integer, else leave as float
            df[col] = df[col].apply(lambda x: int(x) if x.is_integer() else x)
    return df


def update_online_spend_with_quantity(df):
    """Updates the "Online_Spend" column in a DataFrame with cumulative spending amounts per customer, factoring in the quantity of each transaction.

    This function sorts the input DataFrame by "CustomerID", "Transaction_Date", and "Transaction_ID" to ensure chronological processing of transactions. For each transaction, it calculates the spending by multiplying the "Price" by the "Quantity". It then updates the "Online_Spend" for each customer cumulatively, adding the calculated spend to the customer's previous total spend stored in a dictionary. The updated "Online_Spend" values are then mapped back to the original DataFrame.

    Args:
        df (pandas.DataFrame): A DataFrame containing at least the columns "CustomerID", "Transaction_Date", "Transaction_ID", "Price", "Quantity", and "Online_Spend". It's expected that "Price" and "Quantity" are numeric.

    Returns:
        _type_: pandas.DataFrame: The original DataFrame with the "Online_Spend" column updated to reflect the cumulative spending amount per customer, taking into account the quantity of each transaction.
    """
    # Create a copy to sort without changing the original DataFrame's order
    df_sorted = df.sort_values(
        by=["CustomerID", "Transaction_Date", "Transaction_ID"]
    ).copy()

    # Initialize a dictionary to keep track of the last Online_Spend for each customer
    last_online_spend = {}

    # Calculate the new Online_Spend values and store them in a list
    new_online_spends = []

    for index, row in df_sorted.iterrows():
        customer_id = row["CustomerID"]
        # Calculate the spend for this transaction, taking Quantity into account
        transaction_spend = row["Price"] * row["Quantity"]

        if customer_id in last_online_spend:
            # Update the Online_Spend for the current purchase by adding the transaction spend
            new_spend = last_online_spend[customer_id] + transaction_spend
        else:
            # If it's the first purchase, initialize Online_Spend with this transaction's spend
            new_spend = transaction_spend

        # Update the last Online_Spend for this customer
        last_online_spend[customer_id] = new_spend
        # Append the updated Online_Spend value to the list
        new_online_spends.append(new_spend)

    # Map the new Online_Spend values back to the original DataFrame using the index from the sorted copy
    for original_idx, sorted_idx in enumerate(df_sorted.index):
        df.at[sorted_idx, "Online_Spend"] = new_online_spends[original_idx]

    return df


def total_spend(df):
    """Adds new column: Total spend

    Args:
        df (pandas.DataFrame): The DataFrame to calculate total spend for, must include "Offline_Spend", "Online_Spend", and "Delivery_Charges" columns.


    Returns:
        pandas.DataFrame: The DataFrame with an added "Total Spend" column, reflecting the sum of offline and online spends plus delivery charges for each transaction.
    """
    # Correct the Total Spend calculation
    df["Total Spend"] = (
        df["Offline_Spend"] + df["Online_Spend"] + df["Delivery_Charges"]
    )

    return df
