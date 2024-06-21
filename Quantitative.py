import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


#import excel file name disabilitycensus2021.xlsx sheet name Table 6

df = pd.read_excel('Data/disabilitycensus2021.xlsx', sheet_name='Table 6')

st.write(df.head())

#make multi select filters for local authority and age group on the side bar
local_authority = st.sidebar.multiselect('Local Authority', df['Local Authority'].unique())
age_group = st.sidebar.multiselect('Age Group', df['Age'].unique())

#write code if nothing is selected for local_authority and age_group then display a message to select local_authority and age_group for the data to be displayed
if len(local_authority) == 0 or len(age_group) == 0:
    st.write('Please select Local Authority and Age Group')

#display the selected local authority and age group
st.write('Local Authority:', local_authority)
st.write('Age Group:', age_group)


#st_card('Completed Orders', value=76.4, show_progress=True)

#display df['Count'] for selected local authority and age group in card

#filter the data based on the selected local authority and age group
disabled_population = df[(df['Local Authority'].isin(local_authority))
                    & (df['Age'].isin(age_group))
                    & (df['Category'] == 'Four category')
                    & (df['Sex'].isin(['Male','Female']))
                    & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]

st.write('Disabled Population:', disabled_population['Count'].sum())

# Total population

total_population = df[(df['Local Authority'].isin(local_authority))
                    & (df['Age'].isin(age_group))
                    & (df['Category'] == 'Four category')
                    & (df['Sex'].isin(['Male','Female']))
                    & (df['Disability Status'].isin(['Disabled; limited a lot']))]

st.write('Total Population:', total_population['Population'].sum())


#display total population and disabled population in bar chart
plt.figure(figsize=(10, 5))
sns.barplot(x=['Total Population', 'Disabled Population'], y=[total_population['Population'].sum(), disabled_population['Count'].sum()])
plt.title('Total Population vs Disabled Population')
st.pyplot(plt)


#display a pie chart for different sex in the disabled
plt.figure(figsize=(10, 5))
disabled_population.groupby('Sex')['Count'].sum().plot.pie(autopct='%1.1f%%')
plt.title('Disabled Population by Sex')
st.pyplot(plt)

st.write('Disabled Population:', disabled_population.groupby('Sex')['Count'].sum())


poulation_grpby_category = df[(df['Local Authority'].isin(local_authority))
                    & (df['Age'].isin(age_group))
                    & (df['Category'] == 'Four category')
                    & (df['Sex'].isin(['Male','Female']))
                    ]

import seaborn as sns

# Prepare data for seaborn
data = poulation_grpby_category.groupby('Disability Status')['Count'].sum().reset_index()

# Create a bar plot
plt.figure(figsize=(10, 5))
barplot = sns.barplot(x='Disability Status', y='Count', data=data, palette='viridis')

# Add data labels
for bar in barplot.patches:
    barplot.text(x = bar.get_x() + bar.get_width() / 2, 
                 y = bar.get_height(), 
                 s = f'{int(bar.get_height())}', 
                 ha = 'center', 
                 va = 'bottom')

# Set y-axis limit
plt.ylim(0, data['Count'].max() * 1.1)

plt.xticks(rotation=45)
plt.title('Population Group by Disability Status', fontsize=16, fontweight='bold', y=1.05)
plt.tight_layout(pad=1.0)
st.pyplot(plt)

#display disabled population of Top 10 local authorities in a bar chart

# Convert 'Count' column to numeric
df['Count'] = pd.to_numeric(df['Count'], errors='coerce')
uk_disabled_population = df[(df['Age'].isin(age_group))
                    & (df['Category'] == 'Four category')
                    & (df['Sex'].isin(['Male','Female']))
                    & (df['Disability Status'].isin(['Disabled; limited a lot','Disabled; limited a little']))]

# Get the top 10 local authorities by disabled population
disabled_population_top10 = uk_disabled_population.groupby('Local Authority')['Count'].sum().nlargest(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=disabled_population_top10.index, y=disabled_population_top10.values)
plt.xticks(rotation=45)
plt.title('Disabled Population For Top 10 Local Authority')
st.pyplot(plt)

from streamlit_card import card

hasClicked = card(
  title="Hello World!",
  text="Some description",
  image="http://placekitten.com/200/300",
  url="https://github.com/gamcoh/st-card"
)