import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from google_play_scraper import Sort, reviews, search
from textblob import TextBlob
from datetime import datetime, timedelta
import re
from collections import Counter, defaultdict
import json
import base64
from io import BytesIO
import time
import requests
import schedule
import threading
import hashlib
import secrets
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import LatentDirichletAllocation, PCA
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from scipy import stats
from scipy.spatial.distance import cosine
import networkx as nx
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import warnings
import asyncio
import aiohttp
import concurrent.futures
from functools import lru_cache
import holidays
import pytz
from dateutil import parser
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import os
from typing import Dict, List, Optional, Tuple
import uuid
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import subprocess
import sys

warnings.filterwarnings('ignore')

# NLTK Data Download
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet', quiet=True)

# Page Configuration
st.set_page_config(
    page_title="FeedbackForge Pro - Enterprise Analytics",
    page_icon="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEyIDJMMTMuMDkgOC4yNkwyMCA5TDEzLjA5IDE1Ljc0TDEyIDIyTDEwLjkxIDE1Ljc0TDQgOUwxMC45MSA4LjI2TDEyIDJaIiBmaWxsPSIjM0I4MkY2Ii8+Cjwvc3ZnPgo=",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root {
    --primary: #2563EB;
    --primary-dark: #1E40AF;
    --primary-light: #3B82F6;
    --secondary: #64748B;
    --background: #F8FAFC;
    --surface: #FFFFFF;
    --border: #E2E8F0;
    --text-primary: #0F172A;
    --text-secondary: #475569;
    --success: #059669;
    --warning: #D97706;
    --error: #DC2626;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    --radius: 8px;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main {
    background: var(--background);
    padding: 0;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

/* Fixed Top Navigation */
.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    z-index: 1000;
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 70px;
    box-shadow: var(--shadow);
}

.nav-brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

.nav-menu {
    display: flex;
    gap: 2rem;
    align-items: center;
}

.nav-item {
    color: var(--text-secondary);
    text-decoration: none;
    font-weight: 500;
    padding: 0.5rem 1rem;
    border-radius: var(--radius);
    transition: all 0.2s ease;
    cursor: pointer;
}

.nav-item:hover, .nav-item.active {
    background: var(--primary);
    color: white;
}

.nav-toggle {
    background: var(--primary);
    border: none;
    color: white;
    padding: 0.5rem;
    border-radius: var(--radius);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Main Content Area */
.main-content {
    margin-top: 80px;
    padding: 2rem;
}

.content-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow);
}

.page-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}

.page-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.page-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin: 0.5rem 0 0 0;
}

/* Metrics Cards */
.metrics-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow);
    transition: all 0.2s ease;
    text-align: center;
}

.metric-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
    line-height: 1;
}

.metric-label {
    font-size: 0.875rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Buttons */
.stButton > button {
    background: var(--primary);
    border: none;
    border-radius: var(--radius);
    color: white;
    font-weight: 600;
    font-size: 0.875rem;
    padding: 0.75rem 1.5rem;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.stButton > button:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
    box-shadow: var(--shadow-lg);
}

/* Input Styles */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stTextArea > div > div > textarea {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.75rem;
    font-size: 0.875rem;
    transition: border-color 0.2s ease;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
}

/* Sidebar */
.css-1d391kg {
    background: var(--text-primary);
    padding: 0;
}

.sidebar-content {
    padding: 2rem 1rem;
}

.sidebar-header {
    color: white;
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    text-align: center;
}

.sidebar-nav {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.sidebar-nav-item {
    background: rgba(255, 255, 255, 0.1);
    border: none;
    border-radius: var(--radius);
    color: white;
    padding: 0.75rem 1rem;
    text-align: left;
    font-weight: 500;
    transition: all 0.2s ease;
    cursor: pointer;
    font-size: 0.875rem;
}

.sidebar-nav-item:hover {
    background: rgba(255, 255, 255, 0.2);
}

.sidebar-nav-item.active {
    background: var(--primary);
    color: white;
}

/* Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.25rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.status-active {
    background: rgba(5, 150, 105, 0.1);
    color: var(--success);
}

.status-inactive {
    background: rgba(100, 116, 139, 0.1);
    color: var(--secondary);
}

/* Tables */
.dataframe {
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow);
}

.dataframe th {
    background: var(--background);
    color: var(--text-primary);
    font-weight: 600;
    padding: 1rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-size: 0.75rem;
}

.dataframe td {
    padding: 0.75rem 1rem;
    border-top: 1px solid var(--border);
    color: var(--text-primary);
}

/* Authentication */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background: var(--background);
}

