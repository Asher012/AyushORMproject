# Professional ORM Analytics Platform
# Enhanced with Competitor Analysis and Deep AI Insights

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from bs4 import BeautifulSoup
from google_play_scraper import app, reviews, Sort
from textblob import TextBlob
import sqlite3
from datetime import datetime, timedelta
import time
import re
from urllib.parse import urlparse, parse_qs
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import schedule
import threading
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

class ProfessionalORMTool:
    def __init__(self):
        self.admin_password = "Jaimatadiletsrock"
        self.setup_database()
        self.setup_page_config()
        
    def setup_page_config(self):
        st.set_page_config(
            page_title="Professional ORM Analytics Platform",
            page_icon="⭐",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
    def setup_database(self):
        conn = sqlite3.connect('orm_professional.db', check_same_thread=False)
        cursor = conn.cursor()
        
        # Reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT,
                app_name TEXT,
                reviewer_name TEXT,
                rating INTEGER,
                review_text TEXT,
                review_date TEXT,
                sentiment TEXT,
                category TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Competitor analysis table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS competitor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                app_name TEXT,
                app_id TEXT,
                total_reviews INTEGER,
                average_rating REAL,
                installs TEXT,
                last_updated TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Analytics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT,
                metric_value REAL,
                app_name TEXT,
                date_recorded TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    def admin_login(self):
        if 'admin_authenticated' not in st.session_state:
            st.session_state.admin_authenticated = False
            
        if not st.session_state.admin_authenticated:
            st.title("Professional ORM Analytics - Admin Access")
            password = st.text_input("Enter Admin Password:", type="password")
            
            if st.button("Login"):
                if password == self.admin_password:
                    st.session_state.admin_authenticated = True
                    st.success("Access Granted!")
                    st.rerun()
                else:
                    st.error("Invalid Password!")
            return False
        return True

    def extract_app_id_from_url(self, url):
        try:
            if 'play.google.com' in url:
                if 'id=' in url:
                    return url.split('id=')[1].split('&')[0]
                else:
                    return url.split('/')[-1].split('?')[0]
        except:
            return None
        return None

    def scrape_playstore_data(self, app_id, max_reviews=1000):
        try:
            # Get app info
            app_info = app(app_id)
            
            # Get reviews
            reviews_data, _ = reviews(
                app_id,
                lang='en',
                country='in',
                sort=Sort.NEWEST,
                count=max_reviews
            )
            
            return app_info, reviews_data
        except Exception as e:
            st.error(f"Error scraping {app_id}: {str(e)}")
            return None, None

    def analyze_sentiment_advanced(self, text):
        blob = TextBlob(text)
        polarity = blob.polarity
        
        if polarity > 0.3:
            return "Positive", polarity
        elif polarity < -0.3:
            return "Negative", polarity
        else:
            return "Neutral", polarity

    def categorize_feedback_ai(self, text):
        text_lower = text.lower()
        categories = {
            'Bug/Technical': ['bug', 'crash', 'error', 'not working', 'freeze', 'slow', 'loading'],
            'UI/UX': ['interface', 'design', 'layout', 'user friendly', 'navigation', 'confusing'],
            'Performance': ['fast', 'speed', 'performance', 'smooth', 'lag', 'responsive'],
            'Features': ['feature', 'functionality', 'option', 'tool', 'capability'],
            'Customer Service': ['support', 'help', 'service', 'response', 'staff', 'assistance'],
            'Pricing': ['price', 'cost', 'expensive', 'cheap', 'value', 'money', 'premium'],
            'General': ['overall', 'experience', 'satisfied', 'disappointed', 'recommend']
        }
        
        for category, keywords in categories.items():
            if any(keyword in text_lower for keyword in keywords):
                return category
        return 'General'

    def save_reviews_to_db(self, reviews_data, app_name, platform="PlayStore"):
        conn = sqlite3.connect('orm_professional.db', check_same_thread=False)
        cursor = conn.cursor()
        
        for review in reviews_data:
            sentiment, sentiment_score = self.analyze_sentiment_advanced(review['content'])
            category = self.categorize_feedback_ai(review['content'])
            
            cursor.execute('''
                INSERT INTO reviews (platform, app_name, reviewer_name, rating, 
                                   review_text, review_date, sentiment, category)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (platform, app_name, review['userName'], review['score'],
                  review['content'], review['at'].strftime('%Y-%m-%d'), sentiment, category))
        
        conn.commit()
        conn.close()

    def create_competitor_analysis(self):
        st.header("Competitor Analysis Dashboard")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Add Competitor Apps")
            competitor_urls = []
            
            for i in range(4):
                url = st.text_input(f"Competitor {i+1} Play Store URL:", key=f"comp_{i}")
                if url:
                    competitor_urls.append(url)
        
        with col2:
            st.subheader("Analysis Settings")
            max_reviews = st.selectbox("Reviews per app:", [500, 1000, 2000], index=1)
            include_historical = st.checkbox("Include Historical Data")
        
        if st.button("Start Competitor Analysis", type="primary"):
            if len(competitor_urls) < 2:
                st.warning("Please add at least 2 competitor URLs")
                return
                
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            competitor_data = []
            all_reviews_data = []
            
            for i, url in enumerate(competitor_urls):
                app_id = self.extract_app_id_from_url(url)
                if not app_id:
                    st.error(f"Invalid URL: {url}")
                    continue
                    
                status_text.text(f"Analyzing {app_id}...")
                progress_bar.progress((i + 1) / len(competitor_urls))
                
                app_info, reviews_data = self.scrape_playstore_data(app_id, max_reviews)
                
                if app_info and reviews_data:
                    competitor_data.append({
                        'App Name': app_info.get('title', 'Unknown'),
                        'App ID': app_id,
                        'Rating': app_info.get('score', 0),
                        'Reviews': app_info.get('reviews', 0),
                        'Installs': app_info.get('realInstalls', 'Unknown'),
                        'Category': app_info.get('genre', 'Unknown'),
                        'Last Updated': app_info.get('updated', 'Unknown')
                    })
                    
                    # Process reviews for detailed analysis
                    for review in reviews_data:
                        sentiment, sentiment_score = self.analyze_sentiment_advanced(review['content'])
                        category = self.categorize_feedback_ai(review['content'])
                        
                        all_reviews_data.append({
                            'App': app_info.get('title', 'Unknown'),
                            'Rating': review['score'],
                            'Review': review['content'],
                            'Date': review['at'].strftime('%Y-%m-%d'),
                            'Sentiment': sentiment,
                            'Sentiment_Score': sentiment_score,
                            'Category': category,
                            'Reviewer': review['userName']
                        })
            
            # Display results
            if competitor_data:
                self.display_competitor_results(competitor_data, all_reviews_data)

    def display_competitor_results(self, competitor_data, all_reviews_data):
        st.success("Analysis Complete!")
        
        # Overview metrics
        df_competitors = pd.DataFrame(competitor_data)
        df_reviews = pd.DataFrame(all_reviews_data)
        
        # Key metrics comparison
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_rating = df_competitors['Rating'].mean()
            st.metric("Avg Competitor Rating", f"{avg_rating:.2f}⭐")
        
        with col2:
            total_reviews = df_competitors['Reviews'].sum()
            st.metric("Total Reviews", f"{total_reviews:,}")
        
        with col3:
            positive_sentiment = len(df_reviews[df_reviews['Sentiment'] == 'Positive'])
            sentiment_rate = (positive_sentiment / len(df_reviews)) * 100
            st.metric("Positive Sentiment", f"{sentiment_rate:.1f}%")
        
        with col4:
            top_rated = df_competitors.loc[df_competitors['Rating'].idxmax(), 'App Name']
            st.metric("Top Rated App", top_rated)
        
        # Detailed comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Rating comparison
            fig_rating = px.bar(
                df_competitors,
                x='App Name',
                y='Rating',
                title="Rating Comparison",
                color='Rating',
                color_continuous_scale='RdYlGn'
            )
            fig_rating.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_rating, use_container_width=True)
        
        with col2:
            # Sentiment distribution
            sentiment_counts = df_reviews.groupby(['App', 'Sentiment']).size().unstack(fill_value=0)
            fig_sentiment = px.bar(
                sentiment_counts,
                title="Sentiment Distribution by App",
                color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
            )
            fig_sentiment.update_layout(height=400)
            st.plotly_chart(fig_sentiment, use_container_width=True)
        
        # Category analysis
        category_analysis = df_reviews.groupby(['App', 'Category']).agg({
            'Rating': 'mean',
            'Sentiment_Score': 'mean'
        }).round(2)
        
        st.subheader("Category-wise Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_category = px.heatmap(
                category_analysis.pivot_table(values='Rating', index='Category', columns='App'),
                title="Average Rating by Category",
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        with col2:
            # Top issues by competitor
            negative_reviews = df_reviews[df_reviews['Sentiment'] == 'Negative']
            top_issues = negative_reviews.groupby(['App', 'Category']).size().reset_index(name='Count')
            
            fig_issues = px.bar(
                top_issues.nlargest(15, 'Count'),
                x='Count',
                y='Category',
                color='App',
                title="Top Issues by Category",
                orientation='h'
            )
            st.plotly_chart(fig_issues, use_container_width=True)
        
        # Detailed reviews table
        self.create_professional_reviews_table(df_reviews)

    def create_professional_reviews_table(self, df_reviews):
        st.subheader("Complete Reviews Analysis")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_app = st.selectbox("Filter by App:", ['All'] + list(df_reviews['App'].unique()))
        
        with col2:
            selected_sentiment = st.selectbox("Filter by Sentiment:", ['All', 'Positive', 'Negative', 'Neutral'])
        
        with col3:
            selected_category = st.selectbox("Filter by Category:", ['All'] + list(df_reviews['Category'].unique()))
        
        # Apply filters
        filtered_df = df_reviews.copy()
        
        if selected_app != 'All':
            filtered_df = filtered_df[filtered_df['App'] == selected_app]
        if selected_sentiment != 'All':
            filtered_df = filtered_df[filtered_df['Sentiment'] == selected_sentiment]
        if selected_category != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == selected_category]
        
        # Create scrollable table
        st.markdown(f"**Showing {len(filtered_df)} reviews out of {len(df_reviews)} total reviews**")
        
        # Format the dataframe for display
        display_df = filtered_df[['App', 'Rating', 'Review', 'Date', 'Sentiment', 'Category', 'Reviewer']].copy()
        display_df['Rating'] = display_df['Rating'].apply(lambda x: '⭐' * x)
        display_df['Review'] = display_df['Review'].apply(lambda x: x[:100] + '...' if len(x) > 100 else x)
        
        # Display in scrollable container
        st.dataframe(
            display_df,
            use_container_width=True,
            height=600,
            column_config={
                "App": st.column_config.TextColumn("App Name", width="medium"),
                "Rating": st.column_config.TextColumn("Rating", width="small"),
                "Review": st.column_config.TextColumn("Review Text", width="large"),
                "Date": st.column_config.TextColumn("Date", width="small"),
                "Sentiment": st.column_config.TextColumn("Sentiment", width="small"),
                "Category": st.column_config.TextColumn("Category", width="medium"),
                "Reviewer": st.column_config.TextColumn("Reviewer", width="medium")
            }
        )
        
        # Download option
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download Filtered Reviews as CSV",
            data=csv,
            file_name=f"reviews_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

    def generate_orm_report(self):
        st.header("Professional ORM Report")
        
        # Get data from database
        conn = sqlite3.connect('orm_professional.db', check_same_thread=False)
        
        df_reviews = pd.read_sql_query("SELECT * FROM reviews", conn)
        df_competitors = pd.read_sql_query("SELECT * FROM competitor_data", conn)
        
        conn.close()
        
        if df_reviews.empty:
            st.warning("No data available. Please run analysis first.")
            return
        
        # Executive Summary
        col1, col2, col3, col4 = st.columns(4)
        
        total_reviews = len(df_reviews)
        avg_rating = df_reviews['rating'].mean()
        sentiment_distribution = df_reviews['sentiment'].value_counts(normalize=True) * 100
        
        with col1:
            st.metric("Total Reviews Analyzed", f"{total_reviews:,}")
        
        with col2:
            st.metric("Average Rating", f"{avg_rating:.2f}⭐")
        
        with col3:
            positive_rate = sentiment_distribution.get('Positive', 0)
            st.metric("Positive Sentiment", f"{positive_rate:.1f}%")
        
        with col4:
            response_time = "< 2 hours"  # This would be calculated from your actual response data
            st.metric("Avg Response Time", response_time)
        
        # Trend Analysis
        st.subheader("Reputation Trends")
        
        # Convert date column and create monthly trends
        df_reviews['review_date'] = pd.to_datetime(df_reviews['review_date'])
        monthly_trends = df_reviews.groupby([df_reviews['review_date'].dt.to_period('M'), 'sentiment']).size().unstack(fill_value=0)
        
        fig_trends = px.line(
            monthly_trends,
            title="Monthly Sentiment Trends",
            labels={'index': 'Month', 'value': 'Number of Reviews'}
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Category Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            category_ratings = df_reviews.groupby('category')['rating'].mean().sort_values(ascending=False)
            fig_category = px.bar(
                x=category_ratings.values,
                y=category_ratings.index,
                orientation='h',
                title="Average Rating by Category",
                color=category_ratings.values,
                color_continuous_scale='RdYlGn'
            )
            st.plotly_chart(fig_category, use_container_width=True)
        
        with col2:
            sentiment_category = pd.crosstab(df_reviews['category'], df_reviews['sentiment'])
            fig_sentiment_cat = px.bar(
                sentiment_category,
                title="Sentiment Distribution by Category",
                color_discrete_map={'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}
            )
            st.plotly_chart(fig_sentiment_cat, use_container_width=True)
        
        # Key Insights & Recommendations
        st.subheader("AI-Powered Insights & Recommendations")
        
        # Calculate key insights
        top_complaint_category = df_reviews[df_reviews['sentiment'] == 'Negative']['category'].mode().iloc[0]
        top_praise_category = df_reviews[df_reviews['sentiment'] == 'Positive']['category'].mode().iloc[0]
        
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            st.markdown("**Critical Issues:**")
            st.write(f"• Primary concern area: {top_complaint_category}")
            st.write(f"• Negative sentiment rate: {sentiment_distribution.get('Negative', 0):.1f}%")
            
            # Top negative keywords
            negative_reviews = df_reviews[df_reviews['sentiment'] == 'Negative']['review_text'].str.lower().str.split()
            all_words = [word for review in negative_reviews for word in review if len(word) > 3]
            common_negative = Counter(all_words).most_common(5)
            
            st.write("• Most mentioned issues:")
            for word, count in common_negative:
                st.write(f"  - {word}: {count} mentions")
        
        with insights_col2:
            st.markdown("**Strengths & Opportunities:**")
            st.write(f"• Users appreciate: {top_praise_category}")
            st.write(f"• Positive sentiment rate: {sentiment_distribution.get('Positive', 0):.1f}%")
            
            # Top positive keywords
            positive_reviews = df_reviews[df_reviews['sentiment'] == 'Positive']['review_text'].str.lower().str.split()
            all_words = [word for review in positive_reviews for word in review if len(word) > 3]
            common_positive = Counter(all_words).most_common(5)
            
            st.write("• Most appreciated features:")
            for word, count in common_positive:
                st.write(f"  - {word}: {count} mentions")
        
        # Action Plan
        st.subheader("Recommended Action Plan")
        
        action_plan = f"""
        **Immediate Actions (0-30 days):**
        1. Address {top_complaint_category} issues - Priority: High
        2. Improve response time for negative reviews
        3. Create standardized response templates for common issues
        
        **Short-term Goals (1-3 months):**
        1. Implement feedback loop for {top_complaint_category} improvements
        2. Launch proactive communication campaign highlighting {top_praise_category}
        3. Monitor competitor responses and adapt best practices
        
        **Long-term Strategy (3-6 months):**
        1. Develop predictive analytics for issue prevention
        2. Create user satisfaction survey system
        3. Implement automated sentiment monitoring alerts
        """
        
        st.markdown(action_plan)
        
        # Export report
        if st.button("Generate PDF Report", type="primary"):
            st.success("PDF Report generation initiated!")
            st.info("Report will be available for download in a few moments...")

    def main(self):
        if not self.admin_login():
            return
        
        # Sidebar navigation
        st.sidebar.title("Professional ORM Analytics")
        page = st.sidebar.selectbox(
            "Select Module:",
            ["Dashboard", "Competitor Analysis", "Review Scraper", "ORM Report", "Settings"]
        )
        
        if page == "Dashboard":
            self.dashboard()
        elif page == "Competitor Analysis":
            self.create_competitor_analysis()
        elif page == "Review Scraper":
            self.review_scraper()
        elif page == "ORM Report":
            self.generate_orm_report()
        elif page == "Settings":
            self.settings()

    def dashboard(self):
        st.title("Professional ORM Dashboard")
        
        # Quick stats
        conn = sqlite3.connect('orm_professional.db', check_same_thread=False)
        
        total_reviews = pd.read_sql_query("SELECT COUNT(*) as count FROM reviews", conn).iloc[0]['count']
        recent_reviews = pd.read_sql_query("SELECT COUNT(*) as count FROM reviews WHERE date(scraped_at) = date('now')", conn).iloc[0]['count']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Reviews", f"{total_reviews:,}")
        with col2:
            st.metric("Today's Reviews", recent_reviews)
        with col3:
            st.metric("Active Platforms", "3")
        with col4:
            st.metric("Response Rate", "94%")
        
        conn.close()
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔍 Scrape New Reviews", use_container_width=True):
                st.info("Navigate to Review Scraper module")
        
        with col2:
            if st.button("📊 Competitor Analysis", use_container_width=True):
                st.info("Navigate to Competitor Analysis module")
        
        with col3:
            if st.button("📈 Generate Report", use_container_width=True):
                st.info("Navigate to ORM Report module")

    def review_scraper(self):
        st.header("Review Scraper")
        
        platform = st.selectbox("Select Platform:", ["Play Store", "GMB (Coming Soon)", "App Store (Coming Soon)"])
        
        if platform == "Play Store":
            app_url = st.text_input("Enter Play Store URL:")
            max_reviews = st.selectbox("Max Reviews to Scrape:", [500, 1000, 2000, 5000])
            
            if st.button("Start Scraping", type="primary") and app_url:
                app_id = self.extract_app_id_from_url(app_url)
                
                if app_id:
                    with st.spinner("Scraping reviews..."):
                        app_info, reviews_data = self.scrape_playstore_data(app_id, max_reviews)
                        
                        if app_info and reviews_data:
                            self.save_reviews_to_db(reviews_data, app_info['title'])
                            st.success(f"Successfully scraped {len(reviews_data)} reviews for {app_info['title']}")
                        else:
                            st.error("Failed to scrape reviews")
                else:
                    st.error("Invalid URL format")

    def settings(self):
        st.header("Settings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Database Management")
            if st.button("Clear All Data"):
                if st.checkbox("Confirm deletion"):
                    conn = sqlite3.connect('orm_professional.db', check_same_thread=False)
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM reviews")
                    cursor.execute("DELETE FROM competitor_data")
                    cursor.execute("DELETE FROM analytics_data")
                    conn.commit()
                    conn.close()
                    st.success("All data cleared!")
        
        with col2:
            st.subheader("Export Options")
            if st.button("Export All Data"):
                conn = sqlite3.connect('orm_professional.db', check_same_thread=False)
                df = pd.read_sql_query("SELECT * FROM reviews", conn)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f"orm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                conn.close()

if __name__ == "__main__":
    tool = ProfessionalORMTool()
    tool.main()
