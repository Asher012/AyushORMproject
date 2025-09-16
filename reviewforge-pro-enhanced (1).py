import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from bs4 import BeautifulSoup
import time
import json
import sqlite3
import secrets
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from google_play_scraper import Sort, reviews
from textblob import TextBlob
import re
from collections import Counter
from io import BytesIO
import random
from urllib.parse import unquote, quote, urlparse
import warnings
warnings.filterwarnings('ignore')

# PROFESSIONAL CONFIGURATION
st.set_page_config(
    page_title="ReviewForge Analytics Pro - Advanced Review Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# PROFESSIONAL CSS - COMPLETE DESIGN SYSTEM
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary: #2563EB;
    --primary-dark: #1E40AF;
    --secondary: #64748B;
    --success: #10B981;
    --warning: #F59E0B;
    --error: #EF4444;
    --background: #FAFAFA;
    --surface: #FFFFFF;
    --border: #E5E7EB;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
    --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
    --radius: 8px;
}

* {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main {
    background: var(--background);
}

.block-container {
    padding-top: 1rem;
    max-width: 1600px;
}

/* PROFESSIONAL HEADER */
.app-header {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark), #1e3a8a);
    color: white;
    padding: 2.5rem;
    border-radius: var(--radius);
    margin-bottom: 2rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.app-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at 30% 50%, rgba(255,255,255,0.1) 0%, transparent 50%);
    opacity: 0.3;
}

.header-title {
    font-size: 2.75rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.025em;
    position: relative;
    z-index: 1;
}

.header-subtitle {
    font-size: 1.2rem;
    opacity: 0.95;
    margin: 0;
    position: relative;
    z-index: 1;
    font-weight: 500;
}

/* PROFESSIONAL DATA SHEET DISPLAY */
.professional-sheet {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    margin: 1.5rem 0;
}

.sheet-toolbar {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    padding: 1rem;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.sheet-title {
    font-weight: 700;
    color: var(--text-primary);
    font-size: 1.1rem;
}

.sheet-header {
    background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
    padding: 0.75rem 1rem;
    border-bottom: 2px solid var(--border);
    font-weight: 600;
    color: var(--text-primary);
    display: grid;
    grid-template-columns: 50px 120px 80px 1fr 120px 120px 80px;
    gap: 1rem;
    align-items: center;
    font-size: 0.875rem;
}

.sheet-content {
    max-height: 600px;
    overflow-y: auto;
    background: var(--surface);
}

.sheet-row {
    display: grid;
    grid-template-columns: 50px 120px 80px 1fr 120px 120px 80px;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid #f1f5f9;
    align-items: start;
    gap: 1rem;
    transition: all 0.2s ease;
    font-size: 0.875rem;
    min-height: 60px;
}

.sheet-row:hover {
    background: #f8fafc;
    transform: translateX(2px);
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.1);
}

.sheet-row:nth-child(even) {
    background: rgba(248, 250, 252, 0.3);
}

.row-number {
    font-weight: 600;
    color: var(--secondary);
    text-align: center;
    background: rgba(37, 99, 235, 0.1);
    border-radius: 4px;
    padding: 0.25rem;
    font-size: 0.75rem;
}

.reviewer-cell {
    font-weight: 500;
    color: var(--text-primary);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.rating-cell {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.rating-stars {
    color: #fbbf24;
    font-weight: 700;
    font-size: 1rem;
}

.rating-number {
    font-weight: 600;
    color: var(--text-primary);
    font-size: 0.875rem;
}

.review-content-cell {
    font-size: 0.875rem;
    line-height: 1.5;
    color: var(--text-secondary);
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: all 0.2s ease;
    max-height: 4.5em;
}

.review-content-cell:hover {
    background: rgba(37, 99, 235, 0.05);
    color: var(--text-primary);
    box-shadow: inset 0 0 0 1px rgba(37, 99, 235, 0.2);
    max-height: none;
    -webkit-line-clamp: unset;
}

.sentiment-cell {
    text-align: center;
}

.sentiment-positive {
    background: linear-gradient(135deg, #ecfdf5, #d1fae5);
    color: #065f46;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    border: 1px solid #a7f3d0;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.sentiment-negative {
    background: linear-gradient(135deg, #fef2f2, #fecaca);
    color: #991b1b;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    border: 1px solid #fca5a5;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.sentiment-neutral {
    background: linear-gradient(135deg, #f8fafc, #e2e8f0);
    color: #475569;
    padding: 0.35rem 0.75rem;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.75rem;
    border: 1px solid #cbd5e1;
    text-transform: uppercase;
    letter-spacing: 0.025em;
}

.confidence-cell {
    text-align: center;
}

.confidence-bar-container {
    width: 100%;
    height: 8px;
    background: #e5e7eb;
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 0.25rem;
}

.confidence-bar {
    height: 100%;
    background: linear-gradient(90deg, var(--error), var(--warning), var(--success));
    transition: width 0.3s ease;
    border-radius: 4px;
}

.confidence-text {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-secondary);
}

.date-cell {
    font-size: 0.75rem;
    color: var(--text-secondary);
    text-align: center;
}

/* COMPETITIVE ANALYSIS STYLES */
.competitive-section {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: var(--shadow-lg);
}

.vs-battle-header {
    text-align: center;
    margin-bottom: 2rem;
}

.vs-title {
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--primary), var(--success));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
}

.vs-subtitle {
    color: var(--text-secondary);
    font-size: 1.125rem;
    font-weight: 500;
}

.battle-grid {
    display: grid;
    grid-template-columns: 1fr 120px 1fr;
    gap: 2rem;
    align-items: center;
    margin: 2rem 0;
}

.app-battle-card {
    background: linear-gradient(135deg, var(--surface), #f8fafc);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 2rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.app-battle-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(135deg, var(--primary), var(--success));
}

.app-battle-card.winner {
    border-color: var(--success);
    background: linear-gradient(135deg, var(--surface), rgba(16, 185, 129, 0.05));
    transform: scale(1.02);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

.app-battle-card.winner::before {
    background: linear-gradient(135deg, var(--success), #059669);
    height: 6px;
}

.battle-vs {
    text-align: center;
    font-size: 4rem;
    font-weight: 900;
    color: var(--primary);
    background: linear-gradient(135deg, var(--primary), var(--success));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100px;
    position: relative;
}

.battle-vs::before {
    content: '⚔️';
    position: absolute;
    top: -20px;
    font-size: 2rem;
}

.app-name {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 1rem;
    text-align: center;
}

.battle-score {
    font-size: 3rem;
    font-weight: 800;
    color: var(--primary);
    text-align: center;
    margin-bottom: 1rem;
}

.winner-crown {
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 2rem;
    animation: bounce 2s infinite;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-10px);
    }
    60% {
        transform: translateY(-5px);
    }
}

/* ENHANCED METRICS */
.metric-card {
    background: linear-gradient(135deg, var(--surface), #f8fafc);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    text-align: center;
    box-shadow: var(--shadow);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(135deg, var(--primary), var(--success));
}

.metric-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-5px);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 800;
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

/* ENHANCED BUTTONS */
.stButton > button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    border: none;
    border-radius: var(--radius);
    color: white;
    font-weight: 600;
    padding: 0.875rem 1.5rem;
    transition: all 0.3s ease;
    width: 100%;
    font-size: 1rem;
    box-shadow: var(--shadow);
    position: relative;
    overflow: hidden;
}

.stButton > button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
    background: linear-gradient(135deg, var(--primary-dark), var(--primary));
}

.stButton > button:hover::before {
    left: 100%;
}

/* NAVIGATION */
.nav-container {
    background: linear-gradient(135deg, var(--surface), #f8fafc);
    padding: 1rem;
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    margin-bottom: 2rem;
    border: 2px solid var(--border);
}

/* FILTERS */
.filter-container {
    background: linear-gradient(135deg, var(--surface), #f8fafc);
    border: 2px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin: 1.5rem 0;
    box-shadow: var(--shadow);
}

/* STATUS INDICATORS */
.status-live {
    background: linear-gradient(135deg, var(--success), #059669);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: var(--shadow);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { 
        opacity: 1; 
        transform: scale(1);
    }
    50% { 
        opacity: 0.8; 
        transform: scale(1.05);
    }
}

.status-offline {
    background: linear-gradient(135deg, var(--warning), #d97706);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 9999px;
    font-size: 0.875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    box-shadow: var(--shadow);
}

/* FORMS */
.stTextInput > div > div > input {
    border-radius: var(--radius);
    border: 2px solid var(--border);
    padding: 0.875rem;
    transition: all 0.2s;
    font-size: 1rem;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    transform: translateY(-1px);
}

.stSelectbox > div > div > div {
    border-radius: var(--radius);
    border: 2px solid var(--border);
}

/* AUTH PAGE */
.auth-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 80vh;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: var(--radius);
    margin: 2rem 0;
}

.auth-card {
    background: var(--surface);
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    width: 100%;
    max-width: 450px;
    text-align: center;
}

.auth-title {
    font-size: 2.5rem;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
}

.auth-subtitle {
    color: var(--text-secondary);
    margin-bottom: 2rem;
    font-size: 1.125rem;
    line-height: 1.5;
}

/* HIDE STREAMLIT ELEMENTS */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* RESPONSIVE DESIGN */
@media (max-width: 768px) {
    .header-title {
        font-size: 2rem;
    }
    
    .metric-value {
        font-size: 2rem;
    }
    
    .sheet-header,
    .sheet-row {
        grid-template-columns: 40px 100px 60px 1fr 100px 100px 60px;
        gap: 0.5rem;
        padding: 0.5rem;
        font-size: 0.75rem;
    }
    
    .battle-grid {
        grid-template-columns: 1fr;
        gap: 1rem;
    }
    
    .battle-vs {
        font-size: 2rem;
        height: 60px;
    }
    
    .vs-title {
        font-size: 2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# DATABASE SETUP
def setup_database():
    """Complete database setup"""
    conn = sqlite3.connect('reviewforge_pro.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        subscription_plan TEXT DEFAULT 'free',
        premium_access BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_login TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        session_token TEXT,
        api_key TEXT UNIQUE,
        live_notifications BOOLEAN DEFAULT 0,
        slack_webhook TEXT,
        discord_webhook TEXT,
        competitive_analysis_count INTEGER DEFAULT 0
    )
    ''')
    
    # Competitive analysis table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS competitive_analysis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        app1_package TEXT,
        app2_package TEXT,
        app1_name TEXT,
        app2_name TEXT,
        winner TEXT,
        confidence_score REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create admin user
    admin_exists = cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_exists:
        admin_hash = generate_password_hash('Ayush123')
        admin_api_key = secrets.token_urlsafe(32)
        
        cursor.execute('''
        INSERT INTO users (
            username, email, password_hash, role, subscription_plan, 
            premium_access, api_key, live_notifications
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'admin', 
            'admin@reviewforge.pro', 
            admin_hash, 
            'superadmin', 
            'enterprise', 
            1, 
            admin_api_key,
            1
        ))
    
    conn.commit()
    conn.close()

# Initialize database
setup_database()

# ADVANCED SENTIMENT ANALYSIS
class AdvancedSentimentAnalyzer:
    def __init__(self):
        self.positive_keywords = [
            'excellent', 'amazing', 'outstanding', 'fantastic', 'perfect', 'brilliant',
            'superb', 'wonderful', 'incredible', 'awesome', 'great', 'good', 'nice',
            'love', 'like', 'best', 'favorite', 'impressive', 'remarkable', 'exceptional',
            'pleased', 'satisfied', 'happy', 'delighted', 'thrilled', 'enjoy', 'recommend'
        ]
        
        self.negative_keywords = [
            'terrible', 'awful', 'horrible', 'worst', 'pathetic', 'disgusting', 'useless',
            'hate', 'dislike', 'bad', 'poor', 'disappointing', 'frustrating', 'annoying',
            'slow', 'buggy', 'crashes', 'freezes', 'broken', 'issues', 'problems',
            'waste', 'scam', 'fraud', 'fake', 'spam', 'confusing', 'difficult'
        ]
    
    def advanced_sentiment_analysis(self, text):
        """Enhanced sentiment analysis"""
        if not text or len(str(text).strip()) < 3:
            return self._default_sentiment()
        
        text_str = str(text).lower().strip()
        
        # TextBlob Analysis
        try:
            blob = TextBlob(text_str)
            textblob_polarity = blob.sentiment.polarity
            textblob_subjectivity = blob.sentiment.subjectivity
        except:
            textblob_polarity = 0.0
            textblob_subjectivity = 0.5
        
        # Keyword Analysis
        positive_score = sum(1 for word in self.positive_keywords if word in text_str)
        negative_score = sum(1 for word in self.negative_keywords if word in text_str)
        
        # Combined Analysis
        total_words = len(text_str.split())
        keyword_score = (positive_score - negative_score) / max(1, total_words) * 3
        final_polarity = (textblob_polarity * 0.6) + (keyword_score * 0.4)
        
        # Determine sentiment
        if final_polarity >= 0.1:
            sentiment = "Positive"
            confidence = min(1.0, abs(final_polarity) * 2.5 + 0.4)
        elif final_polarity <= -0.1:
            sentiment = "Negative"  
            confidence = min(1.0, abs(final_polarity) * 2.5 + 0.4)
        else:
            sentiment = "Neutral"
            confidence = 0.65 + abs(final_polarity) * 0.5
        
        return {
            'sentiment': sentiment,
            'confidence': round(confidence, 3),
            'polarity': round(final_polarity, 3),
            'subjectivity': round(textblob_subjectivity, 3),
            'positive_keywords': positive_score,
            'negative_keywords': negative_score,
            'word_count': total_words
        }
    
    def _default_sentiment(self):
        return {
            'sentiment': 'Neutral',
            'confidence': 0.5,
            'polarity': 0.0,
            'subjectivity': 0.5,
            'positive_keywords': 0,
            'negative_keywords': 0,
            'word_count': 0
        }

# AUTHENTICATION MANAGER
class AuthenticationManager:
    def __init__(self):
        self.db_path = 'reviewforge_pro.db'
    
    def get_connection(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)
    
    def authenticate_user(self, username: str, password: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            user = cursor.execute('''
            SELECT id, username, email, password_hash, role, subscription_plan, 
                   premium_access, api_key, live_notifications, slack_webhook, 
                   discord_webhook, competitive_analysis_count
            FROM users WHERE (username = ? OR email = ?) AND is_active = 1
            ''', (username, username)).fetchone()
            
            if user and check_password_hash(user[3], password):
                session_token = secrets.token_urlsafe(32)
                cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP, session_token = ? 
                WHERE id = ?
                ''', (session_token, user[0]))
                conn.commit()
                
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[4],
                    'subscription_plan': user[5],
                    'premium_access': bool(user[6]) or user[4] in ['admin', 'superadmin'],
                    'session_token': session_token,
                    'api_key': user[7],
                    'live_notifications': bool(user[8]),
                    'slack_webhook': user[9],
                    'discord_webhook': user[10],
                    'competitive_analysis_count': user[11] or 0
                }
                
                conn.close()
                return user_data
            
            conn.close()
            return None
            
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None
    
    def validate_session(self, session_token: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            user = cursor.execute('''
            SELECT id, username, email, role, subscription_plan, premium_access, 
                   api_key, live_notifications, slack_webhook, discord_webhook, 
                   competitive_analysis_count
            FROM users WHERE session_token = ? AND is_active = 1
            ''', (session_token,)).fetchone()
            
            if user:
                user_data = {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'role': user[3],
                    'subscription_plan': user[4],
                    'premium_access': bool(user[5]) or user[3] in ['admin', 'superadmin'],
                    'session_token': session_token,
                    'api_key': user[6],
                    'live_notifications': bool(user[7]),
                    'slack_webhook': user[8],
                    'discord_webhook': user[9],
                    'competitive_analysis_count': user[10] or 0
                }
                conn.close()
                return user_data
            
            conn.close()
            return None
            
        except Exception:
            return None
    
    def register_user(self, username: str, email: str, password: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            password_hash = generate_password_hash(password)
            api_key = secrets.token_urlsafe(32)
            
            cursor.execute('''
            INSERT INTO users (username, email, password_hash, api_key) 
            VALUES (?, ?, ?, ?)
            ''', (username, email, password_hash, api_key))
            
            conn.commit()
            conn.close()
            return True
            
        except sqlite3.IntegrityError:
            return False
        except Exception:
            return False
    
    def logout_user(self, session_token: str):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET session_token = NULL WHERE session_token = ?', (session_token,))
            conn.commit()
            conn.close()
        except Exception:
            pass

# PROFESSIONAL REVIEW ANALYZER
class ProfessionalReviewAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = AdvancedSentimentAnalyzer()
    
    def extract_package_name(self, url):
        """Extract package name from URL"""
        if not url:
            return None
        
        url = url.strip().lower()
        
        patterns = [
            r'id=([a-zA-Z0-9_\.]+)',
            r'/store/apps/details\?id=([a-zA-Z0-9_\.]+)',
            r'details\?id=([a-zA-Z0-9_\.]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        if re.match(r'^[a-zA-Z0-9_\.]+$', url) and '.' in url:
            return url
            
        return None
    
    def get_app_name(self, package_name):
        """Get app name from package"""
        if not package_name:
            return "Unknown App"
        
        # Common app mappings
        app_names = {
            'com.whatsapp': 'WhatsApp',
            'com.instagram.android': 'Instagram',
            'com.spotify.music': 'Spotify',
            'com.netflix.mediaclient': 'Netflix',
            'com.tiktok': 'TikTok',
            'com.telegram.messenger': 'Telegram'
        }
        
        if package_name in app_names:
            return app_names[package_name]
        
        # Fallback extraction
        name_part = package_name.split('.')[-1]
        return name_part.replace('_', ' ').title()
    
    def extract_playstore_reviews_enhanced(self, package_name, count=1000):
        """Enhanced review extraction with progress tracking"""
        try:
            app_name = self.get_app_name(package_name)
            st.info(f"🚀 Starting analysis for: **{app_name}**")
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            status_text.text("📱 Phase 1/3: Extracting reviews...")
            
            # Extract reviews
            all_reviews = []
            batch_size = min(200, count)
            batches_needed = min((count + batch_size - 1) // batch_size, 5)
            
            for batch_num in range(batches_needed):
                try:
                    batch_count = min(batch_size, count - len(all_reviews))
                    
                    result, continuation_token = reviews(
                        package_name,
                        lang='en',
                        country='us',
                        sort=Sort.NEWEST,
                        count=batch_count
                    )
                    
                    if result:
                        all_reviews.extend(result)
                        progress = (batch_num + 1) / batches_needed * 0.4
                        progress_bar.progress(progress)
                        status_text.text(f"📊 Extracted {len(all_reviews)} reviews...")
                    else:
                        break
                        
                except Exception as e:
                    if batch_num == 0:
                        st.error(f"❌ Extraction failed: {str(e)}")
                        return pd.DataFrame()
                    break
            
            if not all_reviews:
                st.error("❌ No reviews found")
                return pd.DataFrame()
            
            # Process data
            status_text.text("🔄 Phase 2/3: Processing data...")
            df = pd.DataFrame(all_reviews)
            progress_bar.progress(0.4)
            
            # Sentiment analysis
            status_text.text("🧠 Phase 3/3: AI sentiment analysis...")
            
            sentiment_data = []
            total_reviews = len(df)
            
            for idx, review in df.iterrows():
                sentiment_result = self.sentiment_analyzer.advanced_sentiment_analysis(review['content'])
                sentiment_data.append(sentiment_result)
                
                progress = 0.4 + ((idx + 1) / total_reviews) * 0.6
                progress_bar.progress(progress)
            
            # Add sentiment data
            for idx, sentiment in enumerate(sentiment_data):
                for key, value in sentiment.items():
                    df.loc[idx, key] = value
            
            # Additional metrics
            df['review_length'] = df['content'].str.len()
            df['is_detailed'] = df['review_length'] > 100
            df['quality_score'] = np.clip(
                (df['review_length'] / 150 * 0.3 +
                 df['confidence'] * 0.4 +
                 (df['positive_keywords'] + df['negative_keywords']) / 10 * 0.3), 
                0, 5
            ).round(2)
            
            progress_bar.progress(1.0)
            status_text.text("✅ Analysis complete!")
            time.sleep(1)
            progress_bar.empty()
            status_text.empty()
            
            st.success(f"🎉 Analyzed {len(df)} reviews for {app_name}")
            return df
            
        except Exception as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            return pd.DataFrame()
    
    def competitive_analysis(self, package1, package2, review_count=500):
        """Competitive analysis between two apps"""
        app1_name = self.get_app_name(package1)
        app2_name = self.get_app_name(package2)
        
        st.markdown("""
        <div class="competitive-section">
            <div class="vs-battle-header">
                <div class="vs-title">COMPETITIVE ANALYSIS</div>
                <div class="vs-subtitle">AI-Powered App Comparison</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"### 📱 {app1_name}")
            with st.spinner(f"Analyzing {app1_name}..."):
                df1 = self.extract_playstore_reviews_enhanced(package1, review_count)
        
        with col2:
            st.markdown('<div class="battle-vs">VS</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"### 📱 {app2_name}")
            with st.spinner(f"Analyzing {app2_name}..."):
                df2 = self.extract_playstore_reviews_enhanced(package2, review_count)
        
        if df1.empty or df2.empty:
            st.error("❌ Could not extract reviews for comparison")
            return None, None, None
        
        comparison_data = self._perform_competitive_comparison(df1, df2, package1, package2)
        return df1, df2, comparison_data
    
    def _perform_competitive_comparison(self, df1, df2, package1, package2):
        """Perform competitive comparison"""
        app1_name = self.get_app_name(package1)
        app2_name = self.get_app_name(package2)
        
        # Calculate metrics
        metrics1 = self._calculate_app_metrics(df1)
        metrics2 = self._calculate_app_metrics(df2)
        
        # Scoring system (100 points)
        scores = {'app1': 0, 'app2': 0}
        
        # Rating (30 points)
        if metrics1['avg_rating'] > metrics2['avg_rating']:
            scores['app1'] += 30
            scores['app2'] += 25
        else:
            scores['app2'] += 30
            scores['app1'] += 25
        
        # Sentiment (40 points)
        if metrics1['positive_rate'] > metrics2['positive_rate']:
            scores['app1'] += 40
            scores['app2'] += 30
        else:
            scores['app2'] += 40
            scores['app1'] += 30
        
        # Engagement (30 points)
        if metrics1['detailed_review_rate'] > metrics2['detailed_review_rate']:
            scores['app1'] += 30
            scores['app2'] += 20
        else:
            scores['app2'] += 30
            scores['app1'] += 20
        
        # Determine winner
        total_score_1 = scores['app1']
        total_score_2 = scores['app2']
        
        if total_score_1 > total_score_2:
            winner = app1_name
            confidence = (total_score_1 / (total_score_1 + total_score_2)) * 100
        else:
            winner = app2_name
            confidence = (total_score_2 / (total_score_1 + total_score_2)) * 100
        
        return {
            'app1_name': app1_name,
            'app2_name': app2_name,
            'app1_metrics': metrics1,
            'app2_metrics': metrics2,
            'app1_score': round(total_score_1, 1),
            'app2_score': round(total_score_2, 1),
            'winner': winner,
            'confidence': round(confidence, 1)
        }
    
    def _calculate_app_metrics(self, df):
        """Calculate app metrics"""
        return {
            'total_reviews': len(df),
            'avg_rating': round(df['score'].mean(), 2),
            'positive_rate': round((df['sentiment'] == 'Positive').sum() / len(df) * 100, 1),
            'negative_rate': round((df['sentiment'] == 'Negative').sum() / len(df) * 100, 1),
            'neutral_rate': round((df['sentiment'] == 'Neutral').sum() / len(df) * 100, 1),
            'avg_confidence': round(df['confidence'].mean(), 3),
            'avg_review_length': round(df['review_length'].mean(), 0),
            'detailed_review_rate': round((df['is_detailed']).sum() / len(df) * 100, 1),
            'avg_quality_score': round(df['quality_score'].mean(), 2)
        }

# PROFESSIONAL DATA SHEET
class ProfessionalDataSheet:
    def create_review_sheet(self, df, app_name="App", max_rows=100):
        """Create professional sheet display"""
        if df.empty:
            st.warning("📊 No data to display")
            return
        
        display_df = df.head(max_rows).copy()
        
        # Sheet container
        st.markdown(f'''
        <div class="professional-sheet">
            <div class="sheet-toolbar">
                <div class="sheet-title">📊 Review Analysis Sheet - {app_name}</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">
                    Showing {len(display_df):,} of {len(df):,} reviews
                </div>
            </div>
            
            <div class="sheet-header">
                <div><strong>#</strong></div>
                <div><strong>👤 Reviewer</strong></div>
                <div><strong>⭐ Rating</strong></div>
                <div><strong>💬 Review Content</strong></div>
                <div><strong>😊 Sentiment</strong></div>
                <div><strong>🎯 Confidence</strong></div>
                <div><strong>📅 Date</strong></div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Sheet content
        sheet_html = '<div class="sheet-content">'
        
        for idx, row in display_df.iterrows():
            row_num = idx + 1
            reviewer = str(row.get('userName', f'User {row_num}'))[:15] + ('...' if len(str(row.get('userName', ''))) > 15 else '')
            rating = int(row.get('score', 0))
            review_text = str(row.get('content', ''))
            sentiment = row.get('sentiment', 'Neutral')
            confidence = float(row.get('confidence', 0.5))
            review_date = str(row.get('at', 'Unknown'))[:10] if row.get('at') else 'Unknown'
            
            # Format data
            stars = '⭐' * rating if rating > 0 else '⭐'
            sentiment_class = f'sentiment-{sentiment.lower()}'
            confidence_percent = f'{confidence * 100:.0f}%'
            confidence_width = f'{confidence * 100:.0f}%'
            
            sheet_html += f'''
            <div class="sheet-row">
                <div class="row-number">{row_num}</div>
                <div class="reviewer-cell" title="{reviewer}">{reviewer}</div>
                <div class="rating-cell">
                    <span class="rating-stars" title="{rating}/5 stars">{stars}</span>
                    <span class="rating-number">{rating}</span>
                </div>
                <div class="review-content-cell" title="Click to expand">{review_text}</div>
                <div class="sentiment-cell">
                    <span class="{sentiment_class}">{sentiment}</span>
                </div>
                <div class="confidence-cell">
                    <div class="confidence-bar-container">
                        <div class="confidence-bar" style="width: {confidence_width}"></div>
                    </div>
                    <div class="confidence-text">{confidence_percent}</div>
                </div>
                <div class="date-cell">{review_date}</div>
            </div>
            '''
        
        sheet_html += '</div>'
        st.markdown(sheet_html, unsafe_allow_html=True)
        
        if len(df) > max_rows:
            st.info(f"📄 Displaying first {max_rows} of {len(df):,} reviews")

# SESSION STATE MANAGEMENT
def init_session_state():
    """Initialize session state"""
    defaults = {
        'current_page': 'login',
        'user_data': None,
        'session_token': None,
        'analyzed_data': None,
        'competitive_data': None,
        'current_app_name': None,
        'last_activity': datetime.now()
    }
    
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

# Initialize components
init_session_state()
auth_manager = AuthenticationManager()
analyzer = ProfessionalReviewAnalyzer()
data_sheet = ProfessionalDataSheet()

# NAVIGATION FUNCTIONS
def create_header():
    """Create professional header"""
    if st.session_state.current_page == 'login':
        return
    
    user = st.session_state.user_data
    if not user:
        return
    
    status_text = "LIVE" if user.get('live_notifications') else "OFFLINE"
    status_class = "status-live" if user.get('live_notifications') else "status-offline"
    
    st.markdown(f"""
    <div class="app-header">
        <div class="header-title">ReviewForge Analytics Pro</div>
        <div class="header-subtitle">
            Advanced Review Intelligence Platform | User: {user['username']} | 
            Status: <span class="{status_class}">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_navigation():
    """Create navigation"""
    if st.session_state.current_page == 'login':
        return
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        if st.button("🏠 Dashboard", key="nav_dashboard", use_container_width=True):
            st.session_state.current_page = 'dashboard'
            st.rerun()
    
    with col2:
        if st.button("📱 Play Store", key="nav_playstore", use_container_width=True):
            st.session_state.current_page = 'playstore'
            st.rerun()
    
    with col3:
        if st.button("🆚 Competitive", key="nav_competitive", use_container_width=True):
            st.session_state.current_page = 'competitive'
            st.rerun()
    
    with col4:
        if st.button("🔔 Notifications", key="nav_notifications", use_container_width=True):
            st.session_state.current_page = 'notifications'
            st.rerun()
    
    with col5:
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.session_state.current_page = 'settings'
            st.rerun()
    
    with col6:
        if st.button("🚪 Logout", key="nav_logout", use_container_width=True):
            logout_user()
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_sidebar():
    """Create sidebar"""
    if st.session_state.current_page == 'login':
        return
    
    user = st.session_state.user_data
    if not user:
        return
    
    with st.sidebar:
        st.markdown("### 👤 User Info")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Role:** {user['role'].title()}")
        st.write(f"**Plan:** {user['subscription_plan'].title()}")
        
        st.markdown("---")
        st.markdown("### 📊 Quick Stats")
        
        playstore_count = len(st.session_state.analyzed_data) if st.session_state.analyzed_data is not None else 0
        competitive_count = user.get('competitive_analysis_count', 0)
        
        st.metric("Play Store Reviews", f"{playstore_count:,}")
        st.metric("Competitive Analyses", f"{competitive_count}")
        
        st.markdown("---")
        if st.button("🚪 Sign Out", key="sidebar_logout", use_container_width=True):
            logout_user()

# AUTHENTICATION
def show_login():
    """Login page"""
    st.markdown("""
    <div class="auth-container">
        <div class="auth-card">
            <div class="auth-title">ReviewForge Analytics Pro</div>
            <div class="auth-subtitle">
                Advanced Review Intelligence Platform
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Sign In", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                st.markdown("### Access Dashboard")
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                
                st.info("🔑 Demo: admin / Ayush123Pro")
                
                if st.form_submit_button("🚀 Sign In", use_container_width=True):
                    if username and password:
                        user_data = auth_manager.authenticate_user(username, password)
                        if user_data:
                            st.session_state.user_data = user_data
                            st.session_state.session_token = user_data['session_token']
                            st.session_state.current_page = 'dashboard'
                            st.success("✅ Login successful!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials")
                    else:
                        st.warning("⚠️ Please enter credentials")
        
        with tab2:
            with st.form("register_form"):
                st.markdown("### Create Account")
                reg_username = st.text_input("Username", placeholder="Choose username")
                reg_email = st.text_input("Email", placeholder="your.email@company.com")
                reg_password = st.text_input("Password", type="password", placeholder="Strong password")
                
                if st.form_submit_button("✨ Create Account", use_container_width=True):
                    if reg_username and reg_email and reg_password:
                        if len(reg_password) >= 6:
                            if auth_manager.register_user(reg_username, reg_email, reg_password):
                                st.success("🎉 Account created! Please sign in.")
                            else:
                                st.error("❌ Username/email exists")
                        else:
                            st.error("⚠️ Password too short")
                    else:
                        st.warning("⚠️ Fill all fields")

def check_authentication():
    """Check authentication"""
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
    """Logout user"""
    if st.session_state.session_token:
        auth_manager.logout_user(st.session_state.session_token)
    
    for key in list(st.session_state.keys()):
        if key != 'current_page':
            del st.session_state[key]
    
    st.session_state.current_page = 'login'
    st.rerun()

# PAGE FUNCTIONS
def dashboard_page():
    """Dashboard page"""
    user = st.session_state.user_data
    
    st.markdown("## 📊 Analytics Dashboard")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        playstore_count = len(st.session_state.analyzed_data) if st.session_state.analyzed_data is not None else 0
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{playstore_count:,}</div>
            <div class="metric-label">Play Store Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        competitive_count = user.get('competitive_analysis_count', 0)
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{competitive_count}</div>
            <div class="metric-label">Competitive Analyses</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        premium_status = "Pro" if user.get('premium_access') else "Free"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{premium_status}</div>
            <div class="metric-label">Account Tier</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        live_status = "Live" if user.get('live_notifications') else "Off"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{live_status}</div>
            <div class="metric-label">Notifications</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("## 🚀 Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📱 Play Store Analysis")
        st.write("Advanced sentiment analysis with professional sheet display")
        if st.button("🔍 Analyze App", key="dash_playstore", use_container_width=True):
            st.session_state.current_page = 'playstore'
            st.rerun()
    
    with col2:
        st.markdown("#### 🆚 Competitive Analysis")
        st.write("Compare two apps side-by-side with AI scoring")
        if st.button("⚔️ Compare Apps", key="dash_competitive", use_container_width=True):
            st.session_state.current_page = 'competitive'
            st.rerun()
    
    with col3:
        st.markdown("#### 🔔 Live Notifications")
        st.write("Setup real-time Slack/Discord notifications")
        if st.button("📋 Setup Alerts", key="dash_notifications", use_container_width=True):
            st.session_state.current_page = 'notifications'
            st.rerun()
    
    # Recent Analysis
    if st.session_state.analyzed_data is not None:
        st.markdown("## 📈 Recent Analysis")
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'App')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.success(f"✅ {app_name} - {len(df):,} reviews analyzed")
            if 'sentiment' in df.columns:
                positive_rate = (df['sentiment'] == 'Positive').sum() / len(df) * 100
                st.metric("Positive Sentiment", f"{positive_rate:.1f}%")
        
        with col2:
            if 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                fig = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title=f"Sentiment - {app_name}",
                    color_discrete_map={
                        'Positive': '#10B981',
                        'Negative': '#EF4444',
                        'Neutral': '#64748B'
                    }
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

def playstore_analysis_page():
    """Play Store analysis page"""
    st.markdown("## 📱 Play Store Review Analysis")
    
    # Input section
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        url_input = st.text_input(
            "Play Store URL or Package Name",
            placeholder="https://play.google.com/store/apps/details?id=com.example.app",
            help="🔍 Enter complete Play Store URL or package name"
        )
    
    with col2:
        review_count = st.selectbox("Reviews", [500, 1000, 2000], index=1)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        analyze_btn = st.button("🚀 Start Analysis", type="primary", use_container_width=True)
    
    # Examples
    with st.expander("📖 Examples"):
        st.code("com.whatsapp", language="text")
        st.code("com.instagram.android", language="text")
        st.code("https://play.google.com/store/apps/details?id=com.spotify.music", language="text")
    
    # Analysis execution
    if analyze_btn:
        if url_input:
            package_name = analyzer.extract_package_name(url_input)
            
            if package_name:
                df = analyzer.extract_playstore_reviews_enhanced(package_name, review_count)
                
                if not df.empty:
                    st.session_state.analyzed_data = df
                    st.session_state.current_app_name = analyzer.get_app_name(package_name)
                    st.rerun()
                else:
                    st.error("❌ No reviews found")
            else:
                st.error("❌ Invalid URL format")
        else:
            st.warning("⚠️ Please enter URL or package name")
    
    # Display results
    if st.session_state.analyzed_data is not None:
        df = st.session_state.analyzed_data
        app_name = st.session_state.get('current_app_name', 'App')
        
        st.markdown("---")
        st.markdown(f"## 📊 Analysis Results: {app_name}")
        
        # Enhanced metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(df):,}</div>
                <div class="metric-label">Total Reviews</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_rating = df['score'].mean() if 'score' in df.columns else 0
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{avg_rating:.1f}⭐</div>
                <div class="metric-label">Average Rating</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if 'sentiment' in df.columns:
                positive_rate = (df['sentiment'] == 'Positive').sum() / len(df) * 100
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{positive_rate:.1f}%</div>
                    <div class="metric-label">Positive Reviews</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if 'confidence' in df.columns:
                avg_confidence = df['confidence'].mean() * 100
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_confidence:.0f}%</div>
                    <div class="metric-label">AI Confidence</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Charts
        st.markdown("### 📈 Analytics Charts")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'sentiment' in df.columns:
                sentiment_counts = df['sentiment'].value_counts()
                fig = px.pie(
                    values=sentiment_counts.values,
                    names=sentiment_counts.index,
                    title="Sentiment Distribution",
                    color_discrete_map={
                        'Positive': '#10B981',
                        'Negative': '#EF4444',
                        'Neutral': '#64748B'
                    }
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if 'score' in df.columns:
                rating_counts = df['score'].value_counts().sort_index()
                fig = px.bar(
                    x=rating_counts.index,
                    y=rating_counts.values,
                    title="Rating Distribution",
                    labels={'x': 'Stars', 'y': 'Count'},
                    color=rating_counts.values,
                    color_continuous_scale='viridis'
                )
                fig.update_layout(height=350)
                st.plotly_chart(fig, use_container_width=True)
        
        # Professional Sheet Display
        st.markdown("### 📋 Professional Review Sheet")
        data_sheet.create_review_sheet(df, app_name, max_rows=100)
        
        # Export options
        st.markdown("### 💾 Export Options")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv_data = df.to_csv(index=False)
            st.download_button(
                "📊 Download CSV",
                csv_data,
                f"{app_name}_analysis.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            excel_buffer = BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            st.download_button(
                "📈 Download Excel",
                excel_buffer.getvalue(),
                f"{app_name}_analysis.xlsx",
                use_container_width=True
            )
        
        with col3:
            summary_data = {
                'app_name': app_name,
                'total_reviews': len(df),
                'average_rating': round(df['score'].mean(), 2) if 'score' in df.columns else 0,
                'sentiment_breakdown': df['sentiment'].value_counts().to_dict() if 'sentiment' in df.columns else {},
                'analysis_date': datetime.now().isoformat()
            }
            
            summary_json = json.dumps(summary_data, indent=2)
            st.download_button(
                "📋 Download Report",
                summary_json,
                f"{app_name}_report.json",
                "application/json",
                use_container_width=True
            )

def competitive_analysis_page():
    """Competitive analysis page"""
    user = st.session_state.user_data
    
    st.markdown("## 🆚 Competitive Analysis")
    st.markdown("Compare two apps side-by-side with advanced AI analysis")
    
    # Input section
    col1, col2, col3 = st.columns([5, 1, 5])
    
    with col1:
        st.markdown("### 📱 First App")
        app1_input = st.text_input(
            "App 1 URL/Package",
            placeholder="com.whatsapp or Play Store URL",
            help="Enter package name or Play Store URL"
        )
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown('<div class="battle-vs">VS</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 📱 Second App")
        app2_input = st.text_input(
            "App 2 URL/Package", 
            placeholder="com.instagram.android or Play Store URL",
            help="Enter package name or Play Store URL"
        )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        review_count = st.selectbox("Reviews per App", [300, 500, 1000], index=1)
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        start_comparison = st.button("⚔️ Start Battle", type="primary", use_container_width=True)
    
    with col3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💡 Examples", use_container_width=True):
            st.info("WhatsApp vs Telegram: com.whatsapp vs com.telegram.messenger")
    
    # Execute comparison
    if start_comparison:
        if app1_input and app2_input:
            package1 = analyzer.extract_package_name(app1_input)
            package2 = analyzer.extract_package_name(app2_input)
            
            if package1 and package2:
                if package1 != package2:
                    df1, df2, comparison_data = analyzer.competitive_analysis(package1, package2, review_count)
                    
                    if df1 is not None and df2 is not None and comparison_data is not None:
                        st.session_state.competitive_data = comparison_data
                        st.session_state.analyzed_data = df1
                        
                        # Update competitive count
                        try:
                            conn = auth_manager.get_connection()
                            cursor = conn.cursor()
                            cursor.execute(
                                'UPDATE users SET competitive_analysis_count = competitive_analysis_count + 1 WHERE id = ?',
                                (user['id'],)
                            )
                            conn.commit()
                            conn.close()
                        except:
                            pass
                        
                        st.rerun()
                else:
                    st.error("❌ Please enter different apps")
            else:
                st.error("❌ Invalid package names")
        else:
            st.warning("⚠️ Please enter both apps")
    
    # Display results
    if st.session_state.competitive_data is not None:
        comp_data = st.session_state.competitive_data
        
        st.markdown("---")
        st.markdown("## 🏆 Battle Results")
        
        # Winner announcement
        st.success(f"🎉 **Winner: {comp_data['winner']}** with {comp_data['confidence']:.1f}% confidence!")
        
        # Battle cards
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.markdown(f"### 📱 {comp_data['app1_name']}")
            st.markdown(f"**Score: {comp_data['app1_score']}/100**")
            
            metrics1 = comp_data['app1_metrics']
            st.metric("Average Rating", f"{metrics1['avg_rating']}⭐")
            st.metric("Positive Reviews", f"{metrics1['positive_rate']}%")
            st.metric("Total Reviews", f"{metrics1['total_reviews']:,}")
        
        with col2:
            st.markdown('<div class="battle-vs">🏆</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"### 📱 {comp_data['app2_name']}")
            st.markdown(f"**Score: {comp_data['app2_score']}/100**")
            
            metrics2 = comp_data['app2_metrics']
            st.metric("Average Rating", f"{metrics2['avg_rating']}⭐")
            st.metric("Positive Reviews", f"{metrics2['positive_rate']}%")
            st.metric("Total Reviews", f"{metrics2['total_reviews']:,}")
        
        # Comparison charts
        st.markdown("### 📊 Detailed Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_ratings = go.Figure(data=[
                go.Bar(name=comp_data['app1_name'], x=['Rating'], y=[metrics1['avg_rating']], marker_color='#3B82F6'),
                go.Bar(name=comp_data['app2_name'], x=['Rating'], y=[metrics2['avg_rating']], marker_color='#EF4444')
            ])
            fig_ratings.update_layout(title="Rating Comparison", height=300)
            st.plotly_chart(fig_ratings, use_container_width=True)
        
        with col2:
            fig_sentiment = go.Figure(data=[
                go.Bar(name=comp_data['app1_name'], x=['Positive %'], y=[metrics1['positive_rate']], marker_color='#10B981'),
                go.Bar(name=comp_data['app2_name'], x=['Positive %'], y=[metrics2['positive_rate']], marker_color='#F59E0B')
            ])
            fig_sentiment.update_layout(title="Sentiment Comparison", height=300)
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Export comparison
        st.markdown("### 💾 Export Battle Report")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_data = json.dumps(comp_data, indent=2, default=str)
            st.download_button(
                "📊 Download Battle Report",
                report_data,
                f"{comp_data['app1_name']}_vs_{comp_data['app2_name']}_battle.json",
                "application/json",
                use_container_width=True
            )
        
        with col2:
            if st.button("🔄 New Battle", use_container_width=True):
                st.session_state.competitive_data = None
                st.rerun()

def notifications_page():
    """Notifications setup page"""
    st.markdown("## 🔔 Live Notification Center")
    st.write("Setup real-time notifications for analysis completion")
    
    st.info("🚧 Slack & Discord integration coming soon!")
    st.write("**Features will include:**")
    st.write("- Real-time analysis completion alerts")
    st.write("- Professional formatted messages")
    st.write("- Custom webhook integration")
    st.write("- Team collaboration features")

def settings_page():
    """Settings page"""
    user = st.session_state.user_data
    
    st.markdown("## ⚙️ Settings & Configuration")
    
    tab1, tab2 = st.tabs(["👤 Account", "🔧 System"])
    
    with tab1:
        st.markdown("#### Account Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Username", value=user['username'], disabled=True)
            st.text_input("Role", value=user['role'].title(), disabled=True)
        
        with col2:
            st.text_input("Email", value=user['email'], disabled=True)
            premium_status = "Active" if user.get('premium_access') else "Standard"
            st.text_input("Account Type", value=premium_status, disabled=True)
        
        st.markdown("#### Usage Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            playstore_analyses = 1 if st.session_state.analyzed_data is not None else 0
            st.metric("Play Store Analyses", playstore_analyses)
        
        with col2:
            competitive_count = user.get('competitive_analysis_count', 0)
            st.metric("Competitive Analyses", competitive_count)
        
        with col3:
            total_reviews = len(st.session_state.analyzed_data) if st.session_state.analyzed_data is not None else 0
            st.metric("Total Reviews Analyzed", f"{total_reviews:,}")
    
    with tab2:
        st.markdown("#### System Information")
        
        system_info = {
            "Application": "ReviewForge Analytics Pro",
            "Version": "2.0.0 Professional Edition",
            "Platform": "Streamlit Application",
            "Database": "SQLite Professional",
            "Current Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Session": "Active" if st.session_state.session_token else "Inactive"
        }
        
        for key, value in system_info.items():
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"**{key}:**")
            with col2:
                st.markdown(value)

# MAIN APPLICATION
def main():
    """Main application controller"""
    try:
        # Authentication check
        if st.session_state.current_page == 'login' or not check_authentication():
            show_login()
            return
        
        # Create UI components
        create_header()
        create_navigation()
        create_sidebar()
        
        # Route to pages
        if st.session_state.current_page == 'dashboard':
            dashboard_page()
        elif st.session_state.current_page == 'playstore':
            playstore_analysis_page()
        elif st.session_state.current_page == 'competitive':
            competitive_analysis_page()
        elif st.session_state.current_page == 'notifications':
            notifications_page()
        elif st.session_state.current_page == 'settings':
            settings_page()
        else:
            st.session_state.current_page = 'dashboard'
            st.rerun()
        
    except Exception as e:
        st.error(f"⚠️ Application error: {str(e)}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🏠 Return to Dashboard", use_container_width=True):
                st.session_state.current_page = 'dashboard'
                st.rerun()
        
        with col2:
            if st.button("🚪 Logout", use_container_width=True):
                logout_user()

if __name__ == "__main__":
    main()
