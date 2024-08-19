import streamlit as st
from src.data_loader import read_data_from_s3
import plotly.express as px
import awswrangler as wr
import plotly.express as px
st.title("Streams of Data Streamlit Example")

st.header("Data from S3-2")
df = wr.s3.read_parquet("s3://de-sales-data-project-data-lake-146479615822/sales_data/")


st.dataframe(df)

df['Product_Category'] = df['Product_Category'].apply(
    lambda x: 'Nest' if 'Nest' in x else x
)

# Calculate total spend by product category and sort in descending order
category_spend = df.groupby('Product_Category')['Total_Spend'].sum().reset_index()
category_spend = category_spend.sort_values(by='Total_Spend', ascending=False)

# Define your color map for the product categories using solid colors
color_map = {
    'Nest': '#C9D788',  # Light greenish-yellow
    'Category A': '#C9D788',  # Light greenish-yellow
    'Category B': '#c0ca47',  # Medium light variant
    'Category C': '#85C1E9',  # Light blue
    'Category D': '#3498DB',  # Medium blue
    'Category E': '#06275b'   # Dark blue
    # Add more categories as needed with their corresponding colors
}

# Create the bar chart using Plotly
fig = px.bar(
    category_spend,
    x='Product_Category',
    y='Total_Spend',
    title='Total Spend by Product Category',
    labels={'Total_Spend': 'Total Spend (in millions)', 'Product_Category': 'Product Category'},
    text='Total_Spend',
    width=1200, height=1000,
    color='Product_Category',
    color_discrete_map=color_map
)

# Update layout and styling
fig.update_layout(
    plot_bgcolor='white',
    title_text='Total Spend by Product Category',
    title_x=0.5,
    xaxis_title='Product Category',
    yaxis_title='Total Spend (in millions)',  # Clarified that the y-axis is in millions
    yaxis=dict(tickformat='.2f'),  # Adjust the tick format if necessary
    legend_title_text='Product Categories'
)

# Add data labels to the bars with specific styling
fig.update_traces(
    texttemplate='%{text:.2f}', 
    textposition='outside',
    textfont=dict(color='black')  # Set text color to black for better readability
)

# Display the Plotly chart in the Streamlit app
st.plotly_chart(fig)