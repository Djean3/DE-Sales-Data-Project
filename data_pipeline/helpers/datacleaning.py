import pandas as pd
import awswrangler as wr
from datetime import datetime, timedelta
import random

def generate_sales_data(df, start_date=None, end_date=None, current_day_only=False):
    if start_date is None:
        start_date = datetime.today().strftime("%Y-%m-%d")
    if end_date is None:
        end_date = datetime.today().strftime("%Y-%m-%d")
    bean_types, purchase_prices, sell_prices = get_bean_data()

    # Load customers and their addresses
    
    
    #df = df[["Customer", "Address"]].dropna().drop_duplicates()
    customers = df.to_dict("records")

    # Handle date range
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    if current_day_only:
        today = datetime.today().date()
        start_date = end_date = datetime.combine(today, datetime.min.time())

    data = []
    current_date = start_date

    while current_date <= end_date:
        for customer in customers:
            if random.random() < 0.7:  # 70% chance they make an order
                bean_type = random.choice(bean_types)
                amount_purchased = random.randint(500, 5000)

                purchase_price = purchase_prices.get(bean_type, 0)
                sell_price = sell_prices.get(bean_type, 0)
                total_purchase_cost = round(amount_purchased * purchase_price, 2)
                total_sell_price = round(amount_purchased * sell_price, 2)
                profit = round(total_sell_price - total_purchase_cost, 2)

                data.append({
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Customer": customer["Customer"],
                    "Address": customer["Address"],
                    "Bean Type": bean_type,
                    "Amount Purchased (lbs)": amount_purchased,
                    "Purchase Cost ($)": total_purchase_cost,
                    "Sell Price ($)": total_sell_price,
                    "Profit ($)": profit
                })

        current_date += timedelta(days=1)

    return pd.DataFrame(data)



def get_bean_data():
    bean_types = [
        "Black Beans", "Pinto Beans", "Kidney Beans", "Chickpeas", "Lentils",
        "Navy Beans", "Adzuki Beans", "Mung Beans", "Soybeans", "Great Northern Beans",
        "Fava Beans", "Cranberry Beans", "Cannellini Beans", "Butter Beans",
        "Green Peas", "Yellow Peas", "Split Peas", "Red Beans", "White Beans",
        "Borlotti Beans", "Anasazi Beans", "Flageolet Beans", "Marrow Beans",
        "Tepary Beans", "Beluga Lentils", "Puy Lentils", "Horse Beans",
        "Black Eyed Peas", "Tarbais Beans", "Val Beans", "Scarlet Runner Beans",
        "Pink Beans", "Calypso Beans", "Dragon Tongue Beans", "Jacob’s Cattle Beans"
    ]

    # Purchase prices per pound
    purchase_price_per_pound = {
        "Black Beans": 0.32, "Pinto Beans": 0.30, "Kidney Beans": 0.38, "Chickpeas": 0.35,
        "Lentils": 0.28, "Navy Beans": 0.34, "Adzuki Beans": 0.70, "Mung Beans": 0.65,
        "Soybeans": 0.25, "Great Northern Beans": 0.35, "Fava Beans": 0.55, "Cranberry Beans": 0.75,
        "Cannellini Beans": 0.50, "Butter Beans": 0.45, "Green Peas": 0.25, "Yellow Peas": 0.22,
        "Split Peas": 0.20, "Red Beans": 0.38, "White Beans": 0.35, "Borlotti Beans": 0.85,
        "Anasazi Beans": 1.00, "Flageolet Beans": 1.25, "Marrow Beans": 1.10, "Tepary Beans": 1.30,
        "Beluga Lentils": 1.00, "Puy Lentils": 1.10, "Horse Beans": 0.55, "Black Eyed Peas": 0.40,
        "Tarbais Beans": 1.60, "Val Beans": 1.50, "Scarlet Runner Beans": 1.65, "Pink Beans": 0.45,
        "Calypso Beans": 1.20, "Dragon Tongue Beans": 1.50, "Jacob’s Cattle Beans": 1.25
    }

    # Sell prices with markup based on category
    sell_price_per_pound = {
        # Commodity Beans (2.5x markup)
        bean: round(purchase_price_per_pound[bean] * 3, 2) for bean in [
            "Black Beans", "Pinto Beans", "Kidney Beans", "Chickpeas", "Lentils",
            "Navy Beans", "Soybeans", "Green Peas", "Yellow Peas", "Split Peas",
            "Red Beans", "White Beans", "Black Eyed Peas", "Pink Beans"
        ]
    }
    
    # Mid-Tier Beans (3x markup)
    mid_tier_beans = ["Adzuki Beans", "Mung Beans", "Great Northern Beans", "Fava Beans",
                      "Cranberry Beans", "Cannellini Beans", "Butter Beans", "Horse Beans", "Borlotti Beans"]
    sell_price_per_pound.update({bean: round(purchase_price_per_pound[bean] * 3, 2) for bean in mid_tier_beans})

    # Specialty/Heirloom Beans (3.5x to 4x markup)
    specialty_beans = {
        "Anasazi Beans": 3.5, "Flageolet Beans": 3.5, "Marrow Beans": 3.5, "Tepary Beans": 3.5,
        "Beluga Lentils": 3.5, "Puy Lentils": 3.5, "Val Beans": 3.5, "Scarlet Runner Beans": 3.5,
        "Calypso Beans": 3.5, "Dragon Tongue Beans": 3.5, "Jacob’s Cattle Beans": 3.5,
        "Tarbais Beans": 4
    }
    sell_price_per_pound.update({
        bean: round(purchase_price_per_pound[bean] * specialty_beans[bean], 2)
        for bean in specialty_beans
    })

    return bean_types, purchase_price_per_pound, sell_price_per_pound




