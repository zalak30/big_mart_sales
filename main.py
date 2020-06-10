# import required libraries
import pandas as pd

# visualization libraries
import plotly.express as px

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
data['Item_MRP'] = data['Item_MRP'].apply(lambda x: round(x))

# check correlation of columns with each other
corrMatrix = data.corr()
fig = px.imshow(corrMatrix, x=corrMatrix.columns, y=corrMatrix.columns)
fig.show()
# we can see 'Item_MRP' is more correlated to 'Item_Sales' than any other column i.e 0.57

# histogram('Item_MRP')
fig = px.histogram(data, x="Item_MRP")
fig.show()
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


def impute_size(cols):
    outlet_size = cols[0]
    outlet_type = cols[1]
    outlet_location_type = cols[2]

    if pd.isnull(outlet_size):

        if outlet_type == 'Supermarket Type2':
            return 'Medium'
        elif outlet_type == 'Grocery Store':
            return 'Small'
        elif outlet_location_type == 'Tier 2':
            return 'Small'
    else:
        return outlet_size


# apply function
data['Outlet_Size'] = data[['Outlet_Size', 'Outlet_Type', 'Outlet_Location_Type']].apply(impute_size, axis=1)

# no missing values in DF

# box chart (Outlet_Size/Item_Outlet_Sales)
fig = px.box(data, x='Outlet_Size', y='Item_Outlet_Sales')
fig.show()
# from above box plot, 'Medium' size outlet has most sales , followed by 'High' and 'Small' outlet

# scatter chart('Outlet_Size' / 'Outlet_Size')
fig = px.scatter(data, x='Outlet_Size', y='Outlet_Type')
fig.show()
# from above scatter plot, if 'Supermarket type 2' and 'Supermarket type 3'
# then it's always 'medium' in 'outlet size', if it's 'Grocery Store' then it's always 'Small'

# scatter chart('Outlet_Location_Type' / 'Outlet_Size')
fig = px.scatter(data, x='Outlet_Location_Type', y='Outlet_Size')
fig.show()
# if 'Outlet_Location_Type' is 'Tier 2' then it's always 'Small' in 'Outlet_Size', if 'Outlet_size' is 'High' then it's
# always 'Tier3'

# scatter plot (Outlet_Size/Item_Outlet_Sales)
fig = px.scatter(data, x="Outlet_Size", y="Outlet_Type", size="Item_Outlet_Sales", color="Item_MRP",
                 hover_name="Item_Outlet_Sales", size_max=60)
fig.show()
# 'supermarket type3' which is 'Medium' in size has most sales, most items cost range between
# 100 to 200, and some products worth '250 bucks' also got sold
# Most High MRP items sold in 'Supermarket Type1' which is 'High' in size.
# low range products sold in 'Supermarket Type1' which is 'Medium' in size
# 'Supermarket Type1' which is 'Small' in size has sales of all range of products but store's total
#                   sales is not so impressive
