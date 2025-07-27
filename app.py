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
import logging
from typing import Dict, Any, Optional, List
import requests
from PIL import Image
import io
import base64

# LLM imports - Ollama required
try:
    from langchain_ollama import ChatOllama
    from langchain.schema import HumanMessage, SystemMessage
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    print("❌ Ollama libraries not available. Please install: pip install langchain-ollama")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Database path
DB_PATH = "data/db/processed_apple_health_data.db"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Manages database operations and data retrieval."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except Exception as e:
            logger.error(f"Error getting tables: {e}")
            return []
    
    def get_table_data(self, table_name: str, limit: int = 100) -> pd.DataFrame:
        """Get data from a specific table."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"SELECT * FROM {table_name} LIMIT {limit}"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Error getting data from {table_name}: {e}")
            return pd.DataFrame()
    
    def get_all_table_data(self, table_name: str) -> pd.DataFrame:
        """Get all data from a specific table."""
        try:
            conn = sqlite3.connect(self.db_path)
            query = f"SELECT * FROM {table_name}"
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            logger.error(f"Error getting all data from {table_name}: {e}")
            return pd.DataFrame()
    
    def get_database_summary(self) -> Dict[str, Any]:
        """Get a summary of the database contents."""
        try:
            tables = self.get_tables()
            summary = {
                "total_tables": len(tables),
                "tables": []
            }
            
            for table in tables:
                df = self.get_table_data(table, limit=1)
                summary["tables"].append({
                    "name": table,
                    "record_count": len(self.get_all_table_data(table)),
                    "columns": list(df.columns) if not df.empty else []
                })
            
            return summary
        except Exception as e:
            logger.error(f"Error getting database summary: {e}")
            return {"total_tables": 0, "tables": []}

class PlotGenerator:
    """Generates interactive plots using Plotly."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def generate_plot(self, plot_type: str, table_name: str = None, **kwargs) -> Dict[str, Any]:
        """Generate a plot based on the specified type."""
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
            elif plot_type == "custom" and table_name:
                return self._custom_plot(table_name, **kwargs)
            else:
                return {"error": f"Unknown plot type: {plot_type}"}
        except Exception as e:
            logger.error(f"Error generating plot {plot_type}: {e}")
            return {"error": f"Error generating plot: {str(e)}"}
    
    def _daily_steps_plot(self) -> Dict[str, Any]:
        """Generate daily steps plot with moving average."""
        df = self.data_manager.get_all_table_data("DailyStepCount")
        if df.empty:
            return {"error": "No step data available"}
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calculate 7-day moving average
        df['moving_avg'] = df['total_value'].rolling(window=7, min_periods=1).mean()
        
        fig = go.Figure()
        
        # Add step count line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['total_value'],
            mode='lines+markers',
            name='Daily Steps',
            line=dict(color='#6366f1', width=2),
            marker=dict(size=6, color='#6366f1')
        ))
        
        # Add moving average line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['moving_avg'],
            mode='lines',
            name='7-Day Moving Average',
            line=dict(color='#ef4444', width=3, dash='dash')
        ))
        
        fig.update_layout(
            title="Daily Step Count with Moving Average",
            xaxis_title="Date",
            yaxis_title="Steps",
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "daily_steps",
            "title": "Daily Step Count"
        }
    
    def _sleep_analysis_plot(self) -> Dict[str, Any]:
        """Generate sleep analysis plot."""
        df = self.data_manager.get_all_table_data("DailySleepSummary")
        if df.empty:
            return {"error": "No sleep data available"}
        
        df['date'] = pd.to_datetime(df['date'])
        df['sleep_hours'] = df['sleep_minutes'] / 60
        
        # Categorize sleep quality
        def categorize_sleep(hours):
            if hours >= 8: return 'Excellent'
            elif hours >= 7: return 'Good'
            elif hours >= 6: return 'Fair'
            else: return 'Poor'
        
        df['quality'] = df['sleep_hours'].apply(categorize_sleep)
        colors = {'Excellent': '#10b981', 'Good': '#3b82f6', 'Fair': '#f59e0b', 'Poor': '#ef4444'}
        
        fig = go.Figure()
        
        for quality in ['Excellent', 'Good', 'Fair', 'Poor']:
            quality_data = df[df['quality'] == quality]
            if not quality_data.empty:
                fig.add_trace(go.Bar(
                    x=quality_data['date'],
                    y=quality_data['sleep_hours'],
                    name=quality,
                    marker_color=colors[quality],
                    opacity=0.8
                ))
        
        fig.update_layout(
            title="Sleep Duration Analysis",
            xaxis_title="Date",
            yaxis_title="Sleep Hours",
            barmode='stack',
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "sleep_analysis",
            "title": "Sleep Analysis"
        }
    
    def _calories_plot(self) -> Dict[str, Any]:
        """Generate calories plot with active and basal calories."""
        active_df = self.data_manager.get_all_table_data("DailyActiveCalories")
        basal_df = self.data_manager.get_all_table_data("DailyBasalCalories")
        
        if active_df.empty and basal_df.empty:
            return {"error": "No calorie data available"}
        
        fig = go.Figure()
        
        if not active_df.empty:
            active_df['date'] = pd.to_datetime(active_df['date'])
            fig.add_trace(go.Scatter(
                x=active_df['date'],
                y=active_df['total_value'],
                mode='lines+markers',
                name='Active Calories',
                line=dict(color='#f97316', width=2),
                marker=dict(size=6)
            ))
        
        if not basal_df.empty:
            basal_df['date'] = pd.to_datetime(basal_df['date'])
            fig.add_trace(go.Scatter(
                x=basal_df['date'],
                y=basal_df['total_value'],
                mode='lines+markers',
                name='Basal Calories',
                line=dict(color='#8b5cf6', width=2),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title="Daily Calorie Burn",
            xaxis_title="Date",
            yaxis_title="Calories",
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "calories_burned",
            "title": "Daily Calorie Burn"
        }
    
    def _distance_plot(self) -> Dict[str, Any]:
        """Generate distance walked/run plot."""
        df = self.data_manager.get_all_table_data("DailyDistanceWalkRun")
        if df.empty:
            return {"error": "No distance data available"}
        
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['total_value'],
            mode='lines+markers',
            name='Distance',
            line=dict(color='#06b6d4', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title="Daily Distance Walked/Run",
            xaxis_title="Date",
            yaxis_title="Distance (km)",
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "distance_walked",
            "title": "Daily Distance"
        }
    
    def _flights_plot(self) -> Dict[str, Any]:
        """Generate flights climbed plot."""
        df = self.data_manager.get_all_table_data("DailyFlightsClimbed")
        if df.empty:
            return {"error": "No flights data available"}
        
        df['date'] = pd.to_datetime(df['date'])
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df['date'],
            y=df['total_value'],
            name='Flights Climbed',
            marker_color='#84cc16',
            opacity=0.8
        ))
        
        fig.update_layout(
            title="Daily Flights Climbed",
            xaxis_title="Date",
            yaxis_title="Flights",
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "flights_climbed",
            "title": "Daily Flights Climbed"
        }
    
    def _walking_metrics_plot(self) -> Dict[str, Any]:
        """Generate walking metrics plot."""
        speed_df = self.data_manager.get_all_table_data("DailyWalkingSpeed")
        steadiness_df = self.data_manager.get_all_table_data("DailyWalkingSteadiness")
        
        fig = go.Figure()
        
        if not speed_df.empty:
            speed_df['date'] = pd.to_datetime(speed_df['date'])
            fig.add_trace(go.Scatter(
                x=speed_df['date'],
                y=speed_df['avg_value'],
                mode='lines+markers',
                name='Walking Speed',
                line=dict(color='#ec4899', width=2),
                yaxis='y'
            ))
        
        if not steadiness_df.empty:
            steadiness_df['date'] = pd.to_datetime(steadiness_df['date'])
            fig.add_trace(go.Scatter(
                x=steadiness_df['date'],
                y=steadiness_df['avg_value'],
                mode='lines+markers',
                name='Walking Steadiness',
                line=dict(color='#f59e0b', width=2),
                yaxis='y2'
            ))
        
        fig.update_layout(
            title="Walking Metrics",
            xaxis_title="Date",
            yaxis=dict(title="Speed (m/s)", side="left"),
            yaxis2=dict(title="Steadiness (%)", side="right", overlaying="y"),
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "walking_metrics",
            "title": "Walking Metrics"
        }
    
    def _custom_plot(self, table_name: str, **kwargs) -> Dict[str, Any]:
        """Generate a custom plot for any table."""
        df = self.data_manager.get_all_table_data(table_name)
        if df.empty:
            return {"error": f"No data available for table: {table_name}"}
        
        df['date'] = pd.to_datetime(df['date'])
        
        # Find numeric columns for plotting
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if 'date' in numeric_cols:
            numeric_cols.remove('date')
        
        if not numeric_cols:
            return {"error": f"No numeric columns found in {table_name}"}
        
        fig = go.Figure()
        
        for col in numeric_cols:
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df[col],
                mode='lines+markers',
                name=col.replace('_', ' ').title(),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title=f"{table_name.replace('_', ' ').title()}",
            xaxis_title="Date",
            yaxis_title="Value",
            template='plotly_white',
            height=500
        )
        
        return {
            "plot": json.dumps(fig, cls=PlotlyJSONEncoder),
            "type": "custom",
            "title": table_name.replace('_', ' ').title()
        }

