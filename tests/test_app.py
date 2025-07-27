"""
Tests for FitTrackAI application
"""

import pytest
import json
import tempfile
import os
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta

# Import the app components
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, DataManager, PlotGenerator, SimpleAI


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    dates = pd.date_range(start='2023-01-01', end='2023-01-10', freq='D')
    return {
        'DailyStepCount': pd.DataFrame({
            'date': dates,
            'total_value': [8000, 7500, 12000, 9000, 11000, 8500, 13000, 9500, 10500, 12000]
        }),
        'DailySleepSummary': pd.DataFrame({
            'date': dates,
            'sleep_minutes': [420, 450, 480, 390, 510, 440, 460, 430, 470, 490]
        }),
        'DailyActiveCalories': pd.DataFrame({
            'date': dates,
            'total_value': [300, 250, 450, 350, 400, 280, 500, 320, 380, 420]
        }),
        'DailyBasalCalories': pd.DataFrame({
            'date': dates,
            'total_value': [1500, 1480, 1520, 1490, 1530, 1500, 1540, 1510, 1525, 1535]
        })
    }


class TestDataManager:
    """Test DataManager class."""
    
    def test_init(self):
        """Test DataManager initialization."""
        db_path = "test.db"
        dm = DataManager(db_path)
        assert dm.db_path == db_path
    
    @patch('app.sqlite3.connect')
    def test_get_tables(self, mock_connect):
        """Test getting tables from database."""
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [('table1',), ('table2',)]
        mock_connect.return_value.cursor.return_value = mock_cursor
        
        dm = DataManager("test.db")
        tables = dm.get_tables()
        
        assert tables == ['table1', 'table2']
        mock_connect.assert_called_once_with("test.db")
    
    @patch('app.pd.read_sql_query')
    @patch('app.sqlite3.connect')
    def test_get_table_data(self, mock_connect, mock_read_sql):
        """Test getting data from a table."""
        mock_df = pd.DataFrame({'col1': [1, 2, 3]})
        mock_read_sql.return_value = mock_df
        
        dm = DataManager("test.db")
        result = dm.get_table_data("test_table")
        
        assert result.equals(mock_df)
        mock_read_sql.assert_called_once_with("SELECT * FROM test_table LIMIT 100", mock_connect.return_value)


class TestPlotGenerator:
    """Test PlotGenerator class."""
    
    def test_init(self):
        """Test PlotGenerator initialization."""
        mock_dm = MagicMock()
        pg = PlotGenerator(mock_dm)
        assert pg.data_manager == mock_dm
    
    def test_generate_plot_unknown_type(self):
        """Test generating plot with unknown type."""
        mock_dm = MagicMock()
        pg = PlotGenerator(mock_dm)
        
        result = pg.generate_plot("unknown_type")
        assert "error" in result
        assert "Unknown plot type" in result["error"]
    
    @patch('app.PlotGenerator._daily_steps_plot')
    def test_generate_plot_daily_steps(self, mock_steps_plot):
        """Test generating daily steps plot."""
        mock_dm = MagicMock()
        pg = PlotGenerator(mock_dm)
        mock_steps_plot.return_value = {"plot": "test", "type": "daily_steps"}
        
        result = pg.generate_plot("daily_steps")
        assert result == {"plot": "test", "type": "daily_steps"}
        mock_steps_plot.assert_called_once()


class TestSimpleAI:
    """Test SimpleAI class."""
    
    def test_init(self):
        """Test SimpleAI initialization."""
        mock_dm = MagicMock()
        ai = SimpleAI(mock_dm)
        assert ai.data_manager == mock_dm
        assert hasattr(ai, 'plot_generator')
    
    def test_chat_default_response(self):
        """Test default chat response."""
        mock_dm = MagicMock()
        ai = SimpleAI(mock_dm)
        
        response = ai.chat("hello")
        assert "type" in response
        assert response["type"] == "text"
        assert "I can help you" in response["response"]
    
    def test_chat_plot_request(self):
        """Test chat with plot request."""
        mock_dm = MagicMock()
        ai = SimpleAI(mock_dm)
        
        # Mock the plot generator
        ai.plot_generator.generate_plot = MagicMock(return_value={
            "plot": "test_plot",
            "type": "daily_steps",
            "title": "Daily Step Count"
        })
        
        response = ai.chat("show me my step data")
        assert response["type"] == "plot"
        assert "plot_data" in response


class TestFlaskApp:
    """Test Flask application endpoints."""
    
    def test_index_route(self, client):
        """Test the index route."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'FitTrackAI' in response.data
    
    def test_data_summary_route(self, client):
        """Test the data summary route."""
        with patch('app.data_manager.get_database_summary') as mock_summary:
            mock_summary.return_value = {"tables": [], "total_tables": 0}
            response = client.get('/api/data_summary')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "tables" in data
    
    def test_chat_route_no_message(self, client):
        """Test chat route with no message."""
        response = client.post('/api/chat', 
                             json={},
                             content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
    
    def test_chat_route_with_message(self, client):
        """Test chat route with a message."""
        with patch('app.ai_system.chat') as mock_chat:
            mock_chat.return_value = {"response": "test", "type": "text"}
            response = client.post('/api/chat',
                                 json={"message": "hello"},
                                 content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "response" in data
    
    def test_plot_route(self, client):
        """Test the plot generation route."""
        with patch('app.PlotGenerator') as mock_plot_gen:
            mock_instance = MagicMock()
            mock_instance.generate_plot.return_value = {"plot": "test"}
            mock_plot_gen.return_value = mock_instance
            
            response = client.post('/api/plot',
                                 json={"type": "daily_steps"},
                                 content_type='application/json')
            assert response.status_code == 200
            data = json.loads(response.data)
            assert "plot" in data


class TestIntegration:
    """Integration tests."""
    
    def test_full_workflow(self, client):
        """Test a complete workflow."""
        # Test index page loads
        response = client.get('/')
        assert response.status_code == 200
        
        # Test data summary
        response = client.get('/api/data_summary')
        assert response.status_code == 200
        
        # Test chat with analysis request
        with patch('app.ai_system.chat') as mock_chat:
            mock_chat.return_value = {
                "response": "Analysis complete",
                "type": "text"
            }
            response = client.post('/api/chat',
                                 json={"message": "analyze my steps"},
                                 content_type='application/json')
            assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__]) 