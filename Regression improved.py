
# coding: utf-8

# In[63]:

get_ipython().magic(u'matplotlib inline')
import pandas as pd
import numpy as np
from sklearn import ensemble
from sklearn import linear_model
from sklearn.grid_search import GridSearchCV
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
import sklearn.metrics as metrics
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.linear_model import LinearRegression


# In[21]:

regressiondf = pd.read_csv('cleanlisting.csv')
regressiondf.head()


# In[ ]:




# In[65]:

# clf = LinearRegression()
# y = regressiondf['price']
# clf.fit(regressiondf.drop('price', axis='columns'), y)


# In[66]:

regressiondf = regressiondf[[
    "accommodates", "price", "accommodates" , "beds" ,"neighbourhood_cleansed",   "room_type", 
    "cancellation_policy", "instant_bookable", "reviews_per_month", "number_of_reviews","zipcode",
            "review_scores_rating",  "ScoredRating", "property_type",  "bathrooms" ,"beds" ,"host_is_superhost", "TV" ,
            "Internet", "Kitchen"]]

regressiondf.head()


# In[67]:

for categorical_feature in ['neighbourhood_cleansed', 'property_type','cancellation_policy',
                            'room_type','instant_bookable','host_is_superhost']:
    features = pd.concat([features, pd.get_dummies(regressiondf[categorical_feature])], axis=1)
    
features.head()


# In[29]:

for col in features.columns[features.isnul
                            l().any()]:
    print(col)


# In[ ]:




# In[68]:

for col in features.columns[features.isnull().any()]:
    features[col] = features[col].fillna(features[col].median())


# In[69]:

features['price'].sort_values().reset_index(drop=True).plot()


# In[70]:

fitters = features.query('price <= 600')


# In[71]:

#regression
clf = LinearRegression()
y = fitters['price']
clf.fit(fitters.drop('price', axis='columns'), y)


# In[72]:

y_pred = clf.predict(fitters.drop('price', axis='columns'))
import sklearn.metrics


# # MSE is the square of the average error in each term, while root MSE is its absolute value.

# In[73]:

mse = sklearn.metrics.mean_squared_error(y, y_pred)
mse


# In[74]:

root_mse = mse**(1/2)
root_mse



# # Our RMSE is 1.0 dollars, : meaning that our classifier is wrong by that much on average. So its less HEnce out model is fine

# How significant is this with respect to the range of prices we are seeing? To see that let's plot RMSE as a boundary around the median price.

# In[ ]:




# In[77]:

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sns.kdeplot(y)
ax = plt.gca()
ax.set_xlim([0, 600])
plt.axvline(y.median(), c='
            black')
ax.add_patch(
    patches.Rectangle((y.median() - root_mse, 0), 2*root_mse, 0.006,
                      color='red', alpha=0.2)
)


# In[78]:

r_squared = sklearn.metrics.r2_score(y, y_pred)
r_squared


# In[79]:

#effect of neighbourhood

coefs = list(zip(clf.coef_, fitters.drop('price', axis='columns')))
coefs


neighborhoods = np.unique(regressiondf['neighbourhood_cleansed'])
neighborhood_effects = [v for v in coefs if v[1] in neighborhoods]


# In[80]:


plt.figure(figsize=(20,10))

pd.Series(data=[n[0] for n in neighborhood_effects],
          index=[n[1] for n in neighborhood_effects])\
    .sort_values()\
    .plot(kind='bar')



# nb_counts = Counter(neighborhoods.neighbourhood_cleansed)
# tdf = pd.DataFrame.from_dict(nb_counts, orient='index').sort_values(by=0)
# tdf.plot(kind='bar')


# In[ ]:



