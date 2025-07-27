# 🤖 FitTrackAI - Health Data Assistant

A **free, local web application** that helps you analyze and visualize your Apple Health data through an intelligent chat interface powered by **Ollama LLM**. 

## ⚠️ **Important: Ollama Required**

**FitTrackAI requires Ollama to function.** Ollama is a free, local LLM that runs on your computer.

### **Quick Ollama Setup:**
```bash
# 1. Install Ollama
python setup_ollama.py

# 2. Or install manually:
# Visit: https://ollama.ai/download
# Then run: ollama serve
# Then run: ollama pull llama2
```

## ✨ Features

### 🧠 **Smart AI Assistant**
- **Ollama LLM** - Free, local AI powered by llama2 model
- **Data-aware responses** - Understands your actual health data
- **Natural conversation** - Chat naturally about your fitness journey
- **Intelligent insights** - Provides personalized health recommendations

### 📊 **Data Analysis & Visualization**
- **Interactive charts** - Plotly-powered visualizations
- **Multiple metrics** - Steps, sleep, calories, distance, flights climbed
- **Trend analysis** - See patterns and progress over time
- **Custom plots** - Generate specific visualizations on demand

### 🎯 **Health Insights**
- **Performance tracking** - Monitor your fitness progress
- **Goal recommendations** - Get personalized fitness targets
- **Pattern recognition** - Identify trends in your health data
- **Comprehensive analysis** - Deep insights into your wellness journey

### 💻 **User Experience**
- **Real-time chat** - Instant responses via WebSocket
- **Modern UI** - Clean, responsive interface
- **Quick actions** - One-click access to common queries
- **Data summary** - Overview of your health metrics

## 🚀 Quick Start

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Setup Ollama (REQUIRED)**
```bash
# Automatic setup
python setup_ollama.py

# Or manual setup:
# 1. Install Ollama: https://ollama.ai/download
# 2. Start Ollama: ollama serve
# 3. Download model: ollama pull llama2
```

### 3. **Start the Application**
```bash
python start_app.py
```

### 4. **Open Your Browser**
Go to: `http://localhost:5000`

### 5. **Start Chatting!**
- Ask about your health data
- Request visualizations
- Get personalized insights
- Track your progress

## 📊 **Data Profile**

Your FitTrackAI system contains:
- **2+ years** of health data
- **11 different metrics** tracked
- **Real-time analysis** capabilities
- **Personalized insights** based on your data

### **Available Metrics:**
- 🚶‍♂️ **Steps** - Daily step count and trends
- 😴 **Sleep** - Sleep duration and quality analysis
- 🔥 **Calories** - Active and basal calorie burn
- 🏃‍♂️ **Distance** - Walking and running distance
- 🏢 **Flights** - Stairs climbed
- 🚶‍♀️ **Walking Metrics** - Speed, steadiness, gait analysis

## 💬 **Example Conversations**

### **Data Analysis:**
```
You: "How am I doing with my steps?"
AI: "🚶‍♂️ Based on your data, you're averaging 6,223 steps per day. 
     Your best day was 12,450 steps! Let me show you a detailed 
     visualization of your trends."

You: "Analyze my sleep patterns"
AI: "😴 I'll analyze your sleep data showing quality trends, 
     duration consistency, and help identify factors that might 
     affect your rest."
```

### **Visualizations:**
```
You: "Show me my step data"
AI: "🚶‍♂️ Here's your step visualization with daily steps and 
     7-day moving average to show trends!"

You: "Generate a sleep analysis plot"
AI: "😴 Here's your sleep analysis with categorized quality 
     and duration patterns!"
```

### **Insights:**
```
You: "What should I focus on improving?"
AI: "🎯 Based on your data, I recommend focusing on:
     • Increasing daily steps to reach 10,000
     • Improving sleep consistency
     • Adding more active calorie burn
     Let me show you detailed analysis!"
```

## 🛠️ **Technology Stack**

### **Backend:**
- **Flask** - Web framework
- **Flask-SocketIO** - Real-time communication
- **SQLite** - Local database storage
- **Pandas** - Data processing and analysis

### **Frontend:**
- **HTML5/CSS3** - Modern, responsive interface
- **JavaScript** - Interactive chat experience
- **Socket.IO** - Real-time client-server communication

### **Data Visualization:**
- **Plotly** - Interactive charts and plots
- **Matplotlib** - Static plotting capabilities
- **Seaborn** - Statistical visualizations

### **AI System:**
- **Ollama** - Free, local LLM (llama2 model)
- **LangChain** - LLM integration framework
- **Data context analysis** - Deep understanding of your health data
- **Natural language processing** - Understands health-related queries

## 📁 **Project Structure**

```
FitTrackAI/
├── app.py                 # Main Flask application
├── start_app.py          # Application startup script
├── setup_ollama.py       # Ollama setup script (REQUIRED)
├── data_explorer.py      # Data exploration tool
├── requirements.txt      # Python dependencies
├── data/
│   └── db/
│       └── processed_apple_health_data.db  # Your health data
├── templates/
│   └── index.html        # Web interface
└── docs/
    └── API.md            # API documentation
```

## 🎯 **Key Benefits**

### **✅ Always Available**
- Free, local LLM (no API costs)
- Works offline
- No rate limits

### **🔒 Privacy-First**
- All data stays local
- No cloud processing
- Complete data control

### **🚀 Fast & Responsive**
- Instant responses
- Real-time chat
- Smooth interactions

### **📊 Data-Driven**
- Actual health data analysis
- Personalized insights
- Trend recognition

## 🎮 **Quick Actions**

Use these quick action buttons for instant access:
- **📊 Show Steps** - Generate step visualizations
- **😴 Sleep Analysis** - Get sleep insights
- **🔥 Calorie Burn** - View calorie data
- **🏃‍♂️ Distance** - See walking/running data
- **🎯 Performance** - Overall health review

## 🔧 **Advanced Features**

### **Data Explorer Tool**
```bash
python data_explorer.py
```
Get a comprehensive overview of your health data, including:
- Database structure analysis
- Statistical insights
- Health recommendations
- Data quality assessment

### **Custom Visualizations**
Ask for specific plots:
- "Show me my walking speed trends"
- "Generate a sleep quality analysis"
- "Plot my calorie burn over time"
- "Compare my steps vs distance"

## 🚀 **Getting Started**

1. **Ensure your Apple Health data is processed** in `data/db/processed_apple_health_data.db`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Setup Ollama (REQUIRED)**: `python setup_ollama.py`
4. **Start the application**: `python start_app.py`
5. **Open your browser**: Navigate to `http://localhost:5000`
6. **Start chatting**: Ask about your health data!

## 🎉 **Ready to Use!**

Your FitTrackAI system is now ready to help you understand and improve your health journey. The Ollama-powered AI provides intelligent, data-aware responses using a free, local LLM.

**Start exploring your health data today!** 🚀 