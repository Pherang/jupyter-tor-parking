
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


# In[14]:


tickets = pd.read_csv("data/parking_tickets_2016/parking_tags_2016.csv")


# In[17]:


tickets.info(memory_usage='deep')


# In[16]:


tickets.head()

