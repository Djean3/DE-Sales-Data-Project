import streamlit as st
from src.data_loader import read_data_from_s3
import plotly.express as px
import awswrangler as wr
import plotly.express as px
st.title("Streams of Data Streamlit Example")

st.header("Data from S3-2")
df = wr.s3.read_parquet("s3://de-sales-data-project-data-lake-146479615822/sales_data/")



##################### Cleaning#####################

df = df.drop(columns=['Total_Spend', 'Offline_Spend', 'Online_Spend'])
df['Final_Price'] = df.apply(lambda row: 
                             ((row['Price'] - (row['Price'] * (row['Discount_pct'] / 100))) * (1 + row['GST']) if row['Coupon_Status'] == 'Used' 
                              else row['Price'] * (1 + row['GST'])) + 
                             row['Delivery_Charges'], 
                             axis=1)
df['Final_Price'] = df['Final_Price'].round(2)



st.dataframe(df)
#########################################################################

# Group all 'Nest' related categories into one


#df['Product_Category'] = df['Product_Category'].apply(
#    lambda x: 'Nest' if 'Nest' in x else x
#)

# Calculate total spend by summing the 'Price' column for each product category and sort in descending order
category_spend = df.groupby('Product_Category')['Price'].sum().reset_index()
category_spend = category_spend.sort_values(by='Price', ascending=False)

# Define your color map for the product categories using solid colors
color_map = {
    'Nest': '#85C1E9',  # Light blue
    'Category A': '#AED6F1',  # Very light blue
    'Category B': '#5DADE2',  # Medium light blue
    'Category C': '#3498DB',  # Medium blue
    'Category D': '#2E86C1',  # Medium-dark blue
    'Category E': '#1B4F72'   # Dark blue
    # Add more categories as needed with their corresponding blue shades
}

# Create the bar chart using Plotly
fig = px.bar(
    category_spend,
    x='Product_Category',
    y='Price',
    title='Total Spend by Product Category',
    labels={'Price': 'Total Spend', 'Product_Category': 'Product Category'},
    text='Price',
    width=1200, height=1000,
    color='Product_Category',
    color_discrete_map=color_map
)

# Update layout and styling
fig.update_layout(
    plot_bgcolor='white',
    title_text='YTD Total Spend by Product Category',
    title_x=0.5,
    xaxis_title='Product Category',
    yaxis_title='Total Spend ($)',  # Reflects that the y-axis is now in dollars
    yaxis=dict(
        tickformat=',.0f',  # Format ticks as thousands with commas
        tickprefix="$"  # Add dollar sign prefix
    ),
    legend_title_text='Product Categories'
)

# Add data labels to the bars with specific formatting and styling
fig.update_traces(
    texttemplate='%{text:$,.0f}',  # Format labels with dollar sign and commas
    textposition='outside',
    textfont=dict(color='black')  # Set text color to black for better readability
)

# Display the Plotly chart in the Streamlit app
st.plotly_chart(fig)