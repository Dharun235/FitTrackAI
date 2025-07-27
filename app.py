"""
FitTrackAI - Clean Chat & Plot Platform

A streamlined web application for chatting with health data and generating plots.
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import json
import os
from datetime import datetime, timedelta
import random
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Database path
DB_PATH = "data/db/processed_apple_health_data.db"

class DataManager:
    """Manages database operations and data retrieval."""
    
    def __init__(self, db_path):
        self.db_path = db_path
    
    def get_tables(self):
        """Get list of available tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            print(f"Error getting tables: {e}")
            return []
    
    def get_table_data(self, table_name, limit=100):
        """Get data from a specific table."""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT {limit}", conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error getting data from {table_name}: {e}")
            return pd.DataFrame()
    
    def get_all_table_data(self, table_name):
        """Get all data from a specific table."""
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error getting all data from {table_name}: {e}")
            return pd.DataFrame()
    
    def get_database_summary(self):
        """Get summary of database contents."""
        tables = self.get_tables()
        summary = {
            "total_tables": len(tables),
            "tables": []
        }
        
        for table in tables:
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                
                # Get column info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [row[1] for row in cursor.fetchall()]
                
                conn.close()
                
                summary["tables"].append({
                    "name": table,
                    "record_count": count,
                    "columns": columns
                })
            except Exception as e:
                print(f"Error getting info for {table}: {e}")
        
        return summary

