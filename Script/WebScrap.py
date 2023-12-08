#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup

import warnings
warnings.filterwarnings('ignore')


# In[2]:


df=pd.read_csv('movies_with_rotten_tomatoes.csv')


# In[3]:


df['rotten_tomato_genres'].dropna(inplace=True)
# df['rotten_tomato_genres'].replace('nan','No Theme',inplace=True)
df['rotten_tomato_genres']=df['rotten_tomato_genres'].astype(str)
df['rotten_tomato_genres']=df['rotten_tomato_genres'].apply(lambda x: eval(x) if x!='nan' else x)
#### let the dataset become the each row with one rotten_tomato_genres
df_clean=df.explode('rotten_tomato_genres')


# In[4]:


df_clean_T=df_clean[['popularity','production_companies', 'release_date', 'budget', 'revenue', 'runtime','vote_average', 'vote_count', 'credits',
       'tomatometer', 'audience_score', 'weighted_score','rotten_tomato_genres']]


# ### Webscraping

# In[5]:


# Specify the URL of the Wikipedia page
url = 'https://en.wikipedia.org/wiki/Academy_Awards#Awards_of_Merit_categories'  # Replace with the URL of the Wikipedia page you want to scrape

# Send a GET request to the URL
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table you want to extract
table = soup.find('table', {'class': 'wikitable'})  # Replace the class name or other identifiers as needed

# Extract the table data
table_data = []
for row in table.find_all('tr'):
    row_data = []
    for cell in row.find_all(['th', 'td']):
        row_data.append(cell.text.strip())
    if row_data:
        table_data.append(row_data)

# Convert the table data into a pandas DataFrame
df = pd.DataFrame(table_data[1:], columns=table_data[0])


##### Movie Effect Award
def Movie_record(i):
    movie_id=i
    # Specify the URL of the Wikipedia page
    url = Movie_url['Category_url'][movie_id]  # Replace with the URL of the Wikipedia page you want to scrape
    Award_Name=Movie_url['Movie award'][movie_id]

        # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the tables on the page
    tables = soup.find_all('table', {'class': "wikitable"})  # Replace the class name or other identifiers as needed

    df_final_T = pd.DataFrame()

    for i in range(len(tables)):
        table_index = i
        # Extract the table data
        table = tables[table_index]
        table_data = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                row_data.append(cell.text.strip())
            if row_data:
                table_data.append(row_data)


                # Convert the table data into a pandas DataFrame
                df = pd.DataFrame(table_data, columns=table_data[0])
                df_final=df.iloc[1:]
        df_final_T=pd.concat([df_final_T,df_final])




    if movie_id==0:
        Col_name=['Year of Film Release','Film','Film Studio']
        # Convert the table data into a pandas DataFrame
        df_final_Table = df_final_T[Col_name]
        df_final_Table['Year of Film Release'].dropna(inplace=True)
        ######################### Outcome Table
        df_final_Table['Film'].fillna('Time',inplace=True)
        df_final_Table['Film Studio']=np.where(df_final_Table['Film']=='Time',df_final_Table['Year of Film Release'],df_final_Table['Film Studio'])
        df_final_Table['Film Studio'].fillna(method='ffill', inplace=True)

        # #### get the year of the movie
        # df_final_Table['Film Studio']=df_final_Table['Film Studio'].astype(str).str[:7]

        ####Change the name
        df_final_Table.columns=['Film','Film Studio','Year of Film Release']
        df_final_Table.reset_index(inplace=True)

        ##### Only show the movie
        Result_Table=df_final_Table[df_final_Table['Film Studio']!='Time']

        ################ Result Table
        #### Winner
        Result_Table.sort_values('index',ascending=True)
        Award_Winner=Result_Table.groupby('Year of Film Release').head(1)
        Award_Winner['State']='Winner'

        #### Nomination
        Nomination=Result_Table[~Result_Table['Film'].isin(Award_Winner['Film'])]
        Nomination['State']='Nomination'

        Full_list_record=pd.concat([Nomination,Award_Winner])
        Full_list_record['Award']=Award_Name

    else:
        #Col_name=['Year of Film Release','Film','Film Studio']
        # Convert the table data into a pandas DataFrame
        df_final=df_final_T.iloc[:,:3]
        df_final.columns=['Year of Film Release','Film','Film Studio']
        df_final_Table=df_final.copy()
        df_final_Table['Year of Film Release'].dropna(inplace=True)

        ######################### Outcome Table
        df_final_Table['Film'].fillna('Time',inplace=True)
        df_final_Table['Film Studio']=np.where(df_final_Table['Film']=='Time',df_final_Table['Year of Film Release'],df_final_Table['Film Studio'])
        df_final_Table['Film Studio'].fillna(method='ffill', inplace=True)

        # #### get the year of the movie
        # df_final_Table['Film Studio']=df_final_Table['Film Studio'].astype(str).str[:7]

        ####Change the name
        df_final_Table.columns=['Film','Film Studio','Year of Film Release']
        df_final_Table.reset_index(inplace=True)

        ##### Only show the movie
        Result_Table=df_final_Table[df_final_Table['Film Studio']!='Time']

        ################ Result Table
        #### Winner
        Result_Table.sort_values('index',ascending=True)
        Award_Winner=Result_Table.groupby('Year of Film Release').head(1)
        Award_Winner['State']='Winner'

        #### Nomination
        Nomination=Result_Table[~Result_Table['Film'].isin(Award_Winner['Film'])]
        Nomination['State']='Nomination'

        Full_list_record=pd.concat([Nomination,Award_Winner])
        Full_list_record['Award']=Award_Name
    return Full_list_record


