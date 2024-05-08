import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import os
import pymysql 
from utils import layout,connect_db,show_form,display_table

# Set page Config
st.set_page_config(
    page_title="SQL Compilier",
    page_icon='Data',
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize session state
if 'connect' not in st.session_state:
    st.session_state['connect'] = 0
if 'execute' not in st.session_state:
    st.session_state['execute'] = 0
if 'connection' not in st.session_state:
    st.session_state['connection'] = None
if 'sel_table' not in st.session_state:
    st.session_state['sel_table'] = None


if __name__=="__main__":
    option=layout()
    if(option=='Connection'):
        # Show the form for connection
        conn=show_form()
  
        if st.session_state['connect'] == 1:
            # Display table
            st.markdown("<h3 style='margin: 20px 0; text-align: center;'>Availabe Tables</h3>", unsafe_allow_html=True)
            table = display_table()
            with st.container(border=True):
                col1,col2=st.columns(2)
                with col1:
                    st.dataframe(table,use_container_width=True)
                with col2:
                    # st.data_editor(table,use_container_width=True)
                    op=st.selectbox('select table',table)
                    st.session_state['sel_table']=op
        
        else:
            st.info("No Tables Found")
        
    elif(option=='Execution'):
        query=None
        _,col2,_=st.columns(3)
        with col2:
            st.title('Run :red[Query] :shark:')
            if(st.button("Run")):
                st.session_state['execute']=1
                
        
        with st.container(border=True):
                with st.container(border=True):
                    user_query=st.text_area("Enter query here: ")
                    query=user_query
      
                with st.container(border=True):
                    if(st.session_state['execute']==1):
                        conn=st.session_state['connection']
                        # st.write(conn)
                        if(conn is None):
                            st.error("Database Connection is not establish")
                        else:
                            try:
                                cursor=conn.cursor()
                                table=st.session_state['sel_table']
                                # cursor.execute(f"select * from {table}")    
                                cursor.execute(query)    
                                
                                # fetch the columns
                                columns = [desc[0] for desc in cursor.description]
                                data=cursor.fetchall()

                                df = pd.DataFrame(data, columns=columns)
                                st.dataframe(data=df,use_container_width=True)
                            except Exception as e:
                                st.error(e)
        