import streamlit as st
from src.data_loader import read_data_from_s3
import awswrangler as wr
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
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


#####################################
grouped_df = df.groupby(['Location', 'Gender'])['Final_Price'].sum().reset_index()

# Sort the data by total sales (Final_Price) in descending order
grouped_df = grouped_df.sort_values(by='Final_Price', ascending=True)

# Define your color map with shades of blue and green
color_sequence = ['#3498DB', '#2ECC71']  # Blue for Male, Green for Female

# Create the horizontal stacked bar chart
fig = px.bar(
    grouped_df, 
    y='Location',  # Change to y for horizontal bars
    x='Final_Price', 
    color='Gender', 
    title='Total Sales by Location and Gender',
    labels={'Final_Price': 'Total Sales', 'Location': 'Region'},
    text='Final_Price',
    barmode='stack',
    orientation='h',  # Horizontal orientation
    height=600,
    width=1000,
    color_discrete_sequence=color_sequence  # Apply the color sequence
)

# Update the layout for better readability
fig.update_layout(
    plot_bgcolor='white',
    yaxis_title='Location (Region)',
    xaxis_title='Total Sales',
    title_x=0.5,
    legend_title_text='Gender'
)

# Add data labels to the bars
fig.update_traces(texttemplate='%{text:$,.2f}', textposition='inside')

# Display the Plotly chart in the Streamlit app (or just show it if running standalone)
st.plotly_chart(fig) 


#######################################


# Ensure the 'Transaction_Date' column is in datetime format
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])

# Group the data by Transaction_Date to calculate total sales per day
daily_sales = df.groupby('Transaction_Date')['Final_Price'].sum().reset_index()

# Calculate a 7-day rolling average for smoothing
daily_sales['7_day_avg'] = daily_sales['Final_Price'].rolling(window=7).mean()

# Set the seaborn style for the plot
sns.set(style="whitegrid")

# Create the plot with a wider figure size
plt.figure(figsize=(24, 12))

# Plot daily sales
sns.lineplot(x='Transaction_Date', y='Final_Price', data=daily_sales, label='Daily Sales', color='royalblue')

# Plot the 7-day rolling average in red
sns.lineplot(x='Transaction_Date', y='7_day_avg', data=daily_sales, label='7-Day Rolling Average', color='red', linestyle='--')

# Set the title and labels
plt.title('Sales Over Time', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Total Sales', fontsize=14)
plt.legend(title='Metrics')

# Rotate date labels for better readability
plt.xticks(rotation=45)

# Set x-axis major ticks to every month
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

# Adjust layout
plt.tight_layout()

# Display the plot in Streamlit
st.pyplot(plt)


###################################################

# Step 1: Map the Coupon_Status to the desired categories
status_mapping = {
    'Clicked': 'Clicked (Not Used)',
    'Used': 'Used',
    'Not Used': 'Not Opened'
}
df['Coupon_Status'] = df['Coupon_Status'].map(status_mapping)

# Step 2: Convert Discount_pct to a categorical type with a specific order
discount_order = [10, 20, 30]
df['Discount_pct'] = pd.Categorical(df['Discount_pct'], categories=discount_order, ordered=True)

# Step 3: Define the custom order for Coupon_Status
status_order = pd.Categorical(df['Coupon_Status'], categories=["Clicked (Not Used)", "Used", "Not Opened"], ordered=True)
df['Coupon_Status'] = status_order

# Step 4: Count the number of times each coupon was used or not used
sunburst_df = df.groupby(['Coupon_Status', 'Discount_pct']).size().reset_index(name='Count')

# Ensure that the order of Discount_pct is preserved by sorting
sunburst_df = sunburst_df.sort_values(by=['Coupon_Status', 'Discount_pct'], ascending=[True, True])

# Step 5: Modify the labels for clarity
sunburst_df['label'] = 'Discount: ' + sunburst_df['Discount_pct'].astype(str) + '%'

# Step 6: Create the sunburst chart
fig = px.sunburst(
    sunburst_df, 
    path=['Coupon_Status', 'label'], 
    values='Count',  # Use count of occurrences instead of total spend
    color='Count',
    color_continuous_scale=px.colors.sequential.YlOrRd_r[::-1],
    height=800
)

# Remove the color bar if not necessary
fig.update_layout(coloraxis_showscale=False)

# Update the figure layout and labels
fig.update_traces(textinfo='label+percent entry', textfont_size=18)
fig.update_layout(
    title_text='Coupon Usage by Discount Percentage',
    title_font_size=25,
    title_x=0.5,
    plot_bgcolor='white'
)

# Display the Plotly chart in the Streamlit app
st.plotly_chart(fig)
#fig.show()

#########################################