.auth-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 3rem;
    box-shadow: var(--shadow-lg);
    width: 100%;
    max-width: 400px;
    text-align: center;
}

.auth-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.auth-subtitle {
    color: var(--text-secondary);
    margin-bottom: 2rem;
}

/* Alerts */
.stSuccess, .stWarning, .stError, .stInfo {
    border-radius: var(--radius);
    border: none;
    padding: 1rem;
    margin: 1rem 0;
}

.stSuccess {
    background: rgba(5, 150, 105, 0.1);
    color: var(--success);
}

.stWarning {
    background: rgba(217, 119, 6, 0.1);
    color: var(--warning);
}

.stError {
    background: rgba(220, 38, 38, 0.1);
    color: var(--error);
}

.stInfo {
    background: rgba(37, 99, 235, 0.1);
    color: var(--primary);
}

/* Charts */
.chart-container {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
}

/* Progress Bar */
.stProgress .st-bo {
    background: var(--primary);
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* Responsive */
@media (max-width: 768px) {
    .nav-menu {
        display: none;
    }
    
    .main-content {
        padding: 1rem;
    }
    
    .metrics-grid {
        grid-template-columns: 1fr;
    }
}
</style>
""", unsafe_allow_html=True)

# Database Setup
def setup_database():
    """Setup SQLite database for user management"""
    conn = sqlite3.connect('feedbackforge_users.db', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        session_token TEXT,
        api_key TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_settings (
        user_id INTEGER,
        setting_key TEXT,
        setting_value TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS analysis_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        app_name TEXT,
        analysis_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_summary TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create default admin
    admin_exists = cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_exists:
        admin_hash = generate_password_hash('Jaimatadiletsrock')
        cursor.execute('''
        INSERT INTO users (username, email, password_hash, role, api_key) 
        VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'FeedbackForge@outlook.com', admin_hash, 'admin', secrets.token_urlsafe(32)))
    
    conn.commit()
    conn.close()

# Initialize Database
setup_database()

# Authentication Manager
class AuthenticationManager:
    def __init__(self):
        self.db_path = 'feedbackforge_users.db'
    
    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def register_user(self, username: str, email: str, password: str, role: str = 'user') -> bool:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            password_hash = generate_password_hash(password)
            api_key = secrets.token_urlsafe(32)
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, api_key) 
            VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, role, api_key))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception:
            return False
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            user = cursor.execute('''
            SELECT id, username, email, password_hash, role, is_active, api_key 
            FROM users WHERE (username = ? OR email = ?) AND is_active = 1
            ''', (username, username)).fetchone()
            
            if user and check_password_hash(user[3], password):
                session_token = secrets.token_urlsafe(32)
                cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP, session_token = ? 
                WHERE id = ?
                ''', (session_token, user[0]))
                conn.commit()
                conn.close()
                
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[4],
                    'session_token': session_token,
                    'api_key': user[6]
                }
            conn.close()
            return None
        except Exception:
            return None
    
    def validate_session(self, session_token: str) -> Optional[Dict]:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            user = cursor.execute('''
            SELECT id, username, email, role, is_active, api_key 
            FROM users WHERE session_token = ? AND is_active = 1
            ''', (session_token,)).fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[3],
                    'session_token': session_token,
                    'api_key': user[5]
                }
            return None
        except Exception:
            return None
    
    def logout_user(self, session_token: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET session_token = NULL WHERE session_token = ?', (session_token,))
            conn.commit()
            conn.close()
        except Exception:
            pass

# Webhook Manager
class WebhookManager:
    def __init__(self):
        self.slack_webhooks = []
        self.discord_webhooks = []
        self.last_notification = {}
    
    def add_slack_webhook(self, webhook_url: str, channel_name: str = ""):
        webhook_data = {
            'url': webhook_url,
            'channel': channel_name,
            'type': 'slack',
            'active': True
        }
        self.slack_webhooks.append(webhook_data)
        return True
    
    def add_discord_webhook(self, webhook_url: str, channel_name: str = ""):
        webhook_data = {
            'url': webhook_url,
            'channel': channel_name,
            'type': 'discord',
            'active': True
        }
        self.discord_webhooks.append(webhook_data)
        return True
    
    def send_slack_notification(self, message: str, webhook_url: str = None):
        try:
            current_time = time.time()
            if webhook_url in self.last_notification:
                if current_time - self.last_notification[webhook_url] < 60:
                    return False
            
            if webhook_url is None and self.slack_webhooks:
                webhook_url = self.slack_webhooks[0]['url']
            
            if webhook_url:
                payload = {
                    'text': message,
                    'username': 'FeedbackForge Pro'
                }
                response = requests.post(webhook_url, json=payload, timeout=10)
                self.last_notification[webhook_url] = current_time
                return response.status_code == 200
        except Exception:
            return False
    
    def send_discord_notification(self, message: str, webhook_url: str = None):
        try:
            current_time = time.time()
            if webhook_url in self.last_notification:
                if current_time - self.last_notification[webhook_url] < 60:
                    return False
            
            if webhook_url is None and self.discord_webhooks:
                webhook_url = self.discord_webhooks[0]['url']
            
            if webhook_url:
                payload = {
                    'content': message,
                    'username': 'FeedbackForge Pro'
                }
                response = requests.post(webhook_url, json=payload, timeout=10)
                self.last_notification[webhook_url] = current_time
                return response.status_code in [200, 204]
        except Exception:
            return False

# Google Sheets Manager
class GoogleSheetsManager:
    def __init__(self, credentials_file: str = None):
        self.credentials_file = credentials_file
        self.client = None
        if credentials_file and os.path.exists(credentials_file):
            try:
                scope = [
                    "https://spreadsheets.google.com/feeds",
                    "https://www.googleapis.com/auth/drive"
                ]
                creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
                self.client = gspread.authorize(creds)
            except Exception:
                pass
    
    def update_sheet(self, spreadsheet_name: str, worksheet_name: str, data: pd.DataFrame):
        try:
            if not self.client:
                return False
            
            try:
                sheet = self.client.open(spreadsheet_name)
            except gspread.SpreadsheetNotFound:
                sheet = self.client.create(spreadsheet_name)
            
            try:
                worksheet = sheet.worksheet(worksheet_name)
            except gspread.WorksheetNotFound:
                worksheet = sheet.add_worksheet(title=worksheet_name, rows="1000", cols="26")
            
            worksheet.clear()
            data_list = [data.columns.tolist()] + data.values.tolist()
            worksheet.update('A1', data_list)
            
            return True
        except Exception:
            return False

# Review Analyzer
class ReviewAnalyzer:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            self.stop_words = set()
        
        try:
            self.lemmatizer = WordNetLemmatizer()
        except:
            self.lemmatizer = None
    
    def extract_package_name(self, url):
        if not url or not isinstance(url, str):
            return None
        
        patterns = [
            r'id=([a-zA-Z0-9_\.]+)',
            r'/store/apps/details\?id=([a-zA-Z0-9_\.]+)',
            r'play\.google\.com.*id=([a-zA-Z0-9_\.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                package_name = match.group(1)
                if self.validate_package_name(package_name):
                    return package_name
        return None
    
    def validate_package_name(self, package_name):
        if not package_name:
            return False
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*(\.[a-zA-Z][a-zA-Z0-9_]*)*$'
        return bool(re.match(pattern, package_name)) and len(package_name.split('.')) >= 2
    
    def get_app_name(self, package_name):
        if not package_name:
            return "Unknown App"
        parts = package_name.split('.')
        return parts[-1].replace('_', ' ').title()
    
    def advanced_sentiment_analysis(self, text):
        if pd.isna(text) or text.strip() == "":
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'sentiment': 'Neutral',
                'confidence': 0.0,
                'keywords': []
            }
        
        try:
            blob = TextBlob(str(text))
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
        except:
            polarity = 0.0
            subjectivity = 0.0
        
        # Keywords extraction
        text_lower = text.lower()
        positive_words = ['excellent', 'amazing', 'great', 'good', 'love', 'awesome', 'perfect']
        negative_words = ['terrible', 'awful', 'bad', 'hate', 'worst', 'horrible']
        
        found_keywords = []
        for word in positive_words:
            if word in text_lower:
                found_keywords.append(word)
        
        for word in negative_words:
            if word in text_lower:
                found_keywords.append(word)
        
        # Sentiment classification
        if polarity > 0.3:
            sentiment = "Positive"
            confidence = min(1.0, abs(polarity) + 0.2)
        elif polarity < -0.3:
            sentiment = "Negative"
            confidence = min(1.0, abs(polarity) + 0.2)
        else:
            sentiment = "Neutral"
            confidence = 0.5
        
        return {
            'polarity': polarity,
            'subjectivity': subjectivity,
            'sentiment': sentiment,
            'confidence': confidence,
            'keywords': found_keywords
        }
    
    def scrape_reviews(self, package_name, count=500, sort_by=Sort.NEWEST):
        try:
            with st.spinner("Extracting reviews from Google Play Store..."):
                result, continuation_token = reviews(
                    package_name,
                    lang='en',
                    country='us',
                    sort=sort_by,
                    count=count,
                    filter_score_with=None
                )
                
                if not result:
                    return pd.DataFrame()
                
                df = pd.DataFrame(result)
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                sentiments = []
                for idx, review in df.iterrows():
                    progress = (idx + 1) / len(df)
                    progress_bar.progress(progress)
                    status_text.text(f'Analyzing review {idx + 1} of {len(df)}...')
                    
                    sentiment_data = self.advanced_sentiment_analysis(review['content'])
                    sentiments.append(sentiment_data)
                
                # Add sentiment data to DataFrame
                for idx, sentiment in enumerate(sentiments):
                    for key, value in sentiment.items():
                        if key == 'keywords':
                            df.loc[idx, 'keywords'] = ', '.join(value) if value else ''
                        else:
                            df.loc[idx, key] = value
                
                progress_bar.empty()
                status_text.empty()
                
                return df
                
        except Exception as e:
            st.error(f"Error extracting reviews: {str(e)}")
            return pd.DataFrame()

# Session State Initialization
def initialize_session_state():
    session_defaults = {
        'current_page': 'login',
        'analyzed_data': None,
        'user_data': None,
        'session_token': None,
        'webhook_manager': WebhookManager(),
        'sheets_manager': GoogleSheetsManager(),
        'sidebar_collapsed': False
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# Initialize everything
initialize_session_state()
auth_manager = AuthenticationManager()
analyzer = ReviewAnalyzer()

# Top Navigation
def create_top_navigation():
    if st.session_state.current_page == 'login':
        return
    
    user = st.session_state.user_data
    
    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-brand">FeedbackForge Pro</div>
        <div class="nav-menu">
            <span class="nav-item" onclick="window.location.reload();">Dashboard</span>
            <span class="nav-item" onclick="document.querySelector('[data-testid=collapsedControl]').click();">Menu</span>
            <span class="nav-item">{user['username']}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Navigation
def create_sidebar_navigation():
    if st.session_state.current_page == 'login':
        return
    
    user = st.session_state.user_data
    
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-content">
            <div class="sidebar-header">
                Navigation Menu
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # User info
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.1); border-radius: 8px; padding: 1rem; margin-bottom: 2rem;">
            <div style="color: white; font-weight: 600; margin-bottom: 0.25rem;">{user['username']}</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.875rem;">{user['role'].title()}</div>
            <div style="color: rgba(255,255,255,0.6); font-size: 0.75rem;">Built by Ayush Pandey</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        pages = [
            ('dashboard', 'Dashboard'),
            ('playstore_analysis', 'Play Store Analysis'),
            ('gmb_analysis', 'Google My Business'),
            ('competitive_intelligence', 'Competitive Intelligence'),
            ('automation_center', 'Automation Center'),
            ('export_reports', 'Reports & Export'),
            ('password_reset', 'Password Reset'),
            ('settings', 'Settings')
        ]
        
        for page_key, page_name in pages:
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
        
        # Logout
        st.markdown("---")
        if st.button("Sign Out", key="logout_btn", use_container_width=True):
            logout_user()
            st.rerun()

# Authentication Functions
def show_login_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-title">FeedbackForge Pro</div>
            <div class="auth-subtitle">Enterprise Review Analytics Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab1, tab2 = st.tabs(["Sign In", "Register"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("Username or Email", placeholder="Enter your credentials")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                
                login_clicked = st.form_submit_button("Sign In", use_container_width=True)
                
                if login_clicked and username and password:
                    user_data = auth_manager.authenticate_user(username, password)
                    if user_data:
                        st.session_state.user_data = user_data
                        st.session_state.session_token = user_data['session_token']
                        st.session_state.current_page = 'dashboard'
                        st.success("Authentication successful")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            with st.form("register_form"):
                reg_username = st.text_input("Username", placeholder="Choose a username")
                reg_email = st.text_input("Email", placeholder="your.email@company.com")
                reg_password = st.text_input("Password", type="password", placeholder="Create a password")
                
                register_clicked = st.form_submit_button("Register", use_container_width=True)
                
                if register_clicked and reg_username and reg_email and reg_password:
                    if auth_manager.register_user(reg_username, reg_email, reg_password):
                        st.success("Registration successful - Please sign in")
                    else:
                        st.error("Registration failed - User may already exist")

def check_authentication():
    if st.session_state.session_token:
        user_data = auth_manager.validate_session(st.session_state.session_token)
        if user_data:
            st.session_state.user_data = user_data
            return True
    
    st.session_state.user_data = None
    st.session_state.session_token = None
    st.session_state.current_page = 'login'
    return False

def logout_user():
    if st.session_state.session_token:
        auth_manager.logout_user(st.session_state.session_token)
    
    for key in ['user_data', 'session_token', 'analyzed_data']:
        if key in st.session_state:
            st.session_state[key] = None
    
    st.session_state.current_page = 'login'

# Dashboard Functions
def create_metrics_dashboard(df, title="Analysis Metrics"):
    if df.empty:
        st.warning("No data available for metrics display")
        return
    
    st.subheader(title)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_reviews = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{total_reviews:,}</div>
            <div class="metric-label">Total Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if 'score' in df.columns:
            avg_rating = df['score'].mean()
        elif 'rating' in df.columns:
            avg_rating = df['rating'].mean()
        else:
            avg_rating = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_rating:.1f}</div>
            <div class="metric-label">Average Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if 'sentiment' in df.columns:
            positive_rate = (df['sentiment'].str.contains('Positive', na=False).sum() / len(df)) * 100
        else:
            positive_rate = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{positive_rate:.1f}%</div>
            <div class="metric-label">Positive Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if 'confidence' in df.columns:
            avg_confidence = df['confidence'].mean() * 100
        else:
            avg_confidence = 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{avg_confidence:.0f}%</div>
            <div class="metric-label">Analysis Confidence</div>
        </div>
        """, unsafe_allow_html=True)

