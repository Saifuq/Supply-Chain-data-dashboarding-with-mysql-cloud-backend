import mysql.connector
import pandas as pd
import streamlit as st

def get_db_connection():
    """Establishes a connection to the MySQL database using Streamlit secrets."""
    try:
        # Check if secrets are available (works for both local .streamlit/secrets.toml and Streamlit Cloud)
        if "mysql" in st.secrets:
            conn = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"],
                port=st.secrets["mysql"]["port"],
                database=st.secrets["mysql"]["database"]
            )
            return conn
        else:
            st.error("Database secrets not found. Please configure .streamlit/secrets.toml")
            return None
    except mysql.connector.Error as err:
        st.error(f"Error connecting to database: {err}")
        return None

def fetch_data(query):
    """Fetches data from the database using a SQL query."""
    conn = get_db_connection()
    if conn:
        try:
            df = pd.read_sql(query, conn)
            conn.close()
            return df
        except Exception as e:
            st.error(f"Error executing query: {e}")
            conn.close()
            return pd.DataFrame()
    return pd.DataFrame()

def get_all_data():
    """Fetches all data from the supply_chain table."""
    query = "SELECT * FROM supply_chain"
    return fetch_data(query)
