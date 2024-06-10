import streamlit as st
import pandas as pd
 
st.title('Hello World')
st.write('This is a simple example of Streamlit application')

#creat a upload folder button and import all the files in the folder into a dataframe

uploaded_file = st.file_uploader("Choose a folder", type="folder")
if uploaded_file is not None:
    for file in uploaded_file:
        file.seek(0)
        st.write(file)
        data = pd.read_csv(file)
        st.write(data)




        