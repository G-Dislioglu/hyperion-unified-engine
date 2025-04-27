"""
Streamlit dashboard for Hyperion Unified Engine
Features:
- Sidebar login with API key validation
- Display of all tasks
- Bar chart of tasks per module
- Form to create new tasks
"""

import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from datetime import datetime

from storage.db import valid_api_key, conn, init_db
from hue.core import Optimizer

# Initialize the database
init_db()

# Page configuration
st.set_page_config(
    page_title="Hyperion Unified Engine",
    page_icon="🚀",
    layout="wide"
)

# Session state initialization
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "optimizer" not in st.session_state:
    st.session_state.optimizer = Optimizer()

# Sidebar with API key login
with st.sidebar:
    st.title("Hyperion Dashboard")
    st.subheader("Login")
    
    api_key = st.text_input("API Key", type="password")
    login_button = st.button("Login")
    
    if login_button:
        if valid_api_key(api_key):
            st.session_state.authenticated = True
            st.success("Login successful!")
        else:
            st.error("Invalid API key")
    
    if st.session_state.authenticated:
        st.success("Authenticated ✅")
    
    st.divider()
    st.info("Hyperion Unified Engine v0.1.0")

# Main content
if not st.session_state.authenticated:
    st.warning("Please login with a valid API key to access the dashboard")
else:
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Tasks Overview", "Task Analytics", "Create Task"])
    
    # Tab 1: Tasks Overview
    with tab1:
        st.header("Tasks Overview")
        
        # Fetch all tasks from the database
        query = "SELECT id, module, payload, result, created_at FROM tasks ORDER BY created_at DESC"
        df = pd.read_sql_query(query, conn())
        
        if df.empty:
            st.info("No tasks found. Create a new task to get started.")
        else:
            # Display tasks in a dataframe
            st.dataframe(df, use_container_width=True)
    
    # Tab 2: Task Analytics
    with tab2:
        st.header("Task Analytics")
        
        # Fetch task data for analytics
        query = "SELECT module, COUNT(*) as count FROM tasks GROUP BY module"
        df_analytics = pd.read_sql_query(query, conn())
        
        if df_analytics.empty:
            st.info("No tasks found for analytics. Create tasks to see analytics.")
        else:
            # Create a bar chart of tasks per module
            fig = px.bar(
                df_analytics, 
                x="module", 
                y="count",
                title="Tasks per Module",
                labels={"module": "Module", "count": "Number of Tasks"},
                color="module"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Additional analytics
            total_tasks = df_analytics["count"].sum()
            st.metric("Total Tasks", total_tasks)
            
            # Get the most recent task
            query = "SELECT module, created_at FROM tasks ORDER BY created_at DESC LIMIT 1"
            latest_task = pd.read_sql_query(query, conn())
            if not latest_task.empty:
                st.metric("Latest Task", latest_task.iloc[0]["module"], 
                          latest_task.iloc[0]["created_at"])
    
    # Tab 3: Create Task
    with tab3:
        st.header("Create New Task")
        
        # Form to create a new task
        with st.form("new_task_form"):
            module = st.selectbox(
                "Module",
                options=["binance", "coingecko", "whale_alert", "openai", "custom"]
            )
            
            if module == "custom":
                module = st.text_input("Custom Module Name")
            
            payload = st.text_area("Payload (JSON or text)")
            result = st.text_area("Result (optional)")
            
            submit_button = st.form_submit_button("Create Task")
            
            if submit_button:
                if module and payload:
                    # Use the Optimizer to store the task
                    st.session_state.optimizer.optimize(module, payload, result)
                    st.success(f"Task created for module: {module}")
                else:
                    st.error("Module and Payload are required fields")
