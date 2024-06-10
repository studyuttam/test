import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import pandas as pd
from textblob import TextBlob
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

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

# Function to get the most common words for positive feedbacks
def get_most_common_words(data,num_words=10, sentiment='Positive'):
    positive_feedbacks = data[data['Sentiment'] == sentiment]['Feedback']
    text = ' '.join(positive_feedbacks)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word, pos='v') for word in words]
    stop_words = set(stopwords.words('english'))
    additional_stopwords = ['.', ',', 'student','I','session','group','He','-','She','!','today',"'", "also","'",
                            "would", "see", "’", "seem","'s", ")","get","could", "take", "go"]  # replace with your words
    stop_words.update(additional_stopwords)
    words = [word for word in words if word not in stop_words]
    word_counts = Counter(words)
    most_common_words = word_counts.most_common(num_words)
    return most_common_words


#function to make wordcloud of most common words in positive feedbacks

def make_wordcloud(data, sentiment):
    positive_feedbacks = data[data['Sentiment'] == sentiment]['Feedback']
    text = ' '.join(positive_feedbacks)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    lemmatizer = WordNetLemmatizer()
    words = word_tokenize(text)
    words = [lemmatizer.lemmatize(word, pos='v') for word in words]
    stop_words = set(stopwords.words('english'))
    additional_stopwords = ['.', ',', 'Student','I','session','group','He','-','She','!','today',"'", "also","'",
                            "would", "see", "’", "seemed","'s", ")","get","could", "take", "go"]  # replace with your words
    stop_words.update(additional_stopwords)
    words = [word for word in words if word not in stop_words]
    wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stop_words,
                min_font_size = 10).generate(text)
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()
    
    st.pyplot(plt)
    

def cluster_students_with_PCA(data, num_clusters=3):
    data = add_sentiment(data)
    positive_feedbacks = data[data['Sentiment'] == 'Positive']['Feedback']
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(data['Feedback'])
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(X)
    centers = kmeans.cluster_centers_
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X.toarray())
    plt.scatter(X_pca[:, 0], X_pca[:, 1], c=kmeans.labels_, cmap='viridis')
    plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.5)
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')
    plt.title('KMeans Clustering of Feedbacks')
    plt.show()
    st.pyplot(plt)

def cluster_students(data, num_clusters=3):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(data['Feedback'])
    cosine_sim = cosine_similarity(X)
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(cosine_sim)
    data['Cluster'] = clusters
    grouped_data = data.groupby('Cluster')
    for name, group in grouped_data:
        st.text('Cluster:', name)
        st.text(group[['Student ID', 'Feedback']])
        st.text('\n')
    return grouped_data
    
#import excel file with cluster data and plot pie chart using plotly of students in each cluster

def plot_cluster_pie_chart():
    data = pd.read_excel('Data/Data Recieved from NYT/London Met Data with Cluster.xlsx')
    #give meaning to the cluster cluster 0 - Quite and shy, cluster 1 - Active and outspoken, cluster 2 - Average
    data['Cluster'] = data['Cluster'].map({0: 'Quite and shy', 1: 'Active and outspoken', 2: 'Developing and Learning'})
    fig = px.pie(data, names='Cluster', title='Students in Each Cluster')
    #st.title('Pie Chart of Students in Each Cluster (based on Similarity of Feedbacks)')
    st.markdown("# <span style='font-size:30px;'>Student's Cluster \
                (based on Similarity of Feedbacks)</span>", unsafe_allow_html=True)
    st.plotly_chart(fig)


#print students in each cluster and their feedbacks usinf extander

def display_cluster_feedbacks():
    data = pd.read_excel('Data/Data Recieved from NYT/London Met Data with Cluster.xlsx')
    
    #give meaning to the cluster cluster 0 - Quite and shy, cluster 1 - Active and outspoken, cluster 2 - Average
    data['Cluster'] = data['Cluster'].map({0: 'Quite and shy', 1: 'Active and outspoken', 2: 'Developing and Learning'})

    for name, group in data.groupby('Cluster'):
        with st.expander(f'Cluster: {name}'):
            for student_id, feedback in zip(group['Student ID'], group['Feedback']):
                st.write('Student ID:', student_id)
                st.write('Feedback:', feedback)
                st.write('\n')