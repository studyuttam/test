import streamlit as st
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter
import functions as f
import matplotlib.pyplot as plt
import re


nltk.download('all')

#test01
# Set the title of the web app
# Create a list of pages
pages = ['Population Analysis', 'Qualitative Analysis', 'Quantitative Analysis','NYT Staff Information']

# Create a sidebar selectbox for the pages
page = st.sidebar.selectbox('Page', pages)


from textblob import TextBlob

# Create a function to get the sentiment of the feedback and add it to the dataframe
def add_sentiment(data):
    data['Sentiment'] = data['Feedback'].apply(get_sentiment)
    return data

def get_sentiment(feedback):
    analysis = TextBlob(feedback)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'
    
#function for qualitiative analysis feedback data as input and display the feedback data in a table

def qualitative_analysis():
    
    data = pd.read_excel('Data/Data Recieved from NYT/London Met Data.xlsx')
    
    with st.expander("Click here to view Sample Data"):
        st.write('Sample Data:')
        st.table(data.head(2))
    
    number_of_student = data['Student ID'].unique()

    # Add sentiment analysis to the data
    data = add_sentiment(data)

    # Create a container
    container = st.container()

    # Add a header
    container.header("Key Summary Indicators (KPIs)")

    # Add the KPIs
    st.metric(label="Total Number of Students", value=len(number_of_student))
    st.metric(label="Total Feedbacks", value=len(data))
    st.metric(label="Average Number of Feedbacks per Student", value=np.round(len(data)/len(number_of_student), 2))
    #add sample data to the KPIs using expander
    st.metric(label="Number of Positive Feedbacks", value=data['Sentiment'].value_counts()['Positive'])
    with st.expander("Click here to view Sample Positive Feedbacks"):
        positive_feedbacks = data[data['Sentiment'] == 'Positive']['Feedback']
        st.write('Positive Feedbacks:')
        st.table(positive_feedbacks.sample(5))
    st.metric(label="Number of Negative Feedbacks", value=data['Sentiment'].value_counts()['Negative'])
    with st.expander("Click here to view Sample Negative feedbacks"):
        positive_feedbacks = data[data['Sentiment'] == 'Negative']['Feedback']
        st.write('Negative Feedbacks:')
        st.table(positive_feedbacks.sample(5))
    st.metric(label="Number of Neutral Feedbacks", value=data['Sentiment'].value_counts()['Neutral'])
    with st.expander("Click here to view Sample Neutral feedbacks"):
        positive_feedbacks = data[data['Sentiment'] == 'Neutral']['Feedback']
        st.write('Negative Feedbacks:')
        st.table(positive_feedbacks.sample(4))

    # Create a DataFrame for the KPIs
    kpi_data = pd.DataFrame({
    'KPI': ['Total Number of Students', 'Total Feedbacks', 'Number of Positive Feedbacks', 'Number of Negative Feedbacks', 'Number of Neutral Feedbacks', 'Average Number of Feedbacks per Student'],
    'Value': [len(number_of_student), len(data), data['Sentiment'].value_counts()['Positive'], data['Sentiment'].value_counts()['Negative'], data['Sentiment'].value_counts()['Neutral'], np.round(len(data)/len(number_of_student), 2)]
    })

    import plotly.express as px

    # Create a bar chart with plotly
    fig = px.bar(kpi_data, x='KPI', y='Value', text='Value', color='KPI')

    # Make the x-ticks horizontal
    fig.update_layout(xaxis_tickangle=-90)

    # Display the bar chart
    st.plotly_chart(fig)

   

    ####################################################################
    # Display the most common words in the Positive feedbacks

    #most_common_words = f.get_most_common_words(data, num_words=10, sentiment=selected_sentiment)

    # Display the most common words in the Positive feedbacks
    #i = 1
    #st.header(f'Top 10 Words in {selected_sentiment} Feedbacks')
    #st.write('The most common words in the positive feedbacks with word count:')
    #for word, count in most_common_words:
        #st.write(f'{i}. {word}: {count}')
        #i += 1
    ####################################################################
    

    # Display the sentiment count as a pie chart
    
    sentiment_counts = data['Sentiment'].value_counts()

    #add legend to the pie chart

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = [len(data[data['Sentiment'] == 'Positive']), 
             len(data[data['Sentiment'] == 'Negative']),
             len(data[data['Sentiment'] == 'Neutral'])]  # Replace these values with your actual data
    explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Negative')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=330)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.legend(sentiment_counts.index, loc='upper right')
    plt.title('Sentiment Distribution')
    st.pyplot(fig1)
        
    ####################################################################

    #take user input and display the polirity of the input using TextBlob library on streamlit add clear button to clear the input
    st.header('Sentiment Analysis Test')
    user_input = st.text_area("Enter a text to check it's sentiment:")
    
    #make the analyze botton and clear button side by side on strealit
    col1, col2 = st.columns(2)
    if col1.button('Analyze'):
        analysis = TextBlob(user_input)
        if analysis.sentiment.polarity > 0:
            st.write('Sentiment: Positive')
            st.write('Sentiment Score:', analysis.sentiment.polarity)

        elif analysis.sentiment.polarity == 0:
            st.write('Sentiment: Neutral')
            st.write('Sentiment Score:', analysis.sentiment.polarity)
            
        else:
            st.write('Sentiment: Negative')
            st.write('Sentiment Score:', analysis.sentiment.polarity)
            

    if col2.button('Clear'):
        user_input = ''


    ####################################################################
    # Display the data with the sentiment

    #Display 5 random negative feedbacks
    st.title('Sample Feedbacks with different Sentiment')
    negative_feedbacks = data[data['Sentiment'] == 'Negative']['Feedback']
    st.write('Negative Feedbacks:')
    #use expander and scroll bar to display the feedbacks
    with st.expander("Click here to view all Negative Feedbacks"):
        st.table(negative_feedbacks)

    #Display 5 random positive feedbacks

    positive_feedbacks = data[data['Sentiment'] == 'Positive']['Feedback']
    st.write('Positive Feedbacks:')
    with st.expander("Click here to view all Positive Feedbacks"):
        st.table(positive_feedbacks)
    
    #Display 5 random neutral feedbacks

    neutral_feedbacks = data[data['Sentiment'] == 'Neutral']['Feedback']
    st.write('Neutral Feedbacks:')
    with st.expander("Click here to view all Neutral Feedbacks"):
        st.table(neutral_feedbacks)

    #make drop down menu for the showing word cloud of positive , negative and neutral_feedbacks feedbacks
    st.header('Select Sentiment for Wordcloud of Feedbacks')
    selected_sentiment = st.selectbox('Select Sentiment', ['Positive', 'Negative', 'Neutral'])
    f.make_wordcloud(data, sentiment=selected_sentiment)

    ####################################################################

    f.plot_cluster_pie_chart()

    f.display_cluster_feedbacks()
    #f.cluster_students(data, num_clusters=3)
    ####################################################################################
    
# Display the selected page
if page == 'Population Analysis':
    st.title('Welcome to NYT Assemble Project Dashboard!')
    st.text('This dashboard will help you analyze the results of Assemble Project run by Natioal Youth Theater.')

    # Add your population analysis code here


elif page == 'Qualitative Analysis':
    st.title('Welcome to Qualitative Analysis Dashboard!')
    st.write('Our website serves as a comprehensive platform dedicated to exploring the qualitative '
        'analysis of the National Youth Theatre project within the Assemble Project. At the '
        'heart of our endeavor lies a profound commitment to fostering inclusivity, particularly '
        'for individuals with disabilities, within the vibrant landscape of youth theatre', unsafe_allow_html=True, font_size=20, style='color:blue')
    

    # Add your qualitative analysis code here
    qualitative_analysis()

elif page == 'Quantitative Analysis':
    st.write('Quantitative Analysis')
    # Add your quantitative analysis code here

elif page == 'NYT Staff Information':
    st.write('NYT Staff Information')
    # Add your NYT staff information code here