# In[6]:


### Get the URL of these award
url='https://en.wikipedia.org/wiki/Academy_Award_for_'

url_list=[]

### get the url name
df['Category_url']=df['Category'].apply(lambda x: x.replace(' ','_'))

for i in df['Category_url']:
    New_url=url+str(i)
    url_list.append(New_url)


# ## Prepare the Dataset that we need

# In[7]:


##### Select some of the Awards
Category_1=['Best Picture','Visual Effects']    
Category_2=['Best Director' , 'Best Actor','Best Actress','Best Supporting Actor', 'Best Supporting Actress']


# In[8]:


##### Select some of the Awards
Category_1=['Best Picture','Visual Effects']    
Category_2=['Best Director' , 'Best Actor','Best Actress','Best Supporting Actor', 'Best Supporting Actress']


### Get the URL of these award
url='https://en.wikipedia.org/wiki/Academy_Award_for_'

url_list=[]

Category_Table_1=pd.DataFrame(Category_1)
Category_Table_1.columns=['Movie award']
### get the url name
Category_Table_1['Category_word']=Category_Table_1['Movie award'].apply(lambda x: x.replace(' ','_'))
Category_Table_1['Category_url']=Category_Table_1['Category_word'].apply(lambda x: url+str(x))
Category_Table_1['Award Type']='Movie Effect'


##### Category_2
Category_Table_2=pd.DataFrame(Category_2)
Category_Table_2.columns=['Movie award']
### get the url name
Category_Table_2['Category_word']=Category_Table_2['Movie award'].apply(lambda x: x.replace(' ','_'))
Category_Table_2['Category_url']=Category_Table_2['Category_word'].apply(lambda x: url+str(x))
Category_Table_2['Award Type']='Role Award'

##### Overall Table
Overall_Table=pd.concat([Category_Table_1,Category_Table_2])

#### Seperate the Dataset of Movie Effect award or Actor Award
Movie_url=Overall_Table[Overall_Table['Award Type']=='Movie Effect']
Role_url=Overall_Table[Overall_Table['Award Type']=='Role Award']


# # Movie Effect Awards

# In[9]:


def Movie_record(i):
    movie_id=i
    # Specify the URL of the Wikipedia page
    url = Movie_url['Category_url'][movie_id]  # Replace with the URL of the Wikipedia page you want to scrape
    Award_Name=Movie_url['Movie award'][movie_id]

        # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the tables on the page
    tables = soup.find_all('table', {'class': "wikitable"})  # Replace the class name or other identifiers as needed

    df_final_T = pd.DataFrame()

    for i in range(len(tables)):
        table_index = i
        # Extract the table data
        table = tables[table_index]
        table_data = []
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all(['th', 'td']):
                row_data.append(cell.text.strip())
            if row_data:
                table_data.append(row_data)


                # Convert the table data into a pandas DataFrame
                df = pd.DataFrame(table_data, columns=table_data[0])
                df_final=df.iloc[1:]
        df_final_T=pd.concat([df_final_T,df_final])




    if movie_id==0:
        Col_name=['Year of Film Release','Film','Film Studio']
        # Convert the table data into a pandas DataFrame
        df_final_Table = df_final_T[Col_name]
        df_final_Table['Year of Film Release'].dropna(inplace=True)
        ######################### Outcome Table
        df_final_Table['Film'].fillna('Time',inplace=True)
        df_final_Table['Film Studio']=np.where(df_final_Table['Film']=='Time',df_final_Table['Year of Film Release'],df_final_Table['Film Studio'])
        df_final_Table['Film Studio'].fillna(method='ffill', inplace=True)

        # #### get the year of the movie
        # df_final_Table['Film Studio']=df_final_Table['Film Studio'].astype(str).str[:7]

        ####Change the name
        df_final_Table.columns=['Film','Film Studio','Year of Film Release']
        df_final_Table.reset_index(inplace=True)

        ##### Only show the movie
        Result_Table=df_final_Table[df_final_Table['Film Studio']!='Time']

        ################ Result Table
        #### Winner
        Result_Table.sort_values('index',ascending=True)
        Award_Winner=Result_Table.groupby('Year of Film Release').head(1)
        Award_Winner['State']='Winner'

        #### Nomination
        Nomination=Result_Table[~Result_Table['Film'].isin(Award_Winner['Film'])]
        Nomination['State']='Nomination'

        Full_list_record=pd.concat([Nomination,Award_Winner])
        Full_list_record['Award']=Award_Name

    else:
        #Col_name=['Year of Film Release','Film','Film Studio']
        # Convert the table data into a pandas DataFrame
        df_final=df_final_T.iloc[:,:3]
        df_final.columns=['Year of Film Release','Film','Film Studio']
        df_final_Table=df_final.copy()
        df_final_Table['Year of Film Release'].dropna(inplace=True)

        ######################### Outcome Table
        df_final_Table['Film'].fillna('Time',inplace=True)
        df_final_Table['Film Studio']=np.where(df_final_Table['Film']=='Time',df_final_Table['Year of Film Release'],df_final_Table['Film Studio'])
        df_final_Table['Film Studio'].fillna(method='ffill', inplace=True)

        # #### get the year of the movie
        # df_final_Table['Film Studio']=df_final_Table['Film Studio'].astype(str).str[:7]

        ####Change the name
        df_final_Table.columns=['Film','Film Studio','Year of Film Release']
        df_final_Table.reset_index(inplace=True)

        ##### Only show the movie
        Result_Table=df_final_Table[df_final_Table['Film Studio']!='Time']

        ################ Result Table
        #### Winner
        Result_Table.sort_values('index',ascending=True)
        Award_Winner=Result_Table.groupby('Year of Film Release').head(1)
        Award_Winner['State']='Winner'

        #### Nomination
        Nomination=Result_Table[~Result_Table['Film'].isin(Award_Winner['Film'])]
        Nomination['State']='Nomination'

        Full_list_record=pd.concat([Nomination,Award_Winner])
        Full_list_record['Award']=Award_Name
    return Full_list_record


