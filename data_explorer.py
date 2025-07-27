#!/usr/bin/env python3
"""
FitTrackAI Data Explorer

This tool helps you explore and understand your Apple Health data.
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

class DataExplorer:
    """Explore and analyze Apple Health data."""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def get_database_overview(self):
        """Get a comprehensive overview of the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            
            overview = {
                "total_tables": len(tables),
                "tables": []
            }
            
            for table in tables:
                # Get record count
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                record_count = cursor.fetchone()[0]
                
                # Get column info
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [row[1] for row in cursor.fetchall()]
                
                # Get date range if date column exists
                date_range = None
                if 'date' in columns:
                    cursor.execute(f"SELECT MIN(date), MAX(date) FROM {table}")
                    min_date, max_date = cursor.fetchone()
                    if min_date and max_date:
                        date_range = f"{min_date} to {max_date}"
                
                # Get sample data
                cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                sample_data = cursor.fetchall()
                
                table_info = {
                    "name": table,
                    "record_count": record_count,
                    "columns": columns,
                    "date_range": date_range,
                    "sample_data": sample_data
                }
                
                overview["tables"].append(table_info)
            
            conn.close()
            return overview
            
        except Exception as e:
            print(f"Error getting database overview: {e}")
            return None
    
    def analyze_table(self, table_name: str):
        """Analyze a specific table in detail."""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get all data
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
            conn.close()
            
            if df.empty:
                return f"No data found in table {table_name}"
            
            analysis = {
                "table_name": table_name,
                "total_records": len(df),
                "columns": list(df.columns),
                "data_types": df.dtypes.to_dict(),
                "missing_values": df.isnull().sum().to_dict()
            }
            
            # Date analysis
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                analysis["date_range"] = {
                    "start": df['date'].min().strftime('%Y-%m-%d'),
                    "end": df['date'].max().strftime('%Y-%m-%d'),
                    "total_days": (df['date'].max() - df['date'].min()).days
                }
            
            # Numeric column analysis
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if 'date' in numeric_cols:
                numeric_cols.remove('date')
            
            analysis["numeric_analysis"] = {}
            for col in numeric_cols:
                col_data = df[col].dropna()
                if len(col_data) > 0:
                    analysis["numeric_analysis"][col] = {
                        "mean": float(col_data.mean()),
                        "median": float(col_data.median()),
                        "min": float(col_data.min()),
                        "max": float(col_data.max()),
                        "std": float(col_data.std()),
                        "count": int(len(col_data))
                    }
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing table {table_name}: {e}"
    
    def get_health_insights(self):
        """Get health insights from the data."""
        try:
            insights = []
            
            # Steps analysis
            try:
                df_steps = pd.read_sql_query("SELECT * FROM DailyStepCount", sqlite3.connect(self.db_path))
                if not df_steps.empty:
                    avg_steps = df_steps['total_value'].mean()
                    max_steps = df_steps['total_value'].max()
                    min_steps = df_steps['total_value'].min()
                    
                    insights.append({
                        "metric": "Steps",
                        "average": f"{avg_steps:.0f} steps/day",
                        "best_day": f"{max_steps:.0f} steps",
                        "worst_day": f"{min_steps:.0f} steps",
                        "assessment": "Good" if avg_steps >= 7500 else "Needs improvement"
                    })
            except:
                pass
            
            # Sleep analysis
            try:
                df_sleep = pd.read_sql_query("SELECT * FROM DailySleepSummary", sqlite3.connect(self.db_path))
                if not df_sleep.empty:
                    avg_sleep_hours = df_sleep['sleep_minutes'].mean() / 60
                    
                    insights.append({
                        "metric": "Sleep",
                        "average": f"{avg_sleep_hours:.1f} hours/night",
                        "assessment": "Good" if avg_sleep_hours >= 7 else "Needs improvement"
                    })
            except:
                pass
            
            # Calories analysis
            try:
                df_calories = pd.read_sql_query("SELECT * FROM DailyActiveCalories", sqlite3.connect(self.db_path))
                if not df_calories.empty:
                    avg_calories = df_calories['total_value'].mean()
                    
                    insights.append({
                        "metric": "Active Calories",
                        "average": f"{avg_calories:.0f} calories/day",
                        "assessment": "Good" if avg_calories >= 300 else "Needs improvement"
                    })
            except:
                pass
            
            return insights
            
        except Exception as e:
            return f"Error getting health insights: {e}"
    
    def generate_report(self):
        """Generate a comprehensive data report."""
        print("🔍 FitTrackAI Data Explorer")
        print("=" * 50)
        
        # Database overview
        overview = self.get_database_overview()
        if overview:
            print(f"\n📊 Database Overview:")
            print(f"Total tables: {overview['total_tables']}")
            
            for table in overview['tables']:
                print(f"\n📋 {table['name']}:")
                print(f"  Records: {table['record_count']}")
                print(f"  Columns: {', '.join(table['columns'])}")
                if table['date_range']:
                    print(f"  Date range: {table['date_range']}")
        
        # Health insights
        print(f"\n💡 Health Insights:")
        insights = self.get_health_insights()
        if isinstance(insights, list):
            for insight in insights:
                print(f"\n{insight['metric']}:")
                print(f"  Average: {insight['average']}")
                if 'best_day' in insight:
                    print(f"  Best day: {insight['best_day']}")
                print(f"  Assessment: {insight['assessment']}")
        else:
            print(insights)
        
        print(f"\n🎯 Recommendations:")
        print("- Use the web interface to explore visualizations")
        print("- Ask the AI about specific metrics")
        print("- Request trend analysis for insights")

def main():
    """Main function to run the data explorer."""
    db_path = "data/db/processed_apple_health_data.db"
    
    try:
        explorer = DataExplorer(db_path)
        explorer.generate_report()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the database file exists at:", db_path)

if __name__ == "__main__":
    main() 