class PlotGenerator:
    """Generates interactive plots from health data."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def generate_plot(self, plot_type, table_name=None, **kwargs):
        """Generate a plot based on type and parameters."""
        try:
            if plot_type == "daily_steps":
                return self._daily_steps_plot()
            elif plot_type == "sleep_analysis":
                return self._sleep_analysis_plot()
            elif plot_type == "calories_burned":
                return self._calories_plot()
            elif plot_type == "distance_walked":
                return self._distance_plot()
            elif plot_type == "flights_climbed":
                return self._flights_plot()
            elif plot_type == "walking_metrics":
                return self._walking_metrics_plot()
            elif plot_type == "custom":
                return self._custom_plot(table_name, **kwargs)
            else:
                return {"error": f"Unknown plot type: {plot_type}"}
        except Exception as e:
            return {"error": f"Error generating plot: {str(e)}"}
    
    def _daily_steps_plot(self):
        """Generate daily steps plot."""
        df = self.data_manager.get_all_table_data("DailyStepCount")
        if df.empty:
            return {"error": "No step data available"}
        
        # Add moving average
        df['moving_avg'] = df['total_value'].rolling(window=7).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_value'], 
                                mode='lines+markers', name='Daily Steps',
                                line=dict(color='#667eea', width=2)))
        fig.add_trace(go.Scatter(x=df['date'], y=df['moving_avg'], 
                                mode='lines', name='7-Day Average',
                                line=dict(color='#764ba2', width=3, dash='dash')))
        
        fig.update_layout(
            title='Daily Step Count with 7-Day Moving Average',
            xaxis_title='Date',
            yaxis_title='Steps',
            height=400,
            hovermode='x unified'
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "daily_steps",
            "title": "Daily Step Count"
        }
    
    def _sleep_analysis_plot(self):
        """Generate sleep analysis plot."""
        df = self.data_manager.get_all_table_data("DailySleepSummary")
        if df.empty:
            return {"error": "No sleep data available"}
        
        # Convert minutes to hours
        df['sleep_hours'] = df['sleep_minutes'] / 60
        
        # Add sleep quality indicators
        df['sleep_quality'] = df['sleep_hours'].apply(
            lambda x: 'Excellent' if x >= 8 else 'Good' if x >= 7 else 'Fair' if x >= 6 else 'Poor'
        )
        
        fig = px.bar(df, x='date', y='sleep_hours', color='sleep_quality',
                    title='Daily Sleep Duration with Quality Indicators',
                    labels={'sleep_hours': 'Hours', 'date': 'Date', 'sleep_quality': 'Quality'},
                    color_discrete_map={
                        'Excellent': '#28a745',
                        'Good': '#17a2b8', 
                        'Fair': '#ffc107',
                        'Poor': '#dc3545'
                    })
        fig.update_layout(height=400)
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "sleep_analysis",
            "title": "Daily Sleep Duration"
        }
    
    def _calories_plot(self):
        """Generate calories burned plot."""
        active_df = self.data_manager.get_all_table_data("DailyActiveCalories")
        basal_df = self.data_manager.get_all_table_data("DailyBasalCalories")
        
        if active_df.empty and basal_df.empty:
            return {"error": "No calorie data available"}
        
        fig = go.Figure()
        
        if not active_df.empty:
            fig.add_trace(go.Scatter(x=active_df['date'], y=active_df['total_value'],
                                   mode='lines+markers', name='Active Calories',
                                   line=dict(color='#ff6b6b', width=2)))
        
        if not basal_df.empty:
            fig.add_trace(go.Scatter(x=basal_df['date'], y=basal_df['total_value'],
                                   mode='lines+markers', name='Basal Calories',
                                   line=dict(color='#4ecdc4', width=2)))
        
        if not active_df.empty and not basal_df.empty:
            # Combine for total calories
            combined_df = pd.merge(active_df, basal_df, on='date', suffixes=('_active', '_basal'))
            combined_df['total_calories'] = combined_df['total_value_active'] + combined_df['total_value_basal']
            fig.add_trace(go.Scatter(x=combined_df['date'], y=combined_df['total_calories'],
                                   mode='lines+markers', name='Total Calories',
                                   line=dict(color='#45b7d1', width=3)))
        
        fig.update_layout(
            title='Daily Calories Burned',
            xaxis_title='Date',
            yaxis_title='Calories',
            height=400,
            hovermode='x unified'
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "calories_burned",
            "title": "Daily Calories Burned"
        }
    
    def _distance_plot(self):
        """Generate distance walked/run plot."""
        df = self.data_manager.get_all_table_data("DailyDistanceWalkRun")
        if df.empty:
            return {"error": "No distance data available"}
        
        # Add weekly total
        df['week'] = pd.to_datetime(df['date']).dt.isocalendar().week
        weekly_totals = df.groupby('week')['total_value'].sum().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['total_value'],
                               mode='lines+markers', name='Daily Distance',
                               line=dict(color='#667eea', width=2)))
        
        fig.update_layout(
            title='Daily Distance Walked/Run',
            xaxis_title='Date',
            yaxis_title='Distance (km)',
            height=400,
            hovermode='x unified'
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "distance_walked",
            "title": "Daily Distance Walked/Run"
        }
    
    def _flights_plot(self):
        """Generate flights climbed plot."""
        df = self.data_manager.get_all_table_data("DailyFlightsClimbed")
        if df.empty:
            return {"error": "No flights data available"}
        
        fig = px.bar(df, x='date', y='total_value',
                    title='Daily Flights Climbed',
                    labels={'total_value': 'Flights', 'date': 'Date'},
                    color='total_value',
                    color_continuous_scale='viridis')
        fig.update_layout(height=400)
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "flights_climbed",
            "title": "Daily Flights Climbed"
        }
    
    def _walking_metrics_plot(self):
        """Generate walking metrics plot."""
        speed_df = self.data_manager.get_all_table_data("DailyWalkingSpeed")
        steadiness_df = self.data_manager.get_all_table_data("DailyWalkingSteadiness")
        
        if speed_df.empty and steadiness_df.empty:
            return {"error": "No walking metrics data available"}
        
        fig = go.Figure()
        
        if not speed_df.empty:
            fig.add_trace(go.Scatter(x=speed_df['date'], y=speed_df['avg_value'],
                                   mode='lines+markers', name='Walking Speed',
                                   line=dict(color='#667eea', width=2),
                                   yaxis='y'))
        
        if not steadiness_df.empty:
            fig.add_trace(go.Scatter(x=steadiness_df['date'], y=steadiness_df['avg_value'],
                                   mode='lines+markers', name='Walking Steadiness',
                                   line=dict(color='#764ba2', width=2),
                                   yaxis='y2'))
        
        fig.update_layout(
            title='Walking Metrics Over Time',
            xaxis_title='Date',
            yaxis=dict(title='Walking Speed', side='left'),
            yaxis2=dict(title='Walking Steadiness', side='right', overlaying='y'),
            height=400,
            hovermode='x unified'
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "walking_metrics",
            "title": "Walking Metrics"
        }
    
    def _custom_plot(self, table_name, **kwargs):
        """Generate custom plot from any table."""
        df = self.data_manager.get_all_table_data(table_name)
        if df.empty:
            return {"error": f"No data available for table: {table_name}"}
        
        # Determine plot type based on data
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        date_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
        
        if len(numeric_cols) == 0:
            return {"error": "No numeric columns found for plotting"}
        
        # Default to first numeric column
        y_col = kwargs.get('y', numeric_cols[0])
        x_col = kwargs.get('x', df.columns[0])
        
        # Determine plot type
        if len(numeric_cols) >= 2:
            # Scatter plot for multiple numeric columns
            fig = px.scatter(df, x=x_col, y=y_col,
                           title=f'{table_name} - {y_col} vs {x_col}',
                           labels={y_col: y_col, x_col: x_col})
        else:
            # Line plot for time series or single numeric column
            fig = px.line(df, x=x_col, y=y_col,
                         title=f'{table_name} - {y_col} over {x_col}',
                         labels={y_col: y_col, x_col: x_col})
        
        fig.update_layout(height=400)
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "custom",
            "title": f"{table_name} - {y_col} over {x_col}"
        }

class SimpleAI:
    """Enhanced AI chat system with data analysis capabilities."""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.plot_generator = PlotGenerator(data_manager)
    
    def chat(self, message):
        """Process chat message and return response."""
        message_lower = message.lower()
        
        # Check for plot requests
        if any(word in message_lower for word in ['plot', 'chart', 'graph', 'visualize', 'show']):
            return self._handle_plot_request(message)
        
        # Check for data analysis requests
        if any(word in message_lower for word in ['analyze', 'analysis', 'insights', 'trends', 'patterns']):
            return self._handle_analysis_request(message)
        
        # Check for data questions
        if any(word in message_lower for word in ['data', 'table', 'summary', 'info', 'what']):
            return self._handle_data_request(message)
        
        # Check for specific metrics
        if any(word in message_lower for word in ['steps', 'sleep', 'calories', 'distance', 'flights']):
            return self._handle_metric_question(message)
        
        # General health insights
        if any(word in message_lower for word in ['health', 'fitness', 'activity', 'performance']):
            return self._handle_health_question(message)
        
        # Custom plot requests
        if any(word in message_lower for word in ['custom', 'specific', 'particular']):
            return self._handle_custom_plot_request(message)
        
        # Default response
        return {
            "response": "Hey! I'm your health data assistant! 🤖 I can help you with:\n\n" +
                       "📊 **Data Analysis**: Ask me about trends, patterns, and insights\n" +
                       "📈 **Visualizations**: Request charts for steps, sleep, calories, distance, flights\n" +
                       "🔍 **Custom Plots**: Ask for specific data combinations\n" +
                       "📋 **Data Summary**: Get overview of your health metrics\n\n" +
                       "Try asking: 'Show me my step trends' or 'Analyze my sleep patterns' or 'Create a custom plot of walking speed'",
            "type": "text"
        }
    
    def _handle_plot_request(self, message):
        """Handle requests for plots."""
        message_lower = message.lower()
        
        if 'step' in message_lower:
            plot_data = self.plot_generator.generate_plot("daily_steps")
            response_text = "Here's your step data visualization! 🚶‍♂️ I've included a 7-day moving average to show trends."
        elif 'sleep' in message_lower:
            plot_data = self.plot_generator.generate_plot("sleep_analysis")
            response_text = "Here's your sleep analysis! 😴 I've color-coded the bars by sleep quality."
        elif 'calorie' in message_lower:
            plot_data = self.plot_generator.generate_plot("calories_burned")
            response_text = "Here's your calorie burn breakdown! 🔥 Showing active vs basal calories."
        elif 'distance' in message_lower:
            plot_data = self.plot_generator.generate_plot("distance_walked")
            response_text = "Here's your distance tracking! 🏃‍♂️ Shows your daily walking/running distance."
        elif 'flight' in message_lower:
            plot_data = self.plot_generator.generate_plot("flights_climbed")
            response_text = "Here's your flights climbed data! 🏢 Color intensity shows activity level."
        elif 'walking' in message_lower or 'speed' in message_lower or 'steadiness' in message_lower:
            plot_data = self.plot_generator.generate_plot("walking_metrics")
            response_text = "Here's your walking metrics! 🚶‍♀️ Showing speed and steadiness over time."
        else:
            # Default to steps
            plot_data = self.plot_generator.generate_plot("daily_steps")
            response_text = "Here's your step data! 🚶‍♂️ I've included a 7-day moving average to show trends."
        
        if "error" in plot_data:
            return {
                "response": f"Sorry, I couldn't generate that plot: {plot_data['error']} 😕",
                "type": "text"
            }
        
        return {
            "response": response_text,
            "type": "plot",
            "plot_data": plot_data
        }
    
    def _handle_analysis_request(self, message):
        """Handle requests for data analysis."""
        message_lower = message.lower()
        
        if 'step' in message_lower:
            return self._analyze_steps()
        elif 'sleep' in message_lower:
            return self._analyze_sleep()
        elif 'calorie' in message_lower:
            return self._analyze_calories()
        elif 'distance' in message_lower:
            return self._analyze_distance()
        elif 'trend' in message_lower or 'pattern' in message_lower:
            return self._analyze_general_trends()
        else:
            return self._analyze_general_trends()
    
    def _analyze_steps(self):
        """Analyze step data and provide insights."""
        df = self.data_manager.get_all_table_data("DailyStepCount")
        if df.empty:
            return {"response": "No step data available for analysis.", "type": "text"}
        
        avg_steps = df['total_value'].mean()
        max_steps = df['total_value'].max()
        min_steps = df['total_value'].min()
        recent_avg = df.tail(7)['total_value'].mean()
        
        # Calculate trend
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        recent_trend = df.tail(7)['total_value'].mean() - df.head(7)['total_value'].mean()
        
        analysis = f"📊 **Step Analysis Report** 📊\n\n"
        analysis += f"🎯 **Your Stats:**\n"
        analysis += f"• Average daily steps: {avg_steps:.0f} steps\n"
        analysis += f"• Best day: {max_steps:.0f} steps\n"
        analysis += f"• Recent 7-day average: {recent_avg:.0f} steps\n\n"
        
        if recent_trend > 0:
            analysis += f"📈 **Trend**: You're trending upward! Your recent average is {recent_trend:.0f} steps higher than your early data.\n\n"
        elif recent_trend < 0:
            analysis += f"📉 **Trend**: Your step count has decreased by {abs(recent_trend):.0f} steps recently.\n\n"
        else:
            analysis += f"➡️ **Trend**: Your step count is stable.\n\n"
        
        analysis += f"💡 **Recommendations:**\n"
        if avg_steps < 5000:
            analysis += "• Try to increase your daily steps gradually\n"
        elif avg_steps < 10000:
            analysis += "• You're doing well! Aim for 10,000 steps for optimal health\n"
        else:
            analysis += "• Excellent! You're exceeding the recommended daily step goal\n"
        
        return {"response": analysis, "type": "text"}
    
    def _analyze_sleep(self):
        """Analyze sleep data and provide insights."""
        df = self.data_manager.get_all_table_data("DailySleepSummary")
        if df.empty:
            return {"response": "No sleep data available for analysis.", "type": "text"}
        
        df['sleep_hours'] = df['sleep_minutes'] / 60
        avg_sleep = df['sleep_hours'].mean()
        max_sleep = df['sleep_hours'].max()
        min_sleep = df['sleep_hours'].min()
        
        # Sleep quality distribution
        excellent = len(df[df['sleep_hours'] >= 8])
        good = len(df[(df['sleep_hours'] >= 7) & (df['sleep_hours'] < 8)])
        fair = len(df[(df['sleep_hours'] >= 6) & (df['sleep_hours'] < 7)])
        poor = len(df[df['sleep_hours'] < 6])
        
        analysis = f"😴 **Sleep Analysis Report** 😴\n\n"
        analysis += f"🌙 **Your Sleep Stats:**\n"
        analysis += f"• Average sleep: {avg_sleep:.1f} hours\n"
        analysis += f"• Longest sleep: {max_sleep:.1f} hours\n"
        analysis += f"• Shortest sleep: {min_sleep:.1f} hours\n\n"
        
        analysis += f"📊 **Sleep Quality Breakdown:**\n"
        analysis += f"• Excellent (8+ hours): {excellent} days\n"
        analysis += f"• Good (7-8 hours): {good} days\n"
        analysis += f"• Fair (6-7 hours): {fair} days\n"
        analysis += f"• Poor (<6 hours): {poor} days\n\n"
        
        analysis += f"💡 **Recommendations:**\n"
        if avg_sleep < 7:
            analysis += "• Try to get more sleep - aim for 7-9 hours per night\n"
        elif avg_sleep > 9:
            analysis += "• You're getting plenty of sleep! Consider if you need this much\n"
        else:
            analysis += "• Great sleep duration! Keep up the good habits\n"
        
        return {"response": analysis, "type": "text"}
    
    def _analyze_calories(self):
        """Analyze calorie data and provide insights."""
        active_df = self.data_manager.get_all_table_data("DailyActiveCalories")
        basal_df = self.data_manager.get_all_table_data("DailyBasalCalories")
        
        if active_df.empty and basal_df.empty:
            return {"response": "No calorie data available for analysis.", "type": "text"}
        
        analysis = f"🔥 **Calorie Analysis Report** 🔥\n\n"
        
        if not active_df.empty:
            avg_active = active_df['total_value'].mean()
            max_active = active_df['total_value'].max()
            analysis += f"💪 **Active Calories:**\n"
            analysis += f"• Average: {avg_active:.0f} calories\n"
            analysis += f"• Best day: {max_active:.0f} calories\n\n"
        
        if not basal_df.empty:
            avg_basal = basal_df['total_value'].mean()
            analysis += f"⚡ **Basal Calories:**\n"
            analysis += f"• Average: {avg_basal:.0f} calories\n\n"
        
        if not active_df.empty and not basal_df.empty:
            total_avg = avg_active + avg_basal
            analysis += f"📊 **Total Daily Calories:**\n"
            analysis += f"• Average: {total_avg:.0f} calories\n\n"
            
            analysis += f"💡 **Insights:**\n"
            if avg_active < 200:
                analysis += "• Consider increasing your physical activity\n"
            elif avg_active > 500:
                analysis += "• Great job staying active!\n"
            else:
                analysis += "• Good level of physical activity\n"
        
        return {"response": analysis, "type": "text"}
    
    def _analyze_distance(self):
        """Analyze distance data and provide insights."""
        df = self.data_manager.get_all_table_data("DailyDistanceWalkRun")
        if df.empty:
            return {"response": "No distance data available for analysis.", "type": "text"}
        
        avg_distance = df['total_value'].mean()
        max_distance = df['total_value'].max()
        total_distance = df['total_value'].sum()
        
        analysis = f"🏃‍♂️ **Distance Analysis Report** 🏃‍♂️\n\n"
        analysis += f"📏 **Your Stats:**\n"
        analysis += f"• Average daily distance: {avg_distance:.2f} km\n"
        analysis += f"• Longest day: {max_distance:.2f} km\n"
        analysis += f"• Total distance tracked: {total_distance:.1f} km\n\n"
        
        analysis += f"💡 **Recommendations:**\n"
        if avg_distance < 2:
            analysis += "• Try to walk more - aim for at least 2-3 km daily\n"
        elif avg_distance < 5:
            analysis += "• Good distance! Consider adding some running\n"
        else:
            analysis += "• Excellent distance! You're very active\n"
        
        return {"response": analysis, "type": "text"}
    
    def _analyze_general_trends(self):
        """Provide general trend analysis across all metrics."""
        analysis = f"📈 **General Health Trends Analysis** 📈\n\n"
        
        # Get data from multiple tables
        steps_df = self.data_manager.get_all_table_data("DailyStepCount")
        sleep_df = self.data_manager.get_all_table_data("DailySleepSummary")
        active_df = self.data_manager.get_all_table_data("DailyActiveCalories")
        
        if not steps_df.empty:
            recent_steps = steps_df.tail(7)['total_value'].mean()
            early_steps = steps_df.head(7)['total_value'].mean()
            steps_trend = "📈 improving" if recent_steps > early_steps else "📉 declining" if recent_steps < early_steps else "➡️ stable"
            analysis += f"🚶‍♂️ **Steps**: {steps_trend} ({recent_steps:.0f} vs {early_steps:.0f} avg)\n"
        
        if not sleep_df.empty:
            sleep_df['sleep_hours'] = sleep_df['sleep_minutes'] / 60
            recent_sleep = sleep_df.tail(7)['sleep_hours'].mean()
            early_sleep = sleep_df.head(7)['sleep_hours'].mean()
            sleep_trend = "📈 improving" if recent_sleep > early_sleep else "📉 declining" if recent_sleep < early_sleep else "➡️ stable"
            analysis += f"😴 **Sleep**: {sleep_trend} ({recent_sleep:.1f}h vs {early_sleep:.1f}h avg)\n"
        
        if not active_df.empty:
            recent_active = active_df.tail(7)['total_value'].mean()
            early_active = active_df.head(7)['total_value'].mean()
            active_trend = "📈 improving" if recent_active > early_active else "📉 declining" if recent_active < early_active else "➡️ stable"
            analysis += f"🔥 **Active Calories**: {active_trend} ({recent_active:.0f} vs {early_active:.0f} avg)\n"
        
        analysis += f"\n💡 **Overall Assessment:**\n"
        analysis += f"Your health data shows consistent tracking across multiple metrics. "
        analysis += f"Keep monitoring these trends to maintain or improve your fitness levels!"
        
        return {"response": analysis, "type": "text"}
    
    def _handle_data_request(self, message):
        """Handle requests for data information."""
        summary = self.data_manager.get_database_summary()
        
        response = f"📊 **Your Health Database Summary** 📊\n\n"
        response += f"📁 **Total Tables**: {summary['total_tables']}\n\n"
        
        for table in summary['tables']:
            response += f"📋 **{table['name']}**: {table['record_count']} records\n"
            response += f"   Columns: {', '.join(table['columns'][:3])}{'...' if len(table['columns']) > 3 else ''}\n\n"
        
        response += f"💡 **Available Data Types:**\n"
        response += f"• Steps, Distance, Calories (Active & Basal)\n"
        response += f"• Sleep Duration, Flights Climbed\n"
        response += f"• Walking Speed, Steadiness, Asymmetry\n\n"
        response += f"Ask me to analyze any of these metrics or create visualizations!"
        
        return {
            "response": response,
            "type": "text"
        }
    
    def _handle_metric_question(self, message):
        """Handle specific questions about metrics."""
        message_lower = message.lower()
        
        if 'step' in message_lower:
            return self._analyze_steps()
        elif 'sleep' in message_lower:
            return self._analyze_sleep()
        elif 'calorie' in message_lower:
            return self._analyze_calories()
        elif 'distance' in message_lower:
            return self._analyze_distance()
        else:
            return {
                "response": "I can help you with steps, sleep, calories, distance, flights, and walking metrics! What would you like to know?",
                "type": "text"
            }
    
    def _handle_health_question(self, message):
        """Handle general health questions."""
        responses = [
            "Based on your health data, I can see you're tracking multiple fitness metrics! Your data shows a comprehensive view of your daily activities. What specific aspect would you like to explore?",
            "Your health data reveals interesting patterns across steps, sleep, calories, and distance. I can help you understand these trends and identify areas for improvement!",
            "I have access to your Apple Health data with rich metrics including daily steps, sleep duration, calorie burn, and walking patterns. What would you like to analyze?",
            "Your fitness data is quite comprehensive! I can help you visualize trends, analyze patterns, and provide insights to optimize your health journey."
        ]
        
        return {
            "response": random.choice(responses),
            "type": "text"
        }
    
    def _handle_custom_plot_request(self, message):
        """Handle requests for custom plots."""
        # Extract table name from message
        tables = self.data_manager.get_tables()
        message_lower = message.lower()
        
        for table in tables:
            if table.lower().replace('daily', '').replace('_', ' ') in message_lower:
                plot_data = self.plot_generator.generate_plot("custom", table)
                if "error" not in plot_data:
                    return {
                        "response": f"Here's your custom plot for {table}! 📊",
                        "type": "plot",
                        "plot_data": plot_data
                    }
        
        return {
            "response": "I can create custom plots for any of your data tables! Try asking for specific metrics like 'Show me walking speed data' or 'Create a plot of my sleep patterns'",
            "type": "text"
        }

# Initialize components
data_manager = DataManager(DB_PATH)
ai_system = SimpleAI(data_manager)

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = ai_system.chat(message)
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': f'Error processing message: {str(e)}'}), 500

@app.route('/api/plot', methods=['POST'])
def generate_plot():
    """Generate a specific plot."""
    try:
        data = request.get_json()
        plot_type = data.get('type', 'daily_steps')
        
        plot_generator = PlotGenerator(data_manager)
        result = plot_generator.generate_plot(plot_type)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error generating plot: {str(e)}'}), 500

@app.route('/api/data_summary')
def data_summary():
    """Get database summary."""
    try:
        summary = data_manager.get_database_summary()
        return jsonify(summary)
    except Exception as e:
        return jsonify({'error': f'Error getting summary: {str(e)}'}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('status', {'message': 'Connected to FitTrackAI'})

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle real-time chat messages."""
    try:
        message = data.get('message', '')
        if message:
            response = ai_system.chat(message)
            emit('chat_response', response)
        else:
            emit('chat_response', {'error': 'No message provided'})
    except Exception as e:
        emit('chat_response', {'error': f'Error processing message: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Starting FitTrackAI...")
    print("📊 Using database:", DB_PATH)
    print("🌐 Server running at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 