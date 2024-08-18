import streamlit as st
from src.data_loader import read_data_from_s3
import plotly.express as px
import awswrangler as wr

st.title("Streams of Data Streamlit Example")

st.header("Data from S3-2")
df = wr.s3.read_parquet("s3://de-sales-data-project-data-lake-146479615822/sales_data/")


st.dataframe(df)