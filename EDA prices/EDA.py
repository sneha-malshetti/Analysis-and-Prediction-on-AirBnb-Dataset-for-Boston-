
# coding: utf-8

# In[7]:


import boto3
from boto.s3.connection import S3Connection
import os
import json
import boto.s3
import sys
import datetime
from boto.s3.key import Key
import pandas as pd
import pylab
import csv
import io
import requests
import time
import json
import seaborn as sns
import scipy
import numpy as np
import glob
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime
from collections import Counter
from pylab import *
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm



## Importing JSON File contents
with open('configEDA.json') as data_file:
    data = json.load(data_file)

AWSAccess=data["AWSAccess"]
AWSSecret=data["AWSSecret"]



# edadata= pd.read_csv('cleanlisting.csv')
# print(Airbnb_df.head(5))



# In[9]:




link="https://s3.amazonaws.com/adsteam8finalairbnb/CleanData/cleanlisting.csv"
Airbnb_df =  pd.read_csv(link,low_memory=False)

print(Airbnb_df.shape)



# edadata= pd.read_csv('cleanlisting.csv',encoding = 'utf-8')
# print(edadata.head(5))

        
     

 


# In[10]:

import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2

get_ipython().magic(u'matplotlib inline')


# In[ ]:

edadata=Airbnb_df


# In[7]:

# Categorizing differernt listings based on room_type


#how many types of room 
roomTyp=edadata.groupby('room_type').id.count()
roomTyp=roomTyp.reset_index()
roomTyp=roomTyp.rename(columns={'id':'number_Of_Listings'})
roomTyp


# In[59]:

#the number of listings based upon room type.Visualizing 
get_ipython().magic(u'matplotlib inline')

import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

room = edadata.room_type
r = Counter(room)

rooms = pd.DataFrame.from_dict(r, orient='index').sort_values(by=0)
rooms.columns = ['room_type']
rooms.plot.pie(y = 'room_type', 
                 colormap = 'pink_r', 
                 figsize=(5,5), 
                 fontsize = 10, autopct = '%.2f',
                 legend = False,
                 title = 'Room Type Distribution')


# In[6]:

print(edadata.shape)
print(edadata['price'].mean())


# In[ ]:




# In[7]:

#price o various venur availbale  
# analyzing the prices for different room type and property type

venueproperty = edadata.groupby(['property_type','room_type']).price.mean()
venueproperty = venueproperty.reset_index()
venueproperty=venueproperty.sort_values('price',ascending=[0])
venueproperty.head()


# In[67]:

# heat map

#Plotting the same on a heatMap

import seaborn as sns

plt.figure(figsize=(10,10))
sns.heatmap(edadata.groupby([
        'property_type', 'room_type']).price.mean().unstack(),annot=True, fmt=".0f") #string format 


# In[41]:

#additional amenities costs more ?
dryerdf = edadata.groupby(['Dryer','Washer' ]).price.mean()
tvdf = edadata.groupby(['bathrooms','beds' ]).price.mean()


tvdf = tvdf.reset_index()

dryerdf = dryerdf.reset_index()


tvdf=tvdf.sort_values('price',ascending=[0])
dryerdf=dryerdf.sort_values('price',ascending=[0])

print(tvdf.head())
dryerdf.head()



# In[69]:

##coordinates for plotting 

long_max = edadata['longitude'].max() + .02
long_min = edadata['longitude'].min() -.02
mid_long = (edadata['longitude'].min() + edadata['longitude'].max())/2

lat_max = edadata['latitude'].max() + .02
lat_min = edadata['latitude'].min() - .02
mid_lat = (edadata['latitude'].min() + edadata['latitude'].max())/2

## map
m = Basemap(projection='cyl',lat_0=mid_lat,lon_0=mid_long,            llcrnrlat=lat_min,urcrnrlat=lat_max,            llcrnrlon=long_min,urcrnrlon=long_max,            rsphere=6371200.,resolution='h',area_thresh=10)
m.drawcoastlines()
m.drawstates()
m.drawcounties()
m.shadedrelief()

## locations
x, y = m(edadata['longitude'], edadata['latitude'])
sp = plt.scatter(x, y, c=edadata['price'], s=20)
plt.rcParams["figure.figsize"] = [5,5]
cb = plt.colorbar(sp)
cb.set_label('Price($)')
plt.show()
plt.clf()


# In[89]:

df3 = edadata.sample(frac=.25)

m2 = Basemap(projection='cyl',lat_0=mid_lat,lon_0=mid_long,            llcrnrlat=lat_min,urcrnrlat=lat_max,            llcrnrlon=long_min,urcrnrlon=long_max,            rsphere=6371200.,resolution='h',area_thresh=10)
m2.drawcoastlines()
m2.drawstates()
m2.drawcounties()
m2.shadedrelief()

