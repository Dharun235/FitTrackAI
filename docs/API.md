# FitTrackAI API Documentation

## Overview

FitTrackAI provides a RESTful API for health data analysis and visualization. The API is built with Flask and supports real-time communication via WebSocket.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, the API does not require authentication. All endpoints are publicly accessible.

## Endpoints

### 1. Health Check

**GET** `/api/health`

Returns the health status of the application and its services.

**Response:**
```json
{
  "status": "healthy",
  "services": {
    "data_processor": true,
    "rag_system": true,
    "chart_generator": true
  }
}
```

### 2. Data Summary

**GET** `/api/data_summary`

Returns a summary of the database contents including tables and record counts.

**Response:**
```json
{
  "total_tables": 8,
  "tables": [
    {
      "name": "DailyStepCount",
      "record_count": 738,
      "columns": ["date", "total_value"]
    },
    {
      "name": "DailySleepSummary",
      "record_count": 365,
      "columns": ["date", "sleep_minutes"]
    }
  ]
}
```

### 3. Chat Interface

**POST** `/api/chat`

Send a message to the AI chat system and receive a response.

**Request Body:**
```json
{
  "message": "Show me my step data"
}
```

**Response:**
```json
{
  "response": "Here's your step data visualization! 🚶‍♂️ I've included a 7-day moving average to show trends.",
  "type": "plot",
  "plot_data": {
    "plot": "{plotly_json_data}",
    "type": "daily_steps",
    "title": "Daily Step Count"
  }
}
```

**Response Types:**
- `text`: Simple text response
- `plot`: Response with interactive plot data

### 4. Plot Generation

**POST** `/api/plot`

Generate a specific type of plot.

**Request Body:**
```json
{
  "type": "daily_steps"
}
```

**Available Plot Types:**
- `daily_steps`: Step count with moving average
- `sleep_analysis`: Sleep duration with quality indicators
- `calories_burned`: Active and basal calories
- `distance_walked`: Distance tracking
- `flights_climbed`: Flights climbed data
- `walking_metrics`: Walking speed and steadiness

**Response:**
```json
{
  "plot": "{plotly_json_data}",
  "type": "daily_steps",
  "title": "Daily Step Count"
}
```

## WebSocket Events

### Connection

Connect to the WebSocket endpoint:
```
ws://localhost:5000/socket.io/
```

### Events

#### `chat_message`

Send a chat message via WebSocket.

**Emit:**
```javascript
socket.emit('chat_message', {
  message: "Analyze my sleep patterns"
});
```

**Listen:**
```javascript
socket.on('chat_response', function(data) {
  console.log(data);
  // Handle response
});
```

#### `connect`

Connection established event.

**Listen:**
```javascript
socket.on('connect', function() {
  console.log('Connected to FitTrackAI');
});
```

#### `status`

Status updates from the server.

**Listen:**
```javascript
socket.on('status', function(data) {
  console.log(data.message);
});
```

## Error Handling

All endpoints return appropriate HTTP status codes:

- `200`: Success
- `400`: Bad Request (missing parameters, invalid data)
- `500`: Internal Server Error

**Error Response Format:**
```json
{
  "error": "Error message describing the issue"
}
```

## Rate Limiting

Currently, there are no rate limits implemented. Consider implementing rate limiting for production use.

## CORS

The API supports CORS for cross-origin requests. All origins are allowed in development.

## Data Formats

### Date Format
All dates are in ISO 8601 format: `YYYY-MM-DD`

### Numeric Values
- Steps: Integer values
- Sleep: Minutes (can be converted to hours)
- Calories: Float values
- Distance: Kilometers (float values)
- Flights: Integer values

## Example Usage

### JavaScript (Fetch API)

```javascript
// Get data summary
fetch('/api/data_summary')
  .then(response => response.json())
  .then(data => console.log(data));

// Send chat message
fetch('/api/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Show me my step trends'
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

### Python (requests)

```python
import requests

# Get data summary
response = requests.get('http://localhost:5000/api/data_summary')
data = response.json()
print(data)

# Send chat message
response = requests.post('http://localhost:5000/api/chat', 
                        json={'message': 'Analyze my sleep'})
data = response.json()
print(data)
```

### cURL

```bash
# Get data summary
curl http://localhost:5000/api/data_summary

# Send chat message
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Show me my step data"}'
```

## WebSocket Example (JavaScript)

```javascript
const socket = io('http://localhost:5000');

socket.on('connect', function() {
  console.log('Connected to FitTrackAI');
});

socket.on('chat_response', function(data) {
  if (data.type === 'plot') {
    // Render plot
    Plotly.newPlot('plot-container', JSON.parse(data.plot_data.plot));
  } else {
    // Display text response
    console.log(data.response);
  }
});

// Send message
socket.emit('chat_message', {
  message: 'Show me my calorie data'
});
```

## Future Enhancements

- Authentication and authorization
- Rate limiting
- API versioning
- Bulk data operations
- Real-time data streaming
- Webhook support
- API key management 