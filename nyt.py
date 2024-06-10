import streamlit as st
import pandas as pd
import numpy as np


st.title('Welcome to NYT Assemble Project Dashboard!')
st.text('This dashboard will help you analyze the results of Assemble Project run by Natioal Youth Theater.')

#make a sidebar

st.sidebar.title('User Input Features')
st.sidebar.text('Please select the options below:')

# make different containers for different options

#Container 1
st.sidebar.header('Select the Year')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(2010,2021))))  

#Container 2
st.sidebar.header('Select the Month')
selected_month = st.sidebar.selectbox('Month', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])  

#Container 3
st.sidebar.header('Select the Day')
selected_day = st.sidebar.selectbox('Day', list(range(1,32)))

#Container 4
st.sidebar.header('Select the Time')
selected_time = st.sidebar.slider('Time', 0, 23, 12)

 #Different charts

# create a data frame
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50]
})

# create a bar chart
st.bar_chart(data)

# create a line chart
st.line_chart(data)

# create a area chart
st.area_chart(data)

# create a scatter chart
st.write('Scatter Chart')

chart_data = pd.DataFrame(
    np.random.randn(100, 2),
    columns=['a', 'b'])

st.line_chart(chart_data)


#create a woord cloud

st.write('Word Cloud')

text = ('Streamlit is a great tool for data science and machine learning. '
        'It is easy to use and very intuitive. '
        'You can create beautiful web apps with it. '
        'I love using Streamlit.')

#Display word cloud using the wordcloud library remove stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# Streamlit's method to display the plot
st.pyplot(plt)



# create a table
st.write('Data Frame')
st.write(data)

#get the map of united kingdom and display it
st.write('Map of London')
# Create a DataFrame with the latitude and longitude of London
map_data = pd.DataFrame({
    'lat': [51.5074],
    'lon': [-0.1278]
})

# Plot the map
st.map(map_data)


# create a button
if st.button('Say Hello'):
    st.write('Why hello there')
else:    
    st.write('Goodbye')


uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data)

#import xlxs data from /Users/uttam/Desktop/Streamlit/Data with file name disabilitycensus2021.xlsx and sheet name as Table 6 make top row as header while Importing the data

data = pd.read_excel('/Users/uttam/Desktop/Streamlit/Data/disabilitycensus2021.xlsx', sheet_name='Table 6', header=0)

#display the data using pandas dataframe

st.write(data)


#make year and local authority as as filter and display the data for the selected year and local authority

# make a sidebar

st.sidebar.title('User Input Features')
st.sidebar.text('Please select the options below:')

selected_local_authority = st.sidebar.selectbox('Local Authority', data['Local Authority'].unique(), key='local_authority_selectbox')

#add new filter for Disability status select unique values from the Disability Status column
selected_disability_status = st.sidebar.selectbox('Disability Status', data['Disability Status'].unique(), key='disability_status_selectbox')

#add multiple choise checkbox for Sex column select unique values from Sex column
selected_sex = st.sidebar.multiselect('Sex', data['Sex'].unique(),key='sex_selectbox')

#add multiple choise checkbox for Age column select unique values from Age column
selected_age = st.sidebar.multiselect('Age', data['Age'].unique(), key='age_multiselect')


#filter data based on selected_disability_status and selected_local_authority
data_filtered = data[(data['Local Authority'] == selected_local_authority) & 
                     (data['Disability Status'] == selected_disability_status) & 
                     (data['Age'].isin(selected_age)) &
                     (data['Sex'].isin(selected_sex))]

#display the filtered data
st.write(data_filtered)

# display the population column by sex as a pie chart

import matplotlib.pyplot as plt

# Group the data by 'Sex' and sum the 'Population'
population_by_sex = data_filtered.groupby('Sex')['Population'].sum()

# Create a pie chart
plt.figure(figsize=(6,6))
patches, texts, autotexts = plt.pie(population_by_sex, labels = population_by_sex.index, autopct='%1.1f%%')
plt.title('Population by Sex')
# Add a legend
plt.legend(patches, population_by_sex.index, loc="best")
plt.show()

# Display the pie chart in Streamlit
st.pyplot(plt)

# display the population column as a line chart

st.line_chart(data_filtered['Population'])

#display the population column as a area chart

st.area_chart(data_filtered['Population'])

#display the population column as a scatter chart

st.write('Scatter Chart')

// add new page with name Qualitative Analysis

st.write('Qualitative Analysis')


// add new page with name Quantitative Analysis



st.write('Quantitative Analysis')

