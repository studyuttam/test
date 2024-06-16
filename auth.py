#write code for creating users and passwords for a streamlit app

import streamlit as st
import pandas as pd
import numpy as np
import os
import hashlib

def create_user_hash_pwd():
    st.title('Create User')
    user = st.text_input('Username')
    password = st.text_input('Password', type='password')
    if st.button('Create User'):
        if os.path.exists('users.csv'):
            df = pd.read_csv('users.csv')
            if user in df['user'].values:
                st.error('User already exists')
            else:
                # hash password here before saving
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                
                df = pd.concat([df, pd.DataFrame({'user': [user], 'password': [hashed_password]})], ignore_index=True)
                df.to_csv('users.csv', index=False)
                st.success('User created successfully')
        else:
            # hash password here before saving
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            df = pd.DataFrame({'user': [user], 'password': [hashed_password]})
            df.to_csv('users.csv', index=False)
            st.success('User created successfully')


def login():
    st.title('Login')
    user = st.text_input('Username', key='create_user')
    password = st.text_input('Password', type='password', key='create_user_pwd')
    if st.button('Login'):
        if os.path.exists('users.csv'):
            df = pd.read_csv('users.csv')
            if user in df['user'].values:
                # hash the input password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                # compare the hashed input password with the stored hashed password
                if hashed_password == df[df['user'] == user]['password'].values[0]:
                    st.success('Login successful')
                    return True
                else:
                    st.error('Invalid password')
            else:
                st.error('User does not exist')
        else:
            st.error('No users found')

#add code for admin login who can only create users

def admin_login():
    st.title('Admin Login')
    user = st.text_input('Username', key='admin')
    password = st.text_input('Password', type='password', key='admin_pwd')
    if st.button('Login'):
        if os.path.exists('users.csv'):
            df = pd.read_csv('users.csv')
            if user in df['user'].values:
                # hash the input password
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                # compare the hashed input password with the stored hashed password
                if hashed_password == df[df['user'] == user]['password'].values[0]:
                    if user == 'Admin':
                        st.success('Admin login successful')
                        st.write('Create new users')
                        create_user_hash_pwd()
                    else:
                        st.error('Invalid user')
                else:
                    st.error('Invalid password')
            else:
                st.error('User does not exist')
        else:
            st.error('No users found')


if __name__ == '__main__':
    st.sidebar.title('Authentication')
    choice = st.sidebar.radio('Select', ['Create User', 'Login'])
    if choice == 'Create User':
        create_user_hash_pwd()
    else:
        login()
        

