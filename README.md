# FitTrackAI - Interactive Health Data Chat & Analysis Platform

🤖 **AI-Powered Health Data Assistant** - Chat with your Apple Health data and get intelligent insights, beautiful visualizations, and personalized recommendations.

## ✨ Features

### 🎯 **Smart Chat Interface**
- **Natural Language Processing**: Ask questions in plain English
- **Real-time Responses**: Instant AI-powered responses via WebSocket
- **Contextual Understanding**: AI understands your health data context
- **Emoji & Personality**: Friendly, engaging chat experience

### 📊 **Advanced Data Analysis**
- **Trend Analysis**: Identify patterns and trends in your health data
- **Statistical Insights**: Get detailed statistics and comparisons
- **Performance Metrics**: Track improvements over time
- **Personalized Recommendations**: AI-generated health suggestions

### 📈 **Interactive Visualizations**
- **Dynamic Charts**: Real-time plot generation with Plotly
- **Multiple Chart Types**: Line charts, bar charts, scatter plots
- **Enhanced Plots**: Moving averages, color coding, quality indicators
- **Custom Visualizations**: Request specific data combinations

### 🚀 **User Experience**
- **Quick Action Buttons**: One-click access to common features
- **Responsive Design**: Works on desktop and mobile
- **Real-time Updates**: Live chat with typing indicators
- **Modern UI**: Beautiful gradient design with smooth animations

## 🛠️ Technology Stack

- **Backend**: Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly.js, Interactive Charts
- **Real-time Communication**: Socket.IO
- **Database**: SQLite (Apple Health data)
- **AI**: Template-based responses (easily extensible to LLMs)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone or Download the Project**
   ```bash
   # If you have the project files, just navigate to the directory
   cd FitTrackAI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Open in Browser**
   ```
   http://localhost:5000
   ```

## 📖 User Guide

### 🎯 Getting Started

1. **Open the Application**
   - Navigate to `http://localhost:5000`
   - You'll see a beautiful chat interface with quick action buttons

2. **Explore Quick Actions**
   - **📊 Quick Plots**: Generate visualizations instantly
   - **📈 Data Analysis**: Get detailed insights and trends
   - **🔍 Custom & Info**: Access specific data and summaries

3. **Start Chatting**
   - Type your questions in the chat input
   - Use natural language like "Show me my step data"
   - Ask for analysis like "Analyze my sleep patterns"

### 💬 Chat Commands & Examples

#### 📊 **Plot Generation**
```
"Show me my step data"
"Display my sleep analysis"
"Create a calorie burn chart"
"Plot my distance walked"
"Show my flights climbed"
"Visualize my walking metrics"
```

#### 📈 **Data Analysis**
```
"Analyze my step trends"
"Show me sleep patterns"
"Analyze my calorie burn"
"Give me distance insights"
"Show general health trends"
"What are my fitness patterns?"
```

#### 🔍 **Custom Requests**
```
"Give me a summary of my data"
"Show me walking speed data"
"Create a custom plot of sleep vs steps"
"What can you help me with?"
"Show me my health statistics"
```

#### 💡 **Natural Language Examples**
```
"How am I doing with my steps?"
"What's my sleep quality like?"
"Am I improving my fitness?"
"Show me trends in my activity"
"Compare my recent vs past performance"
```

### 🎨 **Interactive Features**

#### **Quick Action Buttons**
- **Color-coded categories** for easy navigation
- **Hover effects** with smooth animations
- **One-click access** to common features

#### **Real-time Chat**
- **Typing indicators** show when AI is thinking
- **Instant responses** via WebSocket
- **Message history** with user/AI avatars

#### **Dynamic Plots**
- **Interactive charts** with zoom and hover
- **Responsive design** adapts to screen size
- **Professional styling** with gradients and shadows

### 📊 **Available Data Types**

The application works with your Apple Health data including:

- **Steps**: Daily step count with trends
- **Sleep**: Duration and quality analysis
- **Calories**: Active and basal calorie burn
- **Distance**: Walking/running distance
- **Flights**: Stairs climbed
- **Walking Metrics**: Speed, steadiness, asymmetry

### 🎯 **Analysis Features**

#### **Step Analysis**
- Average daily steps
- Best/worst performance days
- Trend analysis (improving/declining)
- Personalized recommendations
- 7-day moving averages

#### **Sleep Analysis**
- Sleep duration statistics
- Quality breakdown (Excellent/Good/Fair/Poor)
- Sleep pattern insights
- Recommendations for improvement

#### **Calorie Analysis**
- Active vs basal calories
- Total daily calorie burn
- Performance trends
- Activity level assessment

#### **Distance Analysis**
- Daily distance tracking
- Total distance covered
- Performance trends
- Activity recommendations

## 🔧 Advanced Usage

### **Custom Plot Requests**
Ask for specific data combinations:
```
"Show me walking speed vs steadiness"
"Create a plot of sleep vs steps"
"Display calories over time"
```

### **Trend Analysis**
Get detailed trend insights:
```
"Are my steps improving?"
"What's my sleep trend?"
"How are my calories trending?"
```

### **Comparative Analysis**
Compare different time periods:
```
"Compare my recent vs past performance"
"Show me this month vs last month"
"What's my weekly trend?"
```

## 🎨 **Visualization Types**

### **Enhanced Step Charts**
- Daily step count with markers
- 7-day moving average line
- Trend indicators
- Interactive hover details

### **Sleep Quality Charts**
- Color-coded bars by quality
- Duration in hours
- Quality distribution
- Pattern visualization

### **Calorie Breakdown**
- Active calories line
- Basal calories line
- Total calories trend
- Multi-line visualization

### **Distance Tracking**
- Daily distance with markers
- Weekly totals
- Performance trends
- Interactive charts

### **Walking Metrics**
- Speed over time
- Steadiness tracking
- Dual-axis charts
- Performance correlation

## 🚀 **Performance & Features**

### **Real-time Processing**
- Instant data retrieval
- Live chart generation
- Responsive UI updates
- WebSocket communication

### **Data Security**
- Local data processing
- No external API calls
- Privacy-focused design
- Secure data handling

### **Scalability**
- Modular code structure
- Easy to extend features
- Configurable components
- Clean architecture

## 🔮 **Future Enhancements**

### **AI Integration**
- Connect to real LLMs (Ollama, HuggingFace)
- Advanced natural language processing
- Predictive analytics
- Personalized recommendations

### **Additional Features**
- Data export capabilities
- Goal setting and tracking
- Social sharing
- Mobile app version

### **Advanced Analytics**
- Machine learning insights
- Predictive health trends
- Correlation analysis
- Health score calculation

## 🛠️ **Development**

### **Project Structure**
```
FitTrackAI/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Chat interface
├── data/
│   └── db/               # SQLite database files
├── tests/                # Test files
├── docs/                 # Documentation
├── README.md             # Project documentation
├── CONTRIBUTING.md       # Contributing guidelines
├── LICENSE               # MIT License
├── setup.py              # Package setup
├── Makefile              # Development commands
└── .gitignore            # Git ignore rules
```

### **Key Components**
- **DataManager**: Database operations and data retrieval
- **PlotGenerator**: Chart creation and visualization
- **SimpleAI**: Chat processing and analysis
- **Flask App**: Web server and API endpoints

### **Development Commands**
```bash
# Install dependencies
make install

# Run the application
make run

# Run tests
make test

# Format code
make format

# Run all checks
make check
```

### **Extending the AI**
The current implementation uses template-based responses. To integrate with actual LLMs:

1. **Ollama Integration**
   ```python
   # Add to SimpleAI class
   from langchain_community.llms import Ollama
   
   def _initialize_ollama(self):
       self.llm = Ollama(model="llama2")
   ```

2. **HuggingFace Integration**
   ```python
   # Add HuggingFace API support
   from transformers import pipeline
   
   def _initialize_huggingface(self):
       self.classifier = pipeline("text-generation")
   ```

## 📝 **Troubleshooting**

### **Common Issues**

1. **Port Already in Use**
   ```bash
   # Kill existing process
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   ```

2. **Database Not Found**
   - Ensure `data/db/processed_apple_health_data.db` exists
   - Check file permissions

3. **Dependencies Missing**
   ```bash
   pip install -r requirements.txt
   ```

### **Performance Tips**
- Use SSD storage for faster database access
- Close other applications to free memory
- Use modern browser for best experience

## 🤝 **Contributing**

This project is designed for learning purposes. Feel free to:
- Add new visualization types
- Enhance the AI responses
- Improve the UI/UX
- Add new data analysis features

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 **Acknowledgments**

- **Apple Health**: For the health data format
- **Plotly**: For beautiful interactive charts
- **Flask**: For the web framework
- **Bootstrap**: For the responsive design

---

**🎉 Ready to explore your health data? Start chatting with FitTrackAI!** 