class AdvancedAI:
    """AI system powered by Ollama LLM with deep data understanding."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
        self.ollama_client = None
        self._initialize_ollama()
    
    def _initialize_ollama(self):
        """Initialize Ollama client - required for AI functionality."""
        if not OLLAMA_AVAILABLE:
            raise RuntimeError("❌ Ollama libraries not available. Please install: pip install langchain-ollama")
        
        try:
            # Try to connect to Ollama
            self.ollama_client = ChatOllama(
                model="llama2",
                base_url="http://localhost:11434"
            )
            
            # Test the connection
            test_response = self.ollama_client.invoke([
                HumanMessage(content="Hello, are you working?")
            ])
            
            logger.info("✅ Ollama initialized successfully")
            logger.info(f"🤖 Using model: llama2")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Ollama: {e}")
            logger.error("💡 Make sure Ollama is installed and running:")
            logger.error("   1. Install Ollama: https://ollama.ai/download")
            logger.error("   2. Start Ollama: ollama serve")
            logger.error("   3. Download model: ollama pull llama2")
            raise RuntimeError(f"Ollama initialization failed: {e}")
    
    def _get_detailed_data_context(self) -> str:
        """Get comprehensive data context for intelligent responses."""
        try:
            tables = self.data_manager.get_tables()
            context = f"📊 Database Overview:\n"
            context += f"Total tables: {len(tables)}\n\n"
            
            for table in tables:
                df = self.data_manager.get_all_table_data(table)
                if not df.empty:
                    record_count = len(df)
                    columns = list(df.columns)
                    
                    # Get date range if date column exists
                    date_range = ""
                    if 'date' in columns:
                        df['date'] = pd.to_datetime(df['date'])
                        min_date = df['date'].min().strftime('%Y-%m-%d')
                        max_date = df['date'].max().strftime('%Y-%m-%d')
                        date_range = f" ({min_date} to {max_date})"
                    
                    # Get statistical insights for numeric columns
                    insights = self._analyze_table_data(df, table)
                    
                    context += f"📋 {table}:\n"
                    context += f"  • Records: {record_count}{date_range}\n"
                    context += f"  • Columns: {', '.join(columns)}\n"
                    if insights:
                        context += f"  • Insights: {insights}\n"
                    context += "\n"
            
            return context
        except Exception as e:
            logger.error(f"Error getting data context: {e}")
            return "Database information unavailable"
    
    def _analyze_table_data(self, df: pd.DataFrame, table_name: str) -> str:
        """Analyze table data and return insights."""
        try:
            insights = []
            
            # Get numeric columns (excluding date)
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'date' in numeric_cols:
                numeric_cols.remove('date')
            
            for col in numeric_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    avg_val = col_data.mean()
                    max_val = col_data.max()
                    min_val = col_data.min()
                    
                    # Format based on column type
                    if 'step' in col.lower():
                        insights.append(f"Avg {col}: {avg_val:.0f} steps (max: {max_val:.0f})")
                    elif 'sleep' in col.lower():
                        hours = avg_val / 60 if avg_val > 60 else avg_val
                        max_hours = max_val / 60 if max_val > 60 else max_val
                        insights.append(f"Avg {col}: {hours:.1f} hours (max: {max_hours:.1f}h)")
                    elif 'calorie' in col.lower():
                        insights.append(f"Avg {col}: {avg_val:.0f} calories (max: {max_val:.0f})")
                    elif 'distance' in col.lower():
                        insights.append(f"Avg {col}: {avg_val:.2f} km (max: {max_val:.2f}km)")
                    else:
                        insights.append(f"Avg {col}: {avg_val:.1f} (max: {max_val:.1f})")
            
            return "; ".join(insights) if insights else ""
        except Exception as e:
            logger.error(f"Error analyzing table data: {e}")
            return ""
    
    def _generate_llm_response(self, message: str, context: str = "") -> str:
        """Generate response using Ollama LLM."""
        if not self.ollama_client:
            raise RuntimeError("Ollama client not initialized")
        
        try:
            system_prompt = f"""You are FitTrackAI, an AI health data assistant. You help users understand their Apple Health data through natural conversation.

