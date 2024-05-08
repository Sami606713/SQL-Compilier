import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os
import pymysql 

# Set the navbar
                        # Layout   
def layout():
    selected = option_menu(
            menu_title=None,
            options=["Connection", 'Execution'], 
            icons=['📥', '🔄','🔄'], 
            menu_icon="Data Cleaning", 
            default_index=0,
            orientation="horizontal"
            )
    return selected

# Set the Database Connecction
def connect_db(port,user_name,password,db):
    try:
        conn = pymysql.connect( 
            host=port, 
            user=user_name,  
            password =password ,
            db=db
            ) 
        st.success("Connection Successful")
        st.session_state['connect']=1
        return conn
    except Exception as e:
        st.write("Not connect")
        st.session_state['connect']=0

# Make database connection form
def show_form():
    _,col2,_=st.columns(3)
    with col2:
        st.title('SQL :red[Conn] :shark:')
        with st.popover("Connect Db"):
            with st.form("DB Info"):
                port=st.text_input("Enter Port")
                user_name=st.text_input("Enter user name")
                password = st.text_input('Enter Password')
                db = st.text_input('Enter database name: ')
                submitted = st.form_submit_button("Connect")
                if submitted:
                    conn=connect_db(port=port,user_name=user_name,password=password,db=db)
                    st.session_state['connection']=conn
                    return conn

# Show the available tables
def display_table(query="SHOW TABLES"):
    conn=st.session_state['connection']
    cursor = conn.cursor()
    cursor.execute(query)
    tables = cursor.fetchall()
    return tables
