# 🤖 FitTrackAI - Health Data Assistant

A **free, local web application** that transforms your Apple Health data into an intelligent AI assistant. Chat with your health data and get personalized insights powered by **Ollama LLM**.

## ⚠️ **Ollama Required**

**FitTrackAI requires Ollama to function.** Ollama is a free, local LLM that runs on your computer.

### **Quick Setup:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup Ollama (REQUIRED)
python setup_ollama.py

# 3. Start the application
python start_app.py

# 4. Open browser: http://localhost:5000
```

## ✨ **Features**

### 🤖 **AI-Powered Health Assistant**
- **Real LLM Responses** - Powered by Ollama's llama2 model
- **Data-Aware Conversations** - AI understands your actual health data
- **Natural Language Processing** - Chat naturally about your fitness journey
- **Personalized Insights** - Get recommendations based on your data

### 📊 **Data Analysis & Visualization**
- **11 Health Metrics** - Steps, sleep, calories, distance, walking metrics
- **Interactive Charts** - Plotly-powered visualizations
- **Trend Analysis** - Identify patterns and progress over time
- **Statistical Insights** - Detailed analysis of your health data

### 💻 **Modern Web Interface**
- **Real-time Chat** - Instant responses via WebSocket
- **Responsive Design** - Works on desktop and mobile
- **Quick Actions** - One-click access to common queries
- **Data Summary** - Overview of your health metrics

## 🔒 **Privacy & Security**

- ✅ **All data stays local** - No cloud processing
- ✅ **No external API calls** for user data
- ✅ **Complete data control** - Your data, your rules
- ✅ **Free and open source** - Transparent codebase

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Setup Ollama (REQUIRED)**
```bash
# Automatic setup
python setup_ollama.py

# Or manual setup:
# 1. Install Ollama: https://ollama.ai/download
# 2. Start Ollama: ollama serve
# 3. Download model: ollama pull llama2
```

### **3. Start the Application**
```bash
python start_app.py
```

### **4. Open Your Browser**
Go to: `http://localhost:5000`

### **5. Start Chatting!**
- Ask about your health data
- Request visualizations
- Get personalized insights

## 💬 **Example Conversations**

```
You: "How am I doing with my steps?"
AI: "🚶‍♂️ Based on your data, you're averaging 6,223 steps per day. 
     Your best day was 12,450 steps! Let me show you a detailed 
     visualization of your trends."

You: "Show me my step data"
AI: "🚶‍♂️ Here's your step visualization with daily steps and 
     7-day moving average to show trends!"

You: "What should I focus on improving?"
AI: "🎯 Based on your data, I recommend focusing on:
     • Increasing daily steps to reach 10,000
     • Improving sleep consistency
     • Adding more active calorie burn"
```

## 📊 **Available Health Metrics**

- 🚶‍♂️ **Steps** - Daily step count and trends
- 😴 **Sleep** - Sleep duration and quality analysis
- 🔥 **Calories** - Active and basal calorie burn
- 🏃‍♂️ **Distance** - Walking and running distance
- 🏢 **Flights** - Stairs climbed
- 🚶‍♀️ **Walking Metrics** - Speed, steadiness, gait analysis

## 🛠️ **Technology Stack**

- **Backend**: Flask, Flask-SocketIO, SQLite, Pandas
- **Frontend**: HTML5, CSS3, JavaScript, Socket.IO, Plotly.js
- **AI**: Ollama (llama2 model), LangChain
- **Data**: Apple Health data processing and analysis

## 📁 **Project Structure**

```
FitTrackAI/
├── app.py                 # Main Flask application
├── start_app.py          # Application startup script
├── setup_ollama.py       # Ollama setup script (REQUIRED)
├── requirements.txt      # Python dependencies
├── data/
│   └── db/
│       └── processed_apple_health_data.db  # Your health data
└── templates/
    └── index.html        # Web interface
```

## 🎯 **Use Cases**

- **Health enthusiasts** wanting to understand their data
- **Developers** learning AI and data visualization
- **Privacy-conscious users** who want local solutions
- **Students** studying health data analysis
- **Researchers** exploring health data patterns

## 🚀 **Development**

### **Easy Commands**
```bash
make help          # Show all available commands
make install       # Install dependencies
make setup         # Setup Ollama
make run           # Start application
make test          # Run tests
```

## 🤝 **Contributing**

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Start your health data journey with FitTrackAI today!** 🚀

*Transform your Apple Health data into intelligent insights with the power of local AI.* 