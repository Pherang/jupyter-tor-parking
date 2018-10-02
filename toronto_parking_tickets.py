
# coding: utf-8

# # What Parking Tickets Mean for Toronto
# 
# Parking violations and parking tickets are a contentious topic for Torontonians. Drivers are subjected to misleading signs, police blitzes, and towings.
# 
# Toronto parking regulations have a reputation for being confusing and misleading. In this notebook we study parking tickets and to see what impact they have on the city and its citizens.
# 
# The data was obtained form the city of Toronto's Open Data catalogue and can be downloaded [here](https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#75d14c24-3b7e-f344-4412-d8fd41f89455)

# Align tables in markdown

# In[1]:


get_ipython().run_cell_magic('html', '', '<style>\n    table {\n        margin-left: 0 !important\n    }\n    td, th {\n        text-align: left !important\n    }\n</style>')


# ## Data Dictionary
# 
# | Column | Meaning |
# | :--- | :--- |
# |TAG_NUMBER_MASKED |	First three (3) characters masked with asterisks |
# |DATE_OF_INFRACTION |	Date the infraction occurred in YYYYMMDD format|
# |INFRACTION_CODE	| Applicable Infraction code (numeric)|
# |INFRACTION_DESCRIPTION |	Short description of the infraction|
# |SET_FINE_AMOUNT |	Amount of set fine applicable (in dollars)|
# |TIME_OF_INFRACTION |	Time the infraction occurred  in HHMM format (24-hr clock)|
# |LOCATION1 |	Code to denote proximity (see table below)|
# |LOCATION2 |	Street address|
# |LOCATION3 |	Code to denote proximity (optional)|
# |LOCATION4 |	Street address (optional)|
# |PROVINCE |	Province or state code of vehicle licence plate|
# 

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# The `parking_tags_2016.csv` file was created using csvkit's csvstack to combine four CSV files.

# In[3]:


tickets = pd.read_csv("data/parking_tickets_2016/parking_tags_2016.csv")


# In[4]:


tickets.info(memory_usage='deep')


# In[5]:


tickets.head()


# We can see that some of these columns could be converted to data types that represent them a little better and possibly reduce the memory being used.
# 
# For example we could investigate the `infraction_code` values to see if an int is better suited.

# Around 4pm is when most tickets are given out. Interesting.

# In[6]:


tickets.loc[ tickets['time_of_infraction'].isnull() == True]


# We can convert this column since the values are really four digits representing 24 hour time in the format HHMM. There are some null values so we'll ignore those for now.

# In[7]:


tickets['time_of_infraction'] = tickets['time_of_infraction'].astype('uint16', errors='ignore')


# In[8]:


tickets.loc[ tickets['infraction_code'].isnull() == True]


# We find that there's one ticket with no infraction code. We could replace it with 0 if 0 isn't an infraction code. We can check that below.

# In[9]:


tickets[tickets['infraction_code'] == 0]


# We find there is infraction code numbered 0.

# In[10]:


tickets.loc[1629565, 'infraction_code'] = 0


# In[11]:


tickets[tickets['infraction_code'] == 0]


# In[12]:


tickets['infraction_code'] = tickets['infraction_code'].astype('uint16')


# In[13]:


tickets.info(memory_usage='deep')


# We've managed to reduce memory usage by 13MB. We can convert more of our columns however. The origin column just tracks the spreadsheet number that the row belongs to. It was created when we used CSV kit to combine the files. We know there are only 4 spread sheets numbered 1-4 so we don't need an int64 to store the number. Let's use the int8 datatype instead.

# In[14]:


tickets['origin'] = tickets['origin'].astype('int8')


# In[15]:


tickets.info(memory_usage='deep')


# We've saved another 15MB.

# In[16]:


tickets['set_fine_amount'].value_counts()


# In[17]:


tickets['set_fine_amount'] = tickets['set_fine_amount'].astype('uint16')


# In[18]:


tickets.info(memory_usage='deep')


# ## Exploring Values
# 
# Now that we've loaded the data and tried to reduce it's memory usage we can explore some of the columns to find things of interest.
# 
# A column of interest of course is the fine amounts so let's look at that first.

# In[19]:


tickets['set_fine_amount'].value_counts().sort_index()


# In[20]:


(tickets['set_fine_amount'].describe())


# In[21]:


fines = tickets['set_fine_amount'].value_counts().sort_index()


# In[38]:


plt.style.use('fivethirtyeight')
fines.plot.bar()
plt.xlabel('Fine Amount')
plt.xticks(rotation=45)
plt.ylabel('Ticket Count')
plt.title('Tickets and Fines')


# We can see that almost all of the tickets given out have set fines of $30 dollars.

# In[23]:


tickets['set_fine_amount'].value_counts(normalize=True) * 100


# In[24]:


ticket_total = fines * fines.index


# In[25]:


ticket_total.sum()


# Total ticket fines are worth **$109,675,985** in revenue. Tickets are challenged in court and they can reduced or dismissed entirely. Unfortunately that data wasn't available. However we can look at the potential amount of revenue parking tickets bring in for the city.

# According to the city of Toronto's Revenue Fact [Sheet](https://www.toronto.ca/city-government/budget-finances/city-finance/long-term-financial-plan/city-revenue-fact-sheet/) parking tickets are worth quite a bit of money when compared to additional revenue options that the city can implement. The options highlighted in grey can't be implemented easily.
# 
# 

# ![revenue options](revenue_options_kpmg.png)

# ## Deeper Exploration of Tickets
# 
# Now that we have some general information about parking fines we can explore what people are being fined for.
# We know the most common fine is $30 and that the number of fines is more than 1M.
# 
# We can explore the infractions and break it down to see what parking rules drivers are breaking.

# In[26]:


infraction_info = tickets[['infraction_code','infraction_description','set_fine_amount']].drop_duplicates(subset='infraction_code').sort_values('infraction_code')
infraction_info


# In[27]:


tickets['infraction_code'].value_counts()


# Let's filter for tickets with a fine of $30.

# In[28]:


fine_30 = tickets[tickets['set_fine_amount'] == 30]


# In[29]:


fine_30['infraction_code'].value_counts()


# In[30]:


fine_types = fine_30.drop_duplicates(subset='infraction_code')


# In[31]:


fine_types['infraction_code'].count()


# There are 43 different infractions with a set fine of $30.

# In[32]:


fine_types[['infraction_code', 'infraction_description','set_fine_amount']].sort_values('infraction_code')


# Let's look at the top 10 infractions with a fine of $30.

# In[39]:


top_10 = fine_30['infraction_code'].value_counts()[:10]
top_10 = top_10.sort_values(ascending=False)
#plt.style.use('ggplot')
top_10.plot.bar()
plt.xlabel('Infraction Code')
plt.xticks(rotation=45)
plt.ylabel('Ticket Count')
plt.title('Top 10 Infraction Codes')
plt.show()


# ## Times that Tickets were Given
# 
# We can also look a times that vehicles were ticketed.

# In[34]:


times = tickets['time_of_infraction'].value_counts()
times = times.sort_index()


# In[42]:


fig, ax = plt.subplots()
ax.hist(tickets['time_of_infraction'], range=(0,2400), bins=24, color='orange')

plt.xlabel('Time HH:MM')
plt.ylabel('Ticket Frequency')
plt.axvline(1200, c='blue', label='Noon', linewidth=2)
plt.title('Ticket Times 2016 Total')
plt.show()


# Parking tickets were given out most frequently at 9am, 12pm, and 3-4pm.