def create_visualizations(df, title="Data Visualizations"):
    if df.empty:
        return
    
    st.subheader(title)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'sentiment' in df.columns:
            sentiment_counts = df['sentiment'].value_counts()
            fig = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                color_discrete_sequence=['#2563EB', '#059669', '#D97706', '#DC2626']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        rating_col = 'score' if 'score' in df.columns else 'rating' if 'rating' in df.columns else None
        if rating_col:
            rating_counts = df[rating_col].value_counts().sort_index()
            fig = px.bar(
                x=[f"{i} Stars" for i in rating_counts.index],
                y=rating_counts.values,
                title="Rating Distribution",
                color_discrete_sequence=['#2563EB']
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

# Page Functions
def dashboard_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Analytics Dashboard</div>
            <div class="page-subtitle">Welcome to FeedbackForge Pro - Enterprise Review Intelligence Platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.user_data
    
    # Quick actions
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Play Store Analysis", use_container_width=True):
            st.session_state.current_page = 'playstore_analysis'
            st.rerun()
    
    with col2:
        if st.button("GMB Analysis", use_container_width=True):
            st.session_state.current_page = 'gmb_analysis'
            st.rerun()
    
    with col3:
        if st.button("Competitive Intelligence", use_container_width=True):
            st.session_state.current_page = 'competitive_intelligence'
            st.rerun()
    
    with col4:
        if st.button("Automation Center", use_container_width=True):
            st.session_state.current_page = 'automation_center'
            st.rerun()
    
    # Dashboard metrics
    if st.session_state.analyzed_data is not None:
        st.success("Analysis data is available")
        create_metrics_dashboard(st.session_state.analyzed_data, "Current Analysis Overview")
        create_visualizations(st.session_state.analyzed_data, "Analysis Results")
    else:
        st.info("No analysis data available. Start by analyzing Play Store reviews or Google My Business reviews.")
    
    # System status
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="content-card">
            <h4>Play Store Analysis</h4>
            <p>Advanced review analysis with sentiment detection</p>
            <div class="status-indicator status-active">
                <div style="width: 6px; height: 6px; border-radius: 50%; background: currentColor;"></div>
                Active
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="content-card">
            <h4>Google My Business</h4>
            <p>Local business review monitoring and analysis</p>
            <div class="status-indicator status-active">
                <div style="width: 6px; height: 6px; border-radius: 50%; background: currentColor;"></div>
                Active
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="content-card">
            <h4>Automation</h4>
            <p>Slack, Discord, and Google Sheets integration</p>
            <div class="status-indicator status-active">
                <div style="width: 6px; height: 6px; border-radius: 50%; background: currentColor;"></div>
                Active
            </div>
        </div>
        """, unsafe_allow_html=True)

def playstore_analysis_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Play Store Analysis</div>
            <div class="page-subtitle">Comprehensive Google Play Store review analysis with advanced sentiment detection</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    with st.container():
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            url_input = st.text_input(
                "Google Play Store URL or Package Name",
                placeholder="https://play.google.com/store/apps/details?id=com.example.app",
                help="Enter the complete Play Store URL or just the package name"
            )
        
        with col2:
            review_count = st.selectbox(
                "Reviews to Extract",
                options=[100, 250, 500, 1000, 2000],
                index=2
            )
        
        with col3:
            sort_option = st.selectbox(
                "Sort Method",
                options=["Newest", "Rating", "Helpfulness"]
            )
    
    # Analysis button
    if st.button("Start Analysis", type="primary", use_container_width=True):
        if url_input:
            package_name = analyzer.extract_package_name(url_input)
            
            if package_name:
                sort_mapping = {
                    "Newest": Sort.NEWEST,
                    "Rating": Sort.RATING,
                    "Helpfulness": Sort.MOST_RELEVANT
                }
                
                df = analyzer.scrape_reviews(package_name, count=review_count, sort_by=sort_mapping[sort_option])
                
                if not df.empty:
                    st.session_state.analyzed_data = df
                    st.session_state.current_app_name = analyzer.get_app_name(package_name)
                    
                    # Send notifications if configured
                    if st.session_state.webhook_manager.slack_webhooks or st.session_state.webhook_manager.discord_webhooks:
                        message = f"Play Store analysis completed for {st.session_state.current_app_name}: {len(df)} reviews analyzed"
                        st.session_state.webhook_manager.send_slack_notification(message)
                        st.session_state.webhook_manager.send_discord_notification(message)
                    
                    st.success(f"Successfully analyzed {len(df)} reviews for {st.session_state.current_app_name}")
                    st.rerun()
                else:
                    st.error("No reviews found or extraction failed")
            else:
                st.error("Invalid URL or package name format")
        else:
            st.warning("Please enter a valid Google Play Store URL or package name")
    
    # Display results
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'Unknown App')
        
        st.markdown("---")
        st.subheader(f"Analysis Results: {app_name}")
        
        create_metrics_dashboard(df, "Play Store Metrics")
        create_visualizations(df, "Play Store Analytics")
        
        # Recent reviews
        st.subheader("Recent Reviews Sample")
        display_columns = ['at', 'userName', 'score', 'sentiment', 'confidence', 'content']
        available_columns = [col for col in display_columns if col in df.columns]
        
        if available_columns:
            sample_df = df[available_columns].head(10).copy()
            if 'at' in sample_df.columns:
                sample_df['at'] = pd.to_datetime(sample_df['at']).dt.strftime('%Y-%m-%d')
            if 'content' in sample_df.columns:
                sample_df['content'] = sample_df['content'].str[:100] + '...'
            
            st.dataframe(sample_df, use_container_width=True, hide_index=True)

def gmb_analysis_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Google My Business Analysis</div>
            <div class="page-subtitle">Local business review monitoring and sentiment analysis</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("GMB analysis feature is available for Premium Plan (999 INR/month). Contact FeedbackForge@outlook.com for upgrade.")
    
    # Placeholder for GMB functionality
    col1, col2 = st.columns([3, 1])
    
    with col1:
        gmb_url = st.text_input(
            "Google My Business URL",
            placeholder="https://www.google.com/maps/place/BusinessName",
            help="Enter your business Google Maps or GMB URL"
        )
    
    with col2:
        max_reviews = st.selectbox("Maximum Reviews", options=[25, 50, 100, 200], index=1)
    
    if st.button("Extract GMB Reviews", type="primary", use_container_width=True):
        if gmb_url:
            st.warning("GMB extraction requires premium features. Upgrade to access this functionality.")
        else:
            st.warning("Please enter a valid GMB URL")

def competitive_intelligence_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Competitive Intelligence</div>
            <div class="page-subtitle">Compare your app performance against competitors</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("Competitive Intelligence is available for Premium Plan (1999 INR/month). Contact FeedbackForge@outlook.com for upgrade.")

def automation_center_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Automation Center</div>
            <div class="page-subtitle">Webhook integrations and automated notifications</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Slack Integration", "Discord Integration", "Google Sheets"])
    
    with tab1:
        st.markdown("#### Slack Webhook Configuration")
        slack_webhook_url = st.text_input(
            "Slack Webhook URL",
            placeholder="https://hooks.slack.com/services/...",
            type="password"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Slack Webhook"):
                if slack_webhook_url:
                    st.session_state.webhook_manager.add_slack_webhook(slack_webhook_url)
                    st.success("Slack webhook configured successfully")
        
        with col2:
            if st.button("Test Slack"):
                test_message = f"Test notification from FeedbackForge Pro - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                if st.session_state.webhook_manager.send_slack_notification(test_message):
                    st.success("Slack test successful")
                else:
                    st.error("Slack test failed")
    
    with tab2:
        st.markdown("#### Discord Webhook Configuration")
        discord_webhook_url = st.text_input(
            "Discord Webhook URL",
            placeholder="https://discord.com/api/webhooks/...",
            type="password"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Discord Webhook"):
                if discord_webhook_url:
                    st.session_state.webhook_manager.add_discord_webhook(discord_webhook_url)
                    st.success("Discord webhook configured successfully")
        
        with col2:
            if st.button("Test Discord"):
                test_message = f"Test notification from FeedbackForge Pro - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                if st.session_state.webhook_manager.send_discord_notification(test_message):
                    st.success("Discord test successful")
                else:
                    st.error("Discord test failed")
    
    with tab3:
        st.markdown("#### Google Sheets Integration")
        uploaded_file = st.file_uploader(
            "Upload Google Service Account JSON",
            type=['json'],
            help="Upload your Google Service Account credentials file"
        )
        
        if uploaded_file:
            try:
                credentials_content = json.loads(uploaded_file.getvalue().decode('utf-8'))
                
                with open('google_credentials.json', 'w') as f:
                    json.dump(credentials_content, f)
                
                st.session_state.sheets_manager = GoogleSheetsManager('google_credentials.json')
                
                if st.session_state.sheets_manager.client:
                    st.success("Google Sheets integration configured successfully")
                else:
                    st.error("Failed to authenticate with Google Sheets")
            except Exception as e:
                st.error(f"Error configuring Google Sheets: {str(e)}")

def export_reports_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Reports & Data Export</div>
            <div class="page-subtitle">Export your analysis data in various formats</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        
        st.success(f"Analysis data available: {len(df):,} records")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Export as CSV", use_container_width=True):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"feedbackforge_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with col2:
            if st.button("Export as Excel", use_container_width=True):
                excel_buffer = BytesIO()
                df.to_excel(excel_buffer, index=False, engine='openpyxl')
                excel_data = excel_buffer.getvalue()
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"feedbackforge_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        
        with col3:
            if st.button("Export as JSON", use_container_width=True):
                json_data = df.to_json(orient='records', date_format='iso')
                st.download_button(
                    label="Download JSON",
                    data=json_data,
                    file_name=f"feedbackforge_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        # Preview
        st.subheader("Data Preview")
        preview_df = df.head(20)
        if 'content' in preview_df.columns:
            preview_df['content'] = preview_df['content'].str[:100] + '...'
        
        st.dataframe(preview_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("No data available for export. Please run an analysis first.")

def password_reset_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">Password Reset</div>
            <div class="page-subtitle">Change your account password securely</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("password_reset_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        
        if st.form_submit_button("Reset Password", use_container_width=True):
            if new_password != confirm_password:
                st.error("New passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                # Verify current password and update
                user = st.session_state.user_data
                if auth_manager.authenticate_user(user['username'], current_password):
                    try:
                        conn = auth_manager.get_connection()
                        cursor = conn.cursor()
                        new_hash = generate_password_hash(new_password)
                        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user['id']))
                        conn.commit()
                        conn.close()
                        st.success("Password updated successfully")
                    except Exception as e:
                        st.error(f"Failed to update password: {str(e)}")
                else:
                    st.error("Current password is incorrect")

def settings_page():
    create_top_navigation()
    
    st.markdown("""
    <div class="main-content">
        <div class="page-header">
            <div class="page-title">System Settings</div>
            <div class="page-subtitle">Configuration and system information</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    user = st.session_state.user_data
    
    tab1, tab2 = st.tabs(["User Information", "System Information"])
    
    with tab1:
        st.markdown("#### User Profile")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Username", value=user['username'], disabled=True)
            st.text_input("Role", value=user['role'].title(), disabled=True)
        
        with col2:
            st.text_input("Email", value=user['email'], disabled=True)
            st.text_input("API Key", value=user['api_key'][:20] + "..." if user.get('api_key') else "Not Generated", disabled=True)
    
    with tab2:
        st.markdown("#### System Information")
        
        system_info = {
            'Application': 'FeedbackForge Pro',
            'Version': '2.0.0 Enterprise',
            'Developer': 'Built by Ayush Pandey',
            'Support Email': 'FeedbackForge@outlook.com',
            'Python Version': sys.version.split()[0],
            'Streamlit Version': st.__version__ if hasattr(st, '__version__') else 'Latest',
            'Database': 'SQLite (Local)',
            'Pricing': 'Professional: 999 INR/month, Enterprise: 1999 INR/month'
        }
        
        for key, value in system_info.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{key}:**")
            with col2:
                st.markdown(value)

# Main Application Controller
def main():
    try:
        if st.session_state.current_page == 'login' or not check_authentication():
            show_login_page()
            return
        
        create_sidebar_navigation()
        
        if st.session_state.current_page == 'dashboard':
            dashboard_page()
        elif st.session_state.current_page == 'playstore_analysis':
            playstore_analysis_page()
        elif st.session_state.current_page == 'gmb_analysis':
            gmb_analysis_page()
        elif st.session_state.current_page == 'competitive_intelligence':
            competitive_intelligence_page()
        elif st.session_state.current_page == 'automation_center':
            automation_center_page()
        elif st.session_state.current_page == 'export_reports':
            export_reports_page()
        elif st.session_state.current_page == 'password_reset':
            password_reset_page()
        elif st.session_state.current_page == 'settings':
            settings_page()
        
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")

if __name__ == "__main__":
    main()
