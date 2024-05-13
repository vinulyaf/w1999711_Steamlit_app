
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import seaborn as sns

# Page Title 
st.title("MINGER DASHBOARD")

# Sales Overview
st.subheader("Sales Overview")

# loading data
data = pd.read_excel('GlobalSuperStore_Cleaned.xlsx')

# Creating filters 
st.sidebar.header('Filters')

# Filter by Date
st.sidebar.subheader('Date Filter')
startDate = pd.to_datetime(data['Order Date']).min()
endDate = pd.to_datetime(data['Order Date']).max()
start = pd.to_datetime(st.sidebar.date_input('Start date', startDate))
end = pd.to_datetime(st.sidebar.date_input('End date', endDate))
filtered_df = data[(data['Order Date'] >= start) & (data['Order Date'] <= end)].copy()

# Filter by Geography 
st.sidebar.subheader('Geographic Filters')
country = st.sidebar.multiselect('Select Country', data['Country'].unique())
region = st.sidebar.multiselect('Select Region', data['Region'].unique())
df_geo_filtered = filtered_df[filtered_df['Country'].isin(country) & filtered_df['Region'].isin(region)] if country or region else filtered_df

# Filter by Category and Sub-Category
st.sidebar.subheader('Category Filters')
category = st.sidebar.multiselect('Select Category', filtered_df['Category'].unique())
sub_category = st.sidebar.multiselect('Select Sub-Category', filtered_df['Sub-Category'].unique())
df_cat_filtered = filtered_df[filtered_df['Category'].isin(category) & filtered_df['Sub-Category'].isin(sub_category)] if category or sub_category else filtered_df

# Creating KPI
if 'Sales' in filtered_df.columns and 'Order ID' in filtered_df.columns:
    # Calculating  KPIs
    total_sales = filtered_df['Sales'].sum() / 1000000
    average_profit = filtered_df['Profit'].mean()
    total_orders = filtered_df['Order ID'].nunique()

    # Creating three columns
    col1, col2, col3 = st.columns((3), gap='medium')

    # Displaying the KPIs in each column
    with col1:
        st.metric(label="Total Sales", value=f"${total_sales:,.2f}M")
    with col2:
        st.metric(label="Average profit", value=f"${average_profit:,.2f}")
    with col3:
        st.metric(label="Total Orders", value=total_orders)
else:
    st.error("no column 'Sales' and 'Order ID'")

col1, col2, col3 = st.columns((3), gap='medium')
# Line chart for Sales over the years
#'Year' column is added to 'data' before creating 'filtered_df'
data['Year'] = data['Order Date'].dt.year
filtered_df = data[(data['Order Date'] >= start) & (data['Order Date'] <= end)].copy()
line_chart = filtered_df.groupby('Year')['Sales'].sum().reset_index()
fig1 = px.line(line_chart, x='Year', y='Sales', title='Sales Trend Over the Years')
fig1.update_traces(line=dict(color='yellow', width=3))
fig1.update_layout(width=400, height=400, xaxis=dict(tickmode='array', tickvals=line_chart['Year'], ticktext=line_chart['Year'].astype(str)))
col1.plotly_chart(fig1)

# Treemap for sales by region
region_sales = df_geo_filtered.groupby('Region')['Sales'].sum().reset_index()
fig4 = px.treemap(region_sales, path=['Region'], values='Sales', title='Sales Distribution by Region')
fig4.update_layout(width=400, height=400)
col3.plotly_chart(fig4)

# bar chart for Sales by Category 
category_sales = df_cat_filtered.groupby('Category')['Sales'].sum().reset_index()
fig2 = px.bar(category_sales, x='Category', y='Sales', title='Sales by Category', color='Category',
              color_discrete_map={'Furniture': 'blue', 'Office Supplies': 'light green', 'Technology': 'cyan'})
fig2.update_layout(width=400, height=400)
col1.plotly_chart(fig2)

# pie chart for Sales by Segment
segment_sales = filtered_df.groupby('Segment')['Sales'].sum().reset_index()
fig3 = px.pie(segment_sales, values='Sales', names='Segment', title='Distribution of Sales across Segments', color='Segment',
              color_discrete_map={'Consumer': 'maroon', 'Corporate': 'light blue', 'Home Office': 'orange'})
fig3.update_layout(width=400, height=400)
col3.plotly_chart(fig3)

# Area chart for Cumulative sales over time
cumulative_sales = filtered_df.groupby('Order Date')['Sales'].cumsum().reset_index()
fig5 = px.area(filtered_df, x='Order Date', y='Sales', title='Cumulative Sales Over Time',
              labels={'Cumulative Sales': 'Total Sales'}, color_discrete_sequence=['pink'])
fig5.update_layout(width=800, height=400)
st.plotly_chart(fig5)

# Sales and Profit analysis
st.subheader("Sales and Profit Analysis")
col1, col2, col3 = st.columns((3), gap='medium')

# Top 5 Profitable products
profit_by_product = filtered_df.groupby('Product Name')['Profit'].sum().reset_index()
# Sorting by profit in descending order
sorted_products = profit_by_product.sort_values('Profit', ascending=False)
top_5_products = sorted_products.head(5)
fig6 = px.bar(top_5_products, x='Product Name', y='Profit', title='Top 5 Profitable Products', color_discrete_sequence=['orange'])
fig6.update_layout(width=500, height=400)
col1.plotly_chart(fig6)

# Top 5 Sold products
sales_by_product = filtered_df.groupby('Product Name')['Sales'].sum().reset_index()
sorted_products = sales_by_product.sort_values('Sales', ascending=False)
top_5_products_sold = sorted_products.head(5)
fig7 = px.bar(top_5_products_sold, x='Product Name', y='Sales', title='Top 5 Sold Products', color_discrete_sequence=['Lightgreen'])
fig7.update_layout(width=500, height=400)
col3.plotly_chart(fig7)

# Correlation between sales and profit
fig8 = px.scatter(filtered_df, x='Sales', y='Profit', title='Sales and Profit Correlation', labels={'Sales': 'Sales', 'Profit': 'Profit ($)'}, color_discrete_sequence=['orchid'])
fig8.update_layout(width=500, height=400)
col1.plotly_chart(fig8)

# Pie chart for sales across markets
market_sales = df_geo_filtered.groupby('Market')['Sales'].sum().reset_index()
fig9 = px.pie(market_sales, values='Sales', names='Market', title='Distribution of Sales across Markets', color_discrete_sequence=['teal', 'lightskyblue', 'burlywood', 'maroon', 'gold', 'lightsalmon', 'purple'])
fig9.update_layout(width=500, height=400)
col3.plotly_chart(fig9)

# Line chart for Profit Trend over the years
line_chart = filtered_df.groupby('Year').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
fig10 = px.line(line_chart, x='Year')
fig10.add_scatter(x=line_chart['Year'], y=line_chart['Sales'], mode='lines', name='Sales')
fig10.add_scatter(x=line_chart['Year'], y=line_chart['Profit'], mode='lines', name='Profit')
fig10.update_layout(title='Sales and Profit Trends over The Years', width=800, height=400, xaxis=dict(tickmode='array', tickvals=line_chart['Year'], ticktext=line_chart['Year'].astype(str)))
col1.plotly_chart(fig10)

# Product analysis and Insights
st.subheader("Product Analysis and Insights")
col1, col2, col3 = st.columns((3), gap='medium')

# Market Basket Analysis
transaction = pd.get_dummies(filtered_df['Sub-Category'])
transaction = pd.concat([filtered_df['Order ID'], transaction], axis=1)
transaction = transaction.groupby('Order ID').sum()
transaction = transaction.applymap(lambda x: 1 if x > 0 else 0)
co_occurrence_matrix = transaction.T.dot(transaction)
np.fill_diagonal(co_occurrence_matrix.values, 0)
plt.figure(figsize=(10, 6))
sns.heatmap(co_occurrence_matrix, annot=True, cmap="YlGnBu", fmt="d", linewidths=2)
plt.title('Co-occurrence Matrix of Sub-Categories (Excluding Same Product Combinations)')
plt.xlabel('Sub-Category', color='White')
plt.ylabel('Sub-Category', color='white')
plt.style.use('dark_background')
st.pyplot(plt) 

# Scatterplot to see the relationship between quantity, sales and profit
sizes = filtered_df['Profit']
plt.figure(figsize=(15, 6))
plt.scatter(filtered_df['Sales'], filtered_df['Quantity'], s=sizes, alpha=0.4, color='khaki')
plt.title('Relationship Between Sales, Quantity, and Profit')
plt.xlabel('Sales ($)')
plt.ylabel('Quantity Sold')
plt.grid(True)
st.pyplot(plt) 

# Histogram to check the distribution of Order Sizes 
plt.figure(figsize=(10, 6))
plt.hist(filtered_df['Quantity'], bins=range(1, filtered_df['Quantity'].max() + 2), color='mediumslateblue', alpha=0.7, edgecolor='black')
plt.title('Distribution of Order Sizes')
plt.xlabel('Quantity Per Order')
plt.ylabel('Frequency')
plt.xticks(range(1, filtered_df['Quantity'].max() + 1))
plt.grid(True)
st.pyplot(plt)