{context}

You can:
- Analyze health trends and patterns
- Provide insights about steps, sleep, calories, distance, etc.
- Generate visualizations and plots
- Give personalized health recommendations
- Answer questions about fitness and wellness
- Provide detailed analysis of actual data in the database

Be friendly, helpful, and use emojis to make responses engaging. Keep responses concise but informative. Use the actual data insights provided to give accurate, personalized responses.

Always respond in a conversational, helpful manner. If asked about data that's not available, politely explain what data is available instead."""

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=message)
            ]
            
            response = self.ollama_client.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            raise RuntimeError(f"Failed to generate response: {e}")
    
    def chat(self, message: str) -> Dict[str, Any]:
        """Main chat method - uses Ollama LLM."""
        try:
            # Check for plot requests first
            plot_result = self._handle_plot_request(message)
            if plot_result:
                # Generate LLM response for the plot
                context = self._get_detailed_data_context()
                llm_response = self._generate_llm_response(
                    f"Generate a response for showing {message} visualization",
                    context
                )
                
                return {
                    "response": llm_response,
                    "plot": plot_result,
                    "provider": "OLLAMA"
                }
            
            # Generate text response using Ollama
            context = self._get_detailed_data_context()
            response = self._generate_llm_response(message, context)
            
            return {
                "response": response,
                "provider": "OLLAMA"
            }
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return {
                "response": f"Sorry, I encountered an error: {str(e)}. Please make sure Ollama is running.",
                "provider": "ERROR"
            }
    
    def _handle_plot_request(self, message: str) -> Optional[Dict[str, Any]]:
        """Handle plot generation requests."""
        message_lower = message.lower()
        
        try:
            plot_generator = PlotGenerator(self.data_manager)
            
            if any(word in message_lower for word in ["step", "steps"]):
                return plot_generator.generate_plot("daily_steps")
            
            elif any(word in message_lower for word in ["sleep", "sleeping"]):
                return plot_generator.generate_plot("sleep_analysis")
            
            elif any(word in message_lower for word in ["calorie", "calories"]):
                return plot_generator.generate_plot("calories_burned")
            
            elif any(word in message_lower for word in ["distance", "walk", "run"]):
                return plot_generator.generate_plot("distance_walked")
            
            elif any(word in message_lower for word in ["flight", "stairs"]):
                return plot_generator.generate_plot("flights_climbed")
            
            elif any(word in message_lower for word in ["walking", "speed", "steadiness"]):
                return plot_generator.generate_plot("walking_metrics")
            
            return None
            
        except Exception as e:
            logger.error(f"Error generating plot: {e}")
            return None

