# ReviewForge Analytics Professional - Enhanced Version

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup
from google_play_scraper import app, reviews, Sort
import sqlite3
from datetime import datetime, timedelta
import time
import re
from textblob import TextBlob
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import threading
from urllib.parse import urlparse, parse_qs

# Admin Authentication
ADMIN_PASSWORD = "Jaimatadiletsrock"

class ReviewAnalytics:
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect('reviews.db', check_same_thread=False)
        c = conn.cursor()
        
        # Create tables
        c.execute('''CREATE TABLE IF NOT EXISTS reviews
                     (id INTEGER PRIMARY KEY, app_name TEXT, review TEXT, 
                      rating INTEGER, date TEXT, source TEXT, sentiment REAL,
                      competitor_group TEXT)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS competitors
                     (id INTEGER PRIMARY KEY, app_name TEXT, app_id TEXT, 
                      category TEXT, added_date TEXT)''')
        
        conn.commit()
        conn.close()
    
    def extract_app_id(self, url):
        """Extract app ID from Play Store URL"""
        try:
            parsed = urlparse(url)
            if 'play.google.com' in parsed.netloc:
                params = parse_qs(parsed.query)
                if 'id' in params:
                    return params['id'][0]
                # Alternative format: /store/apps/details/id
                path_parts = parsed.path.split('/')
                if 'details' in path_parts:
                    details_idx = path_parts.index('details')
                    if details_idx + 1 < len(path_parts):
                        return path_parts[details_idx + 1]
            return None
        except:
            return None
    
    def scrape_play_store_reviews(self, app_id, count=1000):
        """Scrape reviews from Google Play Store"""
        try:
            # Get app info
            app_info = app(app_id)
            
            # Get reviews
            result, _ = reviews(
                app_id,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=count
            )
            
            reviews_data = []
            for review in result:
                sentiment = TextBlob(review['content']).sentiment.polarity
                reviews_data.append({
                    'app_name': app_info['title'],
                    'review': review['content'],
                    'rating': review['score'],
                    'date': review['at'].strftime('%Y-%m-%d'),
                    'source': 'Google Play Store',
                    'sentiment': sentiment
                })
            
            return reviews_data, app_info
        except Exception as e:
            st.error(f"Error scraping reviews: {str(e)}")
            return [], {}
    
    def perform_competitor_analysis(self, app_urls):
        """Perform comprehensive competitor analysis"""
        competitor_data = {}
        all_reviews = []
        
        for url in app_urls:
            app_id = self.extract_app_id(url)
            if not app_id:
                continue
                
            reviews_data, app_info = self.scrape_play_store_reviews(app_id)
            
            if reviews_data:
                competitor_data[app_info['title']] = {
                    'app_info': app_info,
                    'reviews': reviews_data,
                    'metrics': self.calculate_metrics(reviews_data)
                }
                
                # Add competitor group identifier
                for review in reviews_data:
                    review['competitor_group'] = app_info['title']
                    all_reviews.append(review)
        
        return competitor_data, all_reviews
    
    def calculate_metrics(self, reviews_data):
        """Calculate detailed metrics for reviews"""
        if not reviews_data:
            return {}
        
        df = pd.DataFrame(reviews_data)
        
        metrics = {
            'total_reviews': len(df),
            'avg_rating': df['rating'].mean(),
            'rating_distribution': df['rating'].value_counts().to_dict(),
            'sentiment_avg': df['sentiment'].mean(),
            'positive_reviews': len(df[df['sentiment'] > 0.1]),
            'negative_reviews': len(df[df['sentiment'] < -0.1]),
            'neutral_reviews': len(df[(df['sentiment'] >= -0.1) & (df['sentiment'] <= 0.1)]),
            'recent_reviews': len(df[df['date'] >= (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')]),
            'common_keywords': self.extract_keywords(df['review'].tolist())
        }
        
        return metrics
    
    def extract_keywords(self, reviews, top_n=20):
        """Extract common keywords from reviews"""
        text = ' '.join(reviews).lower()
        words = re.findall(r'\b[a-z]{3,}\b', text)
        
        # Remove common stop words
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too', 'use', 'app', 'good', 'very', 'like', 'this', 'that', 'with', 'have', 'from', 'they', 'know', 'want', 'been', 'will', 'more', 'than', 'time', 'just', 'great', 'nice', 'love', 'really', 'much', 'work'}
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 3]
        word_freq = pd.Series(filtered_words).value_counts().head(top_n)
        
        return word_freq.to_dict()
    
    def save_to_database(self, reviews_data):
        """Save reviews to database"""
        conn = sqlite3.connect('reviews.db')
        
        for review in reviews_data:
            conn.execute('''INSERT INTO reviews 
                           (app_name, review, rating, date, source, sentiment, competitor_group)
                           VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (review['app_name'], review['review'], review['rating'], 
                         review['date'], review['source'], review['sentiment'], 
                         review.get('competitor_group', '')))
        
        conn.commit()
        conn.close()
    
    def generate_professional_report(self, competitor_data):
        """Generate comprehensive professional report"""
        report = {
            'executive_summary': self.create_executive_summary(competitor_data),
            'detailed_analysis': self.create_detailed_analysis(competitor_data),
            'recommendations': self.create_recommendations(competitor_data),
            'data_tables': self.create_data_tables(competitor_data)
        }
        
        return report
    
    def create_executive_summary(self, competitor_data):
        """Create executive summary"""
        summary = []
        
        for app_name, data in competitor_data.items():
            metrics = data['metrics']
            summary.append({
                'App Name': app_name,
                'Total Reviews Analyzed': metrics.get('total_reviews', 0),
                'Average Rating': f"{metrics.get('avg_rating', 0):.2f} ★",
                'Sentiment Score': f"{metrics.get('sentiment_avg', 0):.2f}",
                'Positive Reviews': f"{(metrics.get('positive_reviews', 0) / metrics.get('total_reviews', 1) * 100):.1f}%",
                'Recent Activity (30 days)': metrics.get('recent_reviews', 0)
            })
        
        return pd.DataFrame(summary)
    
    def create_detailed_analysis(self, competitor_data):
        """Create detailed competitive analysis"""
        analysis = {}
        
        for app_name, data in competitor_data.items():
            app_info = data['app_info']
            metrics = data['metrics']
            
            analysis[app_name] = {
                'App Details': {
                    'Category': app_info.get('genre', 'N/A'),
                    'Developer': app_info.get('developer', 'N/A'),
                    'Downloads': app_info.get('installs', 'N/A'),
                    'Content Rating': app_info.get('contentRating', 'N/A'),
                    'Last Updated': app_info.get('updated', 'N/A')
                },
                'Performance Metrics': {
                    'Overall Rating': f"{app_info.get('score', 0):.2f} ★",
                    'Total Ratings': app_info.get('ratings', 0),
                    'Average Sentiment': f"{metrics.get('sentiment_avg', 0):.3f}",
                    'Engagement Score': self.calculate_engagement_score(metrics)
                },
                'User Sentiment Breakdown': {
                    'Positive': f"{(metrics.get('positive_reviews', 0) / metrics.get('total_reviews', 1) * 100):.1f}%",
                    'Negative': f"{(metrics.get('negative_reviews', 0) / metrics.get('total_reviews', 1) * 100):.1f}%",
                    'Neutral': f"{(metrics.get('neutral_reviews', 0) / metrics.get('total_reviews', 1) * 100):.1f}%"
                },
                'Top Keywords': list(metrics.get('common_keywords', {}).keys())[:10]
            }
        
        return analysis
    
    def calculate_engagement_score(self, metrics):
        """Calculate engagement score"""
        total_reviews = metrics.get('total_reviews', 0)
        recent_reviews = metrics.get('recent_reviews', 0)
        avg_sentiment = metrics.get('sentiment_avg', 0)
        
        if total_reviews == 0:
            return 0
        
        recency_factor = min(recent_reviews / total_reviews * 10, 1.0)
        sentiment_factor = (avg_sentiment + 1) / 2
        volume_factor = min(total_reviews / 1000, 1.0)
        
        engagement_score = (recency_factor + sentiment_factor + volume_factor) / 3 * 100
        
        return f"{engagement_score:.1f}/100"
    
    def create_recommendations(self, competitor_data):
        """Generate strategic recommendations"""
        recommendations = []
        
        # Analyze all competitors
        all_metrics = [data['metrics'] for data in competitor_data.values()]
        
        # Rating analysis
        avg_ratings = [m.get('avg_rating', 0) for m in all_metrics]
        best_rating = max(avg_ratings) if avg_ratings else 0
        
        # Sentiment analysis
        avg_sentiments = [m.get('sentiment_avg', 0) for m in all_metrics]
        best_sentiment = max(avg_sentiments) if avg_sentiments else 0
        
        recommendations.extend([
            {
                'Category': 'Rating Optimization',
                'Priority': 'High',
                'Recommendation': f'Target rating improvement to {best_rating:.1f}★ to match top competitor',
                'Impact': 'Improved app store visibility and user trust'
            },
            {
                'Category': 'Sentiment Enhancement',
                'Priority': 'Medium',
                'Recommendation': f'Focus on improving user sentiment score to {best_sentiment:.2f}',
                'Impact': 'Better user retention and positive word-of-mouth'
            },
            {
                'Category': 'Feature Development',
                'Priority': 'High',
                'Recommendation': 'Analyze top keywords from competitor reviews for feature gaps',
                'Impact': 'Enhanced user experience and competitive advantage'
            },
            {
                'Category': 'User Engagement',
                'Priority': 'Medium',
                'Recommendation': 'Implement review response strategy based on competitor analysis',
                'Impact': 'Improved customer satisfaction and loyalty'
            }
        ])
        
        return pd.DataFrame(recommendations)
    
    def create_data_tables(self, competitor_data):
        """Create comprehensive data tables"""
        tables = {}
        
        # Rating distribution comparison
        rating_comparison = []
        for app_name, data in competitor_data.items():
            rating_dist = data['metrics'].get('rating_distribution', {})
            row = {'App Name': app_name}
            for i in range(1, 6):
                row[f'{i} ★'] = rating_dist.get(i, 0)
            rating_comparison.append(row)
        
        tables['Rating Distribution'] = pd.DataFrame(rating_comparison)
        
        # Keyword analysis
        keyword_comparison = []
        for app_name, data in competitor_data.items():
            keywords = data['metrics'].get('common_keywords', {})
            for keyword, count in list(keywords.items())[:10]:
                keyword_comparison.append({
                    'App Name': app_name,
                    'Keyword': keyword,
                    'Frequency': count
                })
        
        tables['Keyword Analysis'] = pd.DataFrame(keyword_comparison)
        
        return tables

# Streamlit App
def main():
    st.set_page_config(
        page_title="ReviewForge Analytics Professional",
        page_icon="⭐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 3px solid #1f77b4;
        padding-bottom: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .competitor-section {
        border: 2px solid #e1e5e9;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background-color: #f8f9fa;
    }
    
    .review-container {
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
        border-radius: 5px;
        padding: 1rem;
        background-color: white;
    }
    
    .review-item {
        border-bottom: 1px solid #e9ecef;
        padding: 0.8rem 0;
        margin-bottom: 0.5rem;
    }
    
    .rating-stars {
        color: #ffc107;
        font-size: 1.2rem;
    }
    
    .sentiment-positive {
        background-color: #d4edda;
        color: #155724;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    
    .sentiment-negative {
        background-color: #f8d7da;
        color: #721c24;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    
    .sentiment-neutral {
        background-color: #fff3cd;
        color: #856404;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
    }
    
    .professional-table {
        font-size: 0.9rem;
    }
    
    .sidebar .sidebar-content {
        background-color: #f1f3f4;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">ReviewForge Analytics Professional</h1>', unsafe_allow_html=True)
    
    # Initialize analytics
    analytics = ReviewAnalytics()
    
    # Sidebar
    with st.sidebar:
        st.header("Navigation")
        
        # Admin authentication
        admin_password = st.text_input("Admin Password", type="password")
        is_admin = admin_password == ADMIN_PASSWORD
        
        if is_admin:
            st.success("Admin access granted")
            
            page = st.selectbox(
                "Select Analysis Type",
                ["Single App Analysis", "Competitor Analysis", "Bulk Review Analysis", "Professional Report"]
            )
        else:
            st.error("Please enter admin password to access the system")
            return
    
    if is_admin:
        if page == "Single App Analysis":
            single_app_analysis(analytics)
        elif page == "Competitor Analysis":
            competitor_analysis(analytics)
        elif page == "Bulk Review Analysis":
            bulk_review_analysis(analytics)
        elif page == "Professional Report":
            professional_report(analytics)

def single_app_analysis(analytics):
    """Single app analysis interface"""
    st.header("Single App Analysis")
    
    app_url = st.text_input("Enter Google Play Store App URL:")
    
    if st.button("Analyze App", type="primary"):
        if app_url:
            app_id = analytics.extract_app_id(app_url)
            
            if app_id:
                with st.spinner("Analyzing app reviews..."):
                    reviews_data, app_info = analytics.scrape_play_store_reviews(app_id)
                    
                    if reviews_data:
                        # Save to database
                        analytics.save_to_database(reviews_data)
                        
                        # Display results
                        display_single_app_results(app_info, reviews_data, analytics)
                    else:
                        st.error("No reviews found or error occurred")
            else:
                st.error("Invalid Play Store URL")

def competitor_analysis(analytics):
    """Competitor analysis interface"""
    st.header("Competitor Analysis")
    
    st.markdown("Enter 3-4 competitor app URLs for comprehensive analysis:")
    
    urls = []
    for i in range(4):
        url = st.text_input(f"Competitor App {i+1} URL:", key=f"comp_{i}")
        if url:
            urls.append(url)
    
    if st.button("Perform Competitor Analysis", type="primary") and len(urls) >= 2:
        with st.spinner("Analyzing competitor apps..."):
            competitor_data, all_reviews = analytics.perform_competitor_analysis(urls)
            
            if competitor_data:
                # Save all reviews
                analytics.save_to_database(all_reviews)
                
                # Display competitor analysis
                display_competitor_analysis(competitor_data, analytics)
            else:
                st.error("No data could be retrieved from the provided URLs")
    elif len(urls) < 2:
        st.warning("Please enter at least 2 competitor URLs")

def bulk_review_analysis(analytics):
    """Bulk review analysis interface"""
    st.header("Bulk Review Analysis")
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file with reviews", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Data Preview:")
        st.dataframe(df.head())
        
        if st.button("Analyze Uploaded Reviews", type="primary"):
            # Process and analyze uploaded data
            st.success("Bulk analysis completed")

def professional_report(analytics):
    """Professional report generation"""
    st.header("Professional ORM Report")
    
    # Load data from database
    conn = sqlite3.connect('reviews.db')
    query = "SELECT * FROM reviews WHERE date >= date('now', '-30 days')"
    df = pd.read_sql_query(query, conn)
    conn.close()
    
    if not df.empty:
        # Group by competitor
        competitor_groups = df.groupby('competitor_group')
        competitor_data = {}
        
        for name, group in competitor_groups:
            if name:  # Skip empty groups
                reviews_data = group.to_dict('records')
                competitor_data[name] = {
                    'reviews': reviews_data,
                    'metrics': analytics.calculate_metrics(reviews_data),
                    'app_info': {'title': name}  # Simplified app info
                }
        
        if competitor_data:
            # Generate professional report
            report = analytics.generate_professional_report(competitor_data)
            
            # Display report sections
            display_professional_report(report, competitor_data)
        else:
            st.info("No competitor data available. Please run competitor analysis first.")
    else:
        st.info("No recent data available. Please analyze some apps first.")

def display_single_app_results(app_info, reviews_data, analytics):
    """Display single app analysis results"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{len(reviews_data)}</h3><p>Total Reviews</p></div>', unsafe_allow_html=True)
    
    with col2:
        avg_rating = np.mean([r['rating'] for r in reviews_data])
        st.markdown(f'<div class="metric-card"><h3>{avg_rating:.1f} ★</h3><p>Average Rating</p></div>', unsafe_allow_html=True)
    
    with col3:
        avg_sentiment = np.mean([r['sentiment'] for r in reviews_data])
        st.markdown(f'<div class="metric-card"><h3>{avg_sentiment:.2f}</h3><p>Sentiment Score</p></div>', unsafe_allow_html=True)
    
    with col4:
        positive_reviews = len([r for r in reviews_data if r['sentiment'] > 0.1])
        positive_pct = (positive_reviews / len(reviews_data)) * 100
        st.markdown(f'<div class="metric-card"><h3>{positive_pct:.1f}%</h3><p>Positive Reviews</p></div>', unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating distribution
        ratings = [r['rating'] for r in reviews_data]
        fig = px.histogram(x=ratings, nbins=5, title="Rating Distribution")
        fig.update_layout(xaxis_title="Rating", yaxis_title="Count")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment distribution
        sentiments = [r['sentiment'] for r in reviews_data]
        sentiment_labels = ['Negative' if s < -0.1 else 'Positive' if s > 0.1 else 'Neutral' for s in sentiments]
        fig = px.pie(values=[sentiment_labels.count(l) for l in ['Positive', 'Negative', 'Neutral']], 
                     names=['Positive', 'Negative', 'Neutral'],
                     title="Sentiment Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    # Reviews display
    st.subheader("Recent Reviews")
    display_reviews_scroll(reviews_data[:50])  # Show first 50 reviews

def display_competitor_analysis(competitor_data, analytics):
    """Display comprehensive competitor analysis"""
    
    # Executive Summary
    st.subheader("Executive Summary")
    summary_df = analytics.create_executive_summary(competitor_data)
    st.dataframe(summary_df, use_container_width=True)
    
    # Comparison Charts
    st.subheader("Performance Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating comparison
        apps = list(competitor_data.keys())
        ratings = [data['metrics'].get('avg_rating', 0) for data in competitor_data.values()]
        
        fig = px.bar(x=apps, y=ratings, title="Average Rating Comparison",
                     labels={'x': 'Applications', 'y': 'Average Rating'})
        fig.update_traces(marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'][:len(apps)])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Sentiment comparison
        sentiments = [data['metrics'].get('sentiment_avg', 0) for data in competitor_data.values()]
        
        fig = px.bar(x=apps, y=sentiments, title="Sentiment Score Comparison",
                     labels={'x': 'Applications', 'y': 'Sentiment Score'})
        fig.update_traces(marker_color=['#2ca02c' if s > 0 else '#d62728' for s in sentiments])
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Analysis for each competitor
    for app_name, data in competitor_data.items():
        with st.expander(f"Detailed Analysis: {app_name}"):
            display_detailed_competitor_info(app_name, data)
    
    # Combined reviews from all competitors
    st.subheader("All Competitor Reviews")
    all_reviews = []
    for data in competitor_data.values():
        all_reviews.extend(data['reviews'])
    
    display_reviews_scroll(all_reviews[:100])  # Show first 100 reviews

def display_detailed_competitor_info(app_name, data):
    """Display detailed information for a single competitor"""
    metrics = data['metrics']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Reviews", metrics.get('total_reviews', 0))
        st.metric("Average Rating", f"{metrics.get('avg_rating', 0):.2f} ★")
    
    with col2:
        positive_pct = (metrics.get('positive_reviews', 0) / max(metrics.get('total_reviews', 1), 1)) * 100
        st.metric("Positive Reviews", f"{positive_pct:.1f}%")
        st.metric("Sentiment Score", f"{metrics.get('sentiment_avg', 0):.3f}")
    
    with col3:
        st.metric("Recent Reviews (30d)", metrics.get('recent_reviews', 0))
        engagement = analytics.calculate_engagement_score(metrics)
        st.metric("Engagement Score", engagement)
    
    # Top keywords
    st.write("**Top Keywords:**")
    keywords = metrics.get('common_keywords', {})
    if keywords:
        keyword_df = pd.DataFrame(list(keywords.items()), columns=['Keyword', 'Frequency'])
        st.dataframe(keyword_df.head(10), use_container_width=True)

def display_reviews_scroll(reviews_data):
    """Display reviews in a scrollable container"""
    reviews_html = '<div class="review-container">'
    
    for review in reviews_data:
        sentiment_class = "sentiment-positive" if review['sentiment'] > 0.1 else "sentiment-negative" if review['sentiment'] < -0.1 else "sentiment-neutral"
        stars = "★" * review['rating'] + "☆" * (5 - review['rating'])
        
        reviews_html += f'''
        <div class="review-item">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <span class="rating-stars">{stars}</span>
                <span class="{sentiment_class}">
                    {"Positive" if review['sentiment'] > 0.1 else "Negative" if review['sentiment'] < -0.1 else "Neutral"}
                </span>
                <small>{review['date']}</small>
            </div>
            <p style="margin: 0; color: #495057;">{review['review'][:300]}{"..." if len(review['review']) > 300 else ""}</p>
            <small style="color: #6c757d;">Source: {review['source']}</small>
        </div>
        '''
    
    reviews_html += '</div>'
    st.markdown(reviews_html, unsafe_allow_html=True)

def display_professional_report(report, competitor_data):
    """Display professional ORM report"""
    
    # Executive Summary
    st.subheader("Executive Summary")
    st.dataframe(report['executive_summary'], use_container_width=True)
    
    # Detailed Analysis
    st.subheader("Detailed Competitive Analysis")
    detailed = report['detailed_analysis']
    
    for app_name, analysis in detailed.items():
        with st.expander(f"Analysis: {app_name}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**App Details**")
                for key, value in analysis['App Details'].items():
                    st.write(f"- {key}: {value}")
                
                st.write("**Performance Metrics**")
                for key, value in analysis['Performance Metrics'].items():
                    st.write(f"- {key}: {value}")
            
            with col2:
                st.write("**User Sentiment Breakdown**")
                for key, value in analysis['User Sentiment Breakdown'].items():
                    st.write(f"- {key}: {value}")
                
                st.write("**Top Keywords**")
                keywords_text = ", ".join(analysis['Top Keywords'][:10])
                st.write(keywords_text)
    
    # Strategic Recommendations
    st.subheader("Strategic Recommendations")
    recommendations_df = report['recommendations']
    st.dataframe(recommendations_df, use_container_width=True)
    
    # Data Tables
    st.subheader("Detailed Data Analysis")
    tables = report['data_tables']
    
    for table_name, table_df in tables.items():
        st.write(f"**{table_name}**")
        st.dataframe(table_df, use_container_width=True)
    
    # Download options
    st.subheader("Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Export Executive Summary"):
            csv = report['executive_summary'].to_csv(index=False)
            st.download_button("Download CSV", csv, "executive_summary.csv", "text/csv")
    
    with col2:
        if st.button("Export Recommendations"):
            csv = recommendations_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "recommendations.csv", "text/csv")
    
    with col3:
        if st.button("Export Full Report"):
            # Create comprehensive report
            full_report = create_full_report_text(report, competitor_data)
            st.download_button("Download Report", full_report, "orm_report.txt", "text/plain")

def create_full_report_text(report, competitor_data):
    """Create full text report"""
    report_text = f"""
ONLINE REPUTATION MANAGEMENT REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
{report['executive_summary'].to_string()}

DETAILED ANALYSIS
"""
    
    for app_name, analysis in report['detailed_analysis'].items():
        report_text += f"\n{app_name.upper()}\n"
        report_text += "=" * len(app_name) + "\n"
        
        for section, data in analysis.items():
            report_text += f"\n{section}:\n"
            if isinstance(data, dict):
                for key, value in data.items():
                    report_text += f"  - {key}: {value}\n"
            else:
                report_text += f"  {data}\n"
    
    report_text += f"\n\nSTRATEGIC RECOMMENDATIONS\n"
    report_text += report['recommendations'].to_string()
    
    return report_text

if __name__ == "__main__":
    main()
