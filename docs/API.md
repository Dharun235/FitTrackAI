# FitTrackAI API Documentation

## Overview

FitTrackAI provides a RESTful API and WebSocket interface for interacting with Apple Health data through an intelligent AI assistant powered by Ollama LLM.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, no authentication is required for local deployment.

## API Endpoints

### 1. **GET /** - Main Application
Returns the main chat interface HTML page.

**Response:** HTML page with chat interface

---

### 2. **POST /api/chat** - Chat with AI
Send a message to the AI assistant and get a response.

**Request Body:**
```json
{
  "message": "Show me my step data"
}
```

**Response:**
```json
{
  "response": "🚶‍♂️ Here's your step visualization with daily steps and 7-day moving average to show trends!",
  "plot": {
    "data": [...],
    "layout": {...}
  },
  "provider": "OLLAMA"
}
```

**Error Response:**
```json
{
  "response": "Sorry, I encountered an error: Ollama is not running. Please make sure Ollama is installed and running.",
  "provider": "ERROR"
}
```

---

### 3. **POST /api/plot** - Generate Plot
Generate a specific type of plot.

**Request Body:**
```json
{
  "plot_type": "daily_steps"
}
```

**Available Plot Types:**
- `daily_steps` - Daily step count visualization
- `sleep_analysis` - Sleep duration and quality analysis
- `calories_burned` - Active and basal calorie burn
- `distance_walked` - Walking and running distance
- `flights_climbed` - Stairs climbed data
- `walking_metrics` - Walking speed and steadiness

**Response:**
```json
{
  "data": [...],
  "layout": {...},
  "config": {...}
}
```

---

### 4. **GET /api/data_summary** - Get Data Overview
Get a comprehensive overview of the health data in the database.

**Response:**
```json
{
  "summary": "📊 Database Overview:\nTotal tables: 11\n\n📋 DailyStepCount:\n  • Records: 738 (2023-06-01 to 2025-06-30)\n  • Columns: date, total_value\n  • Insights: Avg total_value: 6223.0 steps (max: 12450.0)\n\n..."
}
```

---

### 5. **GET /api/llm_status** - Check LLM Status
Get the status of available LLM providers.

**Response:**
```json
{
  "available_providers": ["ollama"],
  "current_provider": "ollama",
  "ollama_available": true,
  "ollama_required": true
}
```

---

## WebSocket Events

### Connection
Connect to the WebSocket server:
```javascript
const socket = io('http://localhost:5000');
```

### Events

#### **chat_message** - Send Message
Send a chat message to the AI.

**Emit:**
```javascript
socket.emit('chat_message', {
  message: 'Show me my step data'
});
```

#### **chat_response** - Receive Response
Receive AI response.

**Listen:**
```javascript
socket.on('chat_response', function(data) {
  console.log('AI Response:', data.response);
  if (data.plot) {
    // Handle plot data
    Plotly.newPlot('plot-container', data.plot.data, data.plot.layout);
  }
});
```

---

## Data Models

### Health Data Tables

The application works with the following Apple Health data tables:

1. **DailyStepCount** - Daily step count data
2. **DailySleepSummary** - Sleep duration and quality
3. **DailyActiveCalories** - Active calorie burn
4. **DailyBasalCalories** - Basal calorie burn
5. **DailyDistanceWalkRun** - Walking and running distance
6. **DailyFlightsClimbed** - Stairs climbed
7. **WalkingSpeed** - Walking speed metrics
8. **WalkingSteadiness** - Walking steadiness data
9. **WalkingAsymmetry** - Walking asymmetry data
10. **WalkingDoubleSupport** - Walking double support time
11. **WalkingStepLength** - Walking step length data

### Plot Data Structure

Plot responses follow the Plotly.js format:

```json
{
  "data": [
    {
      "x": ["2023-06-01", "2023-06-02", ...],
      "y": [6234, 7890, ...],
      "type": "scatter",
      "mode": "lines+markers",
      "name": "Daily Steps"
    }
  ],
  "layout": {
    "title": "Daily Step Count",
    "xaxis": {"title": "Date"},
    "yaxis": {"title": "Steps"}
  },
  "config": {
    "responsive": true,
    "displayModeBar": true
  }
}
```

---

## Error Handling

### Common Error Codes

- **500** - Internal server error
- **400** - Bad request (invalid plot type, etc.)
- **503** - Service unavailable (Ollama not running)

### Error Response Format

```json
{
  "error": "Error description",
  "details": "Additional error information"
}
```

---

## Rate Limiting

Currently, no rate limiting is implemented for local deployment.

## CORS

CORS is enabled for local development:
```python
socketio = SocketIO(app, cors_allowed_origins="*")
```

---

## Examples

### JavaScript Example

```javascript
// Connect to WebSocket
const socket = io('http://localhost:5000');

// Send a message
socket.emit('chat_message', {
  message: 'Analyze my sleep patterns'
});

// Listen for response
socket.on('chat_response', function(data) {
  if (data.plot) {
    // Display plot
    Plotly.newPlot('plot-container', data.plot.data, data.plot.layout);
  }
  
  // Display text response
  document.getElementById('chat-output').innerHTML += 
    `<div class="ai-response">${data.response}</div>`;
});
```

### Python Example

```python
import requests

# Send chat message
response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'Show me my step data'
})

data = response.json()
print(f"AI Response: {data['response']}")

if 'plot' in data:
    print("Plot data available")
```

---

## Development

### Running the API Server

```bash
# Start the application
python start_app.py

# Or in development mode
python app.py
```

### Testing the API

```bash
# Test data summary endpoint
curl http://localhost:5000/api/data_summary

# Test chat endpoint
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## Notes

- All data processing happens locally
- No external API calls for user data
- Ollama LLM is required for AI functionality
- Database is SQLite-based for simplicity
- Real-time communication via WebSocket 