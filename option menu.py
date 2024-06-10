import streamlit as st

#write a streamlit code for multipage app with the following pages:Home, About, Contact 
# Create a list of pages
pages = ['Home', 'About', 'Contact']

# Create a sidebar selectbox for the pages
page = st.sidebar.selectbox('Page', pages)

if page == 'Home':
    st.title('Home Page')
    st.write('Welcome to the Home Page!')

elif page == 'About':
    st.title('About Page')
    st.write('Welcome to the About Page!')

elif page == 'Contact':
    st.title('Contact Page')
    st.write('Welcome to the Contact Page!')

import streamlit as st
import matplotlib.pyplot as plt


#import data to a dataframe

import pandas as pd

data = pd.read_excel('Data/Data Recieved from NYT/Assemble data edited.xlsx')
st.write(data.head(5))

#display different role in role column using bar chart


# Display the role count as a pie chart
import matplotlib.pyplot as plt

role_counts = data['Role'].value_counts()
role_counts.plot(kind='pie', autopct='%1.1f%%', colormap='Paired')
plt.xlabel('Role')
plt.ylabel('Count')
plt.title('Role Distribution')
plt.show()
st.pyplot(plt)

plt.clf()
#display the role count by location using bar chart

role_counts = data.groupby('Location')['Role'].value_counts().unstack().plot(kind='bar', stacked=True, colormap='Pastel2')
plt.xlabel('Location')
plt.xticks(rotation=45)
plt.ylabel('Count')
plt.title('Role Count by Location')
plt.legend(title='Role', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()
st.pyplot(plt)

#clear the output of the previous code for new plot
plt.clf()
# display information of "Disability (Do you identify as):" column using bar chart, display count on each bar
disability_counts = data['Disability (Do you identify as):'].value_counts()
disability_counts.plot(kind='bar', color='skyblue')
plt.xlabel('Disability')
plt.ylabel('Count')
plt.title('Disability Distribution')
for i, count in enumerate(disability_counts):
    plt.text(i, count, count, ha='center')
plt.show()
st.pyplot(plt)

# display information of "Disability (Do you identify as):" column using table

st.table(disability_counts)