# In[10]:


per_movie=[Movie_record(i) for i in range(len(Movie_url))]
Movie_award=pd.concat(per_movie)


# In[11]:


Movie_award


# In[12]:


#Movie_award.to_csv('Movie_effect_award.csv')


# ## Role Award

# In[13]:


def movie_role_award(i):
    movie_id=i
    # Specify the URL of the Wikipedia page
    url = Role_url['Category_url'][movie_id]  # Replace with the URL of the Wikipedia page you want to scrape
    Award_Name=Role_url['Movie award'][movie_id]

        # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the tables on the page
    tables = soup.find_all('table', {'class': "wikitable sortable"})  # Replace the class name or other identifiers as needed

    df_final_T = pd.DataFrame()

    for i in range(len(tables)):
        table_index = i
        # Extract the table data
        table = tables[table_index]
        table_data = []
        if len(table.find_all('tr'))>=3:

            for row in table.find_all('tr'):
                row_data = []
                #if len(row.find_all(['th', 'td']))>=2:
                for cell in row.find_all(['th', 'td']):
                    row_data.append(cell.text.strip())
                if row_data:
                    table_data.append(row_data)

                    # Convert the table data into a pandas DataFrame
                    df = pd.DataFrame(table_data, columns=table_data[0])
                    df_final=df.iloc[1:]
        df_final_T=pd.concat([df_final_T,df_final])

    if movie_id==0:
        df_final_T['Ref.'].fillna('Nominees',inplace=True)
        df_final_T.reset_index(inplace=True,drop=True)
        #### set up the index no of the dataframe
        df_final_T.reset_index(inplace=True)
        Adjust_T=df_final_T[df_final_T['Ref.']=='Nominees'][['index','Year','Director(s)','Ref.']]
        Adjust_T.columns=['index','Director(s)','Film','Award_Type']
        Adjust_T['Year']=np.nan

        winner_T=df_final_T[df_final_T['Ref.']!='Nominees']
        winner_T['Ref.']='Winner'
        winner_T.rename(columns={'Ref.':'Award_Type'},inplace=True)
        
        df_final_Table=pd.concat([Adjust_T,winner_T])

        df_final_Table.sort_values('index',ascending=True,inplace=True)
        df_final_Table['Year'].fillna(method='ffill',inplace=True)
        df_final_Table['Award']=Award_Name

    else:
        df_final_T['Ref.'].fillna('Nominees',inplace=True)
        df_final_T.reset_index(inplace=True,drop=True)
        #### set up the index no of the dataframe
        df_final_T.reset_index(inplace=True)
        df_final_T.columns=['index','Year','Actor/Actress','Role(s)','Film','Ref.']
        Adjust_T=df_final_T[df_final_T['Ref.']=='Nominees'][['index','Year','Actor/Actress','Role(s)','Ref.']]
        Adjust_T.columns=['index','Actor/Actress','Role(s)','Film','Award_Type']
        Adjust_T['Year']=np.nan

        winner_T=df_final_T[df_final_T['Ref.']!='Nominees']
        winner_T['Ref.']='Winner'
        winner_T.rename(columns={'Ref.':'Award_Type'},inplace=True)

        df_final_Table=pd.concat([Adjust_T,winner_T])

        df_final_Table.sort_values('index',ascending=True,inplace=True)
        df_final_Table['Year'].fillna(method='ffill',inplace=True)
        df_final_Table['Award']=Award_Name
    return df_final_Table


# In[14]:


per_movie_role=[movie_role_award(i) for i in range(len(Role_url))]
Award_movie_role=pd.concat(per_movie_role)


# In[15]:


Award_movie_role


# In[16]:


#Award_movie_role.to_csv('Actor_Actress_Director_award.csv')