x1, y1 = m(df3['longitude'], df3['latitude'])
sp1 = plt.scatter(x1, y1, c=df3['price'], s=20)



plt.rcParams["figure.figsize"] = [15,7]
cb1 = plt.colorbar(sp1)
cb1.set_label('Price($)')
plt.show()


# In[43]:


#sample = edadata.sample()
plt.scatter(edadata['longitude'], edadata['latitude'])


# In[ ]:

#import geopandas as gpd


# In[71]:

print(edadata.describe())


# In[45]:

# fig=edadata.hist()

fig = plt.figure(figsize = (15,20))
ax = fig.gca()
edadata.hist(ax = ax)


# In[6]:

# Total price and adding a new column
edadata['Totalprice'] = edadata['security_deposit'] + edadata['cleaning_fee']+edadata['price']
print(edadata.Totalprice.head())


# In[47]:

edadata.Totalprice.plot.line() # price


# In[ ]:

# price vs venue
edadata.groupby('id').hist()



# In[8]:

# visualize distribution of price (target variable)
plt.hist(edadata['accommodates'], bins=50)
plt.title("Histogram of Accommodations")
plt.xlabel("Number of Accommodations")
plt.ylabel("Frequency")
plt.show()


# In[13]:

print ('Number of Unique Beds: ', np.unique(edadata['beds']))
for i in range(1, 17):
    print( 'Beds {}:'.format(i), len(edadata[edadata['beds'] == i]))


# In[74]:

# visualize distribution of beds
plt.hist(edadata['beds'], bins=50)
plt.title("graph of Beds")
plt.xlabel("Bed Count")
plt.ylabel("Frequency")
sns.plt.show()


# In[78]:

#  review scores ratings
plt.hist(edadata['review_scores_rating'][~edadata['review_scores_rating'].isnull()])
plt.title("Total Review Scores Ratings")
plt.xlabel("Review Score")
plt.ylabel("Count")
plt.show()


# In[94]:

# visualize distribution of price (target variable)
plt.hist(edadata['price'], bins=100 )
plt.title("Graph of Pricing")
plt.xlabel("Pricing $ Per Day")
plt.ylabel("count")
sns.plt.show()


# In[95]:

# log transform the response 'price'
edadata['price_log'] = edadata['price'].apply(lambda x: math.log(x))


# In[98]:

# price distribution (target variable)
plt.hist(edadata['price_log'], bins=30)
plt.title("Graph Pricing ")
plt.xlabel("Price Per Day")
plt.ylabel("count")
sns.plt.show()


# In[30]:

# qq plot for log-transformed pricing
stats.probplot(edadata['price'], dist="norm", plot=pylab)
pylab.show()


# In[31]:

# qq plot for log-transformed pricing
stats.probplot(edadata['price_log'], dist="norm", plot=pylab)
pylab.show()


# 

# In[34]:

edadata['id'].dtype
edadata.dtypes
# number of reviews and price
reviews=edadata[['price','number_of_reviews']]
sns.jointplot('price','number_of_reviews',data=reviews)


# In[99]:

# edadata.id.astype("float")
# convert text-based columns to dummies 
for var_name in edadata:
    dummies = pd.get_dummies(edadata['id'], prefix=var_name)
        
    # Drop the current variable, concat/append the dummy dataframe to the dataframe.
    edadata = pd.concat([edadata.drop(var_name, 1), dummies.iloc[:,1:]], axis = 1)
    
print(edadata)


# In[7]:


hostprice=edadata[['host_id','Totalprice']]
sns.jointplot('host_id','Totalprice',data=hostprice)


#plt.scatter(edadata.host_id, edadata.Totalprice)


# In[9]:

# roomtypeprice=edadata[['Totalprice','room_type']]
# sns.jointplot('Totalprice','room_type',data=roomtypeprice)


# roomTypeDF=edadata.groupby('room_type').id.count()
# roomTypeDF.hist()

plt.hist(edadata.groupby('room_type').id.count(), bins=30)
plt.title("roomtype")
plt.xlabel("id")
plt.ylabel("count")
sns.plt.show()


# In[ ]:




# In[42]:



proprytypeDF = edadata.groupby('property_type').id.count()
proprytypeDF.hist()


# In[47]:

roomPrptyDF = edadata.groupby(['property_type','room_type']).price.mean()
roomPrptyDF.hist()


# In[10]:

from pandas.tools.plotting import scatter_matrix
scatter_matrix(edadata, alpha=0.2, figsize=(10, 10), diagonal='kde')


# In[ ]:

import mplleaflet

sample = edadata.sample(1000)
plt.scatter(sample['longitude'], sample['latitude'])

mplleaflet.display()