def drop_na(df):
    """Drop na values from dataframe

    Args:
        df (dataframe): sales data dataframe

    Returns:
        dataframe: sales data dataframe with na values dropped
    """
    clean_data = df.dropna()
    clean_data = clean_data[(clean_data != 0).all(axis=1)]
    return clean_data


def drop_bad_addresses(df):
    """
    Removes rows where the Address column does not start with a number.
    Assumes the column is named 'Address'.
    """
    return df[df["Address"].astype(str).str.match(r"^\d+")]


def extract_state(df):
    """
    Extracts the state abbreviation from the 'Address' column and adds it as a new 'State' column.

    Parameters:
        df (pd.DataFrame): DataFrame containing an 'Address' column.

    Returns:
        pd.DataFrame: DataFrame with an added 'State' column.
    """
    # Use regular expression to extract the state abbreviation (two uppercase letters)
    df['State'] = df['Address'].str.extract(r',\s*([A-Z]{2})\b')
    return df


def assign_region(df):
    region_map = {
        # North East
        "ME": "North East", "NH": "North East", "VT": "North East",
        "MA": "North East", "RI": "North East", "CT": "North East",

        # Mid-Atlantic
        "NY": "Mid-Atlantic", "NJ": "Mid-Atlantic", "PA": "Mid-Atlantic",
        "DE": "Mid-Atlantic", "MD": "Mid-Atlantic",

        # South East
        "VA": "South East", "WV": "South East", "KY": "South East", "NC": "South East",
        "SC": "South East", "GA": "South East", "FL": "South East",
        "AL": "South East", "MS": "South East", "TN": "South East", "AR": "South East", "LA": "South East",

        # Mid-West
        "ND": "Mid-West", "SD": "Mid-West", "NE": "Mid-West", "KS": "Mid-West",
        "MN": "Mid-West", "IA": "Mid-West", "MO": "Mid-West",
        "WI": "Mid-West", "IL": "Mid-West", "IN": "Mid-West", "MI": "Mid-West", "OH": "Mid-West",

        # South West
        "TX": "South West", "OK": "South West", "NM": "South West", "AZ": "South West",

        # North West
        "MT": "North West", "ID": "North West", "WY": "North West",
        "WA": "North West", "OR": "North West",

        # West
        "CA": "West", "NV": "West", "UT": "West", "CO": "West",

        # Outliers
        "AK": "West", "HI": "West", "DC": "Mid-Atlantic"  # DC was near MD/VA
    }

    df["Region"] = df["State"].map(region_map).fillna("Unknown")
    return df