# Initialize components
data_manager = DataManager(DB_PATH)
plot_generator = PlotGenerator(data_manager)

# Initialize AI system (Ollama required)
try:
    ai_system = AdvancedAI(data_manager)
    logger.info("✅ AI system initialized with Ollama")
except Exception as e:
    logger.error(f"❌ Failed to initialize AI system: {e}")
    logger.error("💡 Please ensure Ollama is installed and running:")
    logger.error("   1. Install Ollama: https://ollama.ai/download")
    logger.error("   2. Start Ollama: ollama serve")
    logger.error("   3. Download model: ollama pull llama2")
    ai_system = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        message = data['message']
        response = ai_system.chat(message)
        
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/plot', methods=['POST'])
def generate_plot():
    try:
        data = request.get_json()
        if not data or 'type' not in data:
            return jsonify({"error": "No plot type provided"}), 400
        
        plot_type = data['type']
        table_name = data.get('table_name')
        
        result = ai_system.plot_generator.generate_plot(plot_type, table_name)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in plot endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/data_summary')
def data_summary():
    try:
        summary = data_manager.get_database_summary()
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error in data summary endpoint: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/llm_status')
def llm_status():
    """Get status of available LLM providers."""
    status = {
        "available_providers": ["ollama"] if OLLAMA_AVAILABLE else [],
        "current_provider": "ollama" if OLLAMA_AVAILABLE else "none",
        "ollama_available": OLLAMA_AVAILABLE,
        "ollama_required": True
    }
    return jsonify(status)

@socketio.on('connect')
def handle_connect():
    emit('status', {'message': 'Connected to FitTrackAI!'})

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle incoming chat messages."""
    try:
        message = data.get('message', '')
        
        if not ai_system:
            emit('chat_response', {
                'response': "❌ AI system is not available. Please ensure Ollama is installed and running:\n\n1. Install Ollama: https://ollama.ai/download\n2. Start Ollama: ollama serve\n3. Download model: ollama pull llama2",
                'provider': 'ERROR'
            })
            return
        
        # Get AI response
        response = ai_system.chat(message)
        
        # Emit response back to client
        emit('chat_response', response)
        
    except Exception as e:
        logger.error(f"Error handling chat message: {e}")
        emit('chat_response', {
            'response': f"Sorry, I encountered an error: {str(e)}. Please make sure Ollama is running.",
            'provider': 'ERROR'
        })

if __name__ == '__main__':
    print("🚀 Starting FitTrackAI...")
    print(f"📊 Using database: {DB_PATH}")
    print("🌐 Server running at: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 