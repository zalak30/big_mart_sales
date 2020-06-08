# import required libraries
import pandas as pd

# visualization libraries
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

# read csv file
data = pd.read_csv('data_test.csv')

# check column
print(data.columns)

# check DataFrame size
shape = data.shape
print("\nnumber of rows : {0}, number of columns : {1}".format(shape[0], shape[1]))

# check for missing or null values
print("\n", data.isnull().any())
print("\nTotal numbers of missing values in column 'Item_Weight':{}".format(data['Item_Weight'].isnull().sum()))
print("Total numbers of missing values in column 'Outlet_Size':{}".format(data['Outlet_Size'].isnull().sum()))
print("\nDF info", data.info())
print("\nDF describe", data.describe())

# missing values in 'outlet_size'
print(data['Outlet_Size'].value_counts())
print(data['Outlet_Identifier'].value_counts())
print(data['Outlet_Type'].value_counts())

# check correlation of columns with each other
corrMatrix = data.corr()
# sns.heatmap(corrMatrix, annot=True)
# plt.show()
# we can see 'Item_MRP' is more correlated to 'Item_Sales' than any other column i.e 0.57


# histogram('Item_MRP')
# fig = px.histogram(data, x="Item_MRP")
# fig.show()
# mrp distribute between 30 to 270

# let's check mean of 'item weight' in different range of 'item mrp'
print("\nmean of 'item weight' in different range of 'item mrp'")
print(data[(data['Item_MRP'] >= 30) & (data['Item_MRP'] <= 50)][['Item_MRP', 'Item_Weight']].mean())
print(data[(data['Item_MRP'] > 50) & (data['Item_MRP'] <= 100)][['Item_MRP', 'Item_Weight']].mean())
print(data[(data['Item_MRP'] > 100) & (data['Item_MRP'] <= 150)][['Item_MRP', 'Item_Weight']].mean())
print(data[(data['Item_MRP'] > 150) & (data['Item_MRP'] <= 200)][['Item_MRP', 'Item_Weight']].mean())
print(data[(data['Item_MRP'] > 200) & (data['Item_MRP'] <= 270)][['Item_MRP', 'Item_Weight']].mean())
# from above data we can see in all range weight mean is 12 point something

# so now for NaN values in column 'Item weight' we can replace with 12.00
data.fillna({'Item_Weight': 12.00}, inplace=True)

# scatter chart('Outlet_Location_Type' / 'Outlet_Size')
fig = px.scatter(data, x='Outlet_Size', y='Outlet_Type')
fig.show()
fig = px.scatter(data, x='Outlet_Location_Type', y='Outlet_Size')
fig.show()
# from above scatter plot we can say if 'Supermarket type 2' and 'Supermarket type 3'
# then it's always 'medium' in 'outlet size', if it's 'Grocery Store' then it's always 'Small',
# if 'Outlet_Location_Type' is 'Tier 2' then it's always 'Small' in 'Outlet_Size'


def impute_size(cols):
    Outlet_Size = cols[0]
    Outlet_Type = cols[1]
    Outlet_Location_Type = cols[2]

    if pd.isnull(Outlet_Size):

        if Outlet_Type == 'Supermarket Type2':
            return 'Medium'
        elif Outlet_Type == 'Grocery Store':
            return 'Small'
        elif Outlet_Location_Type == 'Tier 2':
            return 'Small'
    else:
        return Outlet_Size


# apply function
data['Outlet_Size'] = data[['Outlet_Size', 'Outlet_Type', 'Outlet_Location_Type']].apply(impute_size, axis=1)

# no missing values in DF

# bar chart (Outlet_Type/Item_Outlet_Sales)
# fig = px.scatter(data, x='Item_MRP', y='Item_Outlet_Sales')
# fig.show()

fig = px.box(data, x='Outlet_Size', y='Item_Outlet_Sales')
fig.show()
