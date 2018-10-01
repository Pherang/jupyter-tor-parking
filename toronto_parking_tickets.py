
# coding: utf-8

# # What Parking Tickets Mean for Toronto
# 
# Parking violations and parking tickets are a contentious topic for Torontonians.
# 
# Toronto parking regulations have a reputation for being confusing and misleading. In this notebook we study parking tickets and to see what impact they have on the city and its citizens.
# 
# The data was obtained form the city of Toronto's Open Data catalogue and can be downloaded [here](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#75d14c24-3b7e-f344-4412-d8fd41f89455)

# ## Data Dictionary
# 
# | Column | Meaning |
# | :--- | :--- |
# |TAG_NUMBER_MASKED |	First three (3) characters masked with asterisks |
# DATE_OF_INFRACTION |	Date the infraction occurred in YYYYMMDD format
# INFRACTION_CODE	| Applicable Infraction code (numeric)
# INFRACTION_DESCRIPTION |	Short description of the infraction
# SET_FINE_AMOUNT |	Amount of set fine applicable (in dollars)
# TIME_OF_INFRACTION |	Time the infraction occurred  in HHMM format (24-hr clock)
# LOCATION1 |	Code to denote proximity (see table below)
# LOCATION2 |	Street address
# LOCATION3 |	Code to denote proximity (optional)
# LOCATION4 |	Street address (optional)
# PROVINCE |	Province or state code of vehicle licence plate
# 

# In[9]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Align tables in markdown

# In[12]:


get_ipython().run_cell_magic('html', '', '<style>\n    table {\n        margin-left: 0 !important\n    }\n    td, th {\n        text-align: left !important\n    }\n</style>')


# The `parking_tags_2016.csv` file was created using csvkit's csvstack to combine four CSV files.

# In[14]:


tickets = pd.read_csv("data/parking_tickets_2016/parking_tags_2016.csv")


# In[31]:


tickets.info(memory_usage='deep')


# In[16]:


tickets.head()


# We can see that some of these columns could be converted to data types that represent them a little better and possibly reduce the memory being used.
# 
# For example we could investigate the `infraction_code` values to see if an int is better suited.

# In[19]:


tickets['time_of_infraction'].value_counts()


# In[26]:


tickets.loc[ tickets['time_of_infraction'].isnull() == True]['']


# We can convert this column since the values are really four digits representing 24 hour time in the format HHMM. There are some null values so we'll ignore those for now.

# In[29]:


tickets['time_of_infraction'] = tickets['time_of_infraction'].astype('uint16', errors='ignore')


# In[34]:


tickets.loc[ tickets['infraction_code'].isnull() == True]


# We find that there's one ticket with no infraction code. We could replace it with 0 if 0 isn't an infraction code. We can check that below.

# In[36]:


tickets[tickets['infraction_code'] == 0]


# We find there is infraction code numbered 0.

# In[42]:


tickets.loc[1629565, 'infraction_code'] = 0


# In[43]:


tickets[tickets['infraction_code'] == 0]


# In[46]:


tickets['infraction_code'] = tickets['infraction_code'].astype('uint16')


# In[47]:


tickets.info(memory_usage='deep')


# We've managed to reduce memory usage by 13MB. We can convert more of our columns however. The origin column just tracks the spreadsheet number that the row belongs to. It was created when we used CSV kit to combine the files. We know there are only 4 spread sheets numbered 1-4 so we don't need an int64 to store the number. Let's use the int8 datatype instead.

# In[48]:


tickets['origin'] = tickets['origin'].astype('int8')


# In[49]:


tickets.info(memory_usage='deep')


# We've saved another 15MB.

# In[50]:


tickets['set_fine_amount'].value_counts()


# In[51]:


tickets['set_fine_amount'] = tickets['set_fine_amount'].astype('uint16')


# In[52]:


tickets.info(memory_usage='deep')


# ## Exploring Values
# 
# Now that we've loaded the data and tried to reduce it's memory usage we can explore some of the columns to find things of interest.
# 
# A column of interest of course is the fine amounts so let's look at that first.
