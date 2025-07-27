# FitTrackAI Deployment Guide

This guide covers how to deploy FitTrackAI for local development and simple hosting scenarios.

## 🏠 Local Development

### Prerequisites
- Python 3.8+
- pip package manager
- Git

### Quick Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/FitTrackAI.git
cd FitTrackAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:5000`

## 🚀 Simple Hosting Options

### 1. Heroku (Free Tier)

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Deployment Steps
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-fittrackai-app

# Add Python buildpack
heroku buildpacks:set heroku/python

# Deploy
git push heroku main

# Open the app
heroku open
```

#### Required Files
- `Procfile` (create this file):
```
web: python app.py
```

### 2. Python Anywhere (Free Tier)

#### Steps
1. Create account at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your project files
3. Create a new web app
4. Set the WSGI configuration file to point to your Flask app
5. Install dependencies in the bash console

### 3. Railway (Free Tier)

#### Steps
1. Connect your GitHub repository to Railway
2. Railway will automatically detect Python and install dependencies
3. Set environment variables if needed
4. Deploy with one click

## 🔧 Configuration

### Environment Variables
Create a `.env` file for local development:
```env
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=your-secret-key-here
DATABASE_PATH=data/db/processed_apple_health_data.db
```

### Production Settings
For production deployment:
```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-production-secret-key
DATABASE_PATH=/path/to/your/database.db
```

## 📁 File Structure for Deployment

Ensure your deployment includes these essential files:
```
FitTrackAI/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── templates/
│   └── index.html        # Frontend
├── data/
│   └── db/               # Database files
├── .gitignore            # Git ignore rules
├── README.md             # Documentation
└── Procfile              # For Heroku (if using)
```

## 🛡️ Security Considerations

### For Production
1. **Change Secret Key**: Use a strong, unique secret key
2. **Database Security**: Ensure database files are not publicly accessible
3. **HTTPS**: Use HTTPS in production
4. **Environment Variables**: Store sensitive data in environment variables

### Example Production Configuration
```python
# In app.py
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['DATABASE_PATH'] = os.getenv('DATABASE_PATH', 'data/db/processed_apple_health_data.db')
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Find process using port 5000
   lsof -i :5000
   # Kill the process
   kill -9 <PID>
   ```

2. **Database Not Found**
   - Ensure database file exists in the correct path
   - Check file permissions
   - Verify database path in configuration

3. **Dependencies Missing**
   ```bash
   pip install -r requirements.txt
   ```

4. **Permission Errors**
   ```bash
   # Make sure you have write permissions
   chmod 755 data/
   chmod 644 data/db/*.db
   ```

### Logs and Debugging
```bash
# Run with debug mode
FLASK_DEBUG=1 python app.py

# Check application logs
tail -f app.log
```

## 📊 Performance Optimization

### For Local Development
- Use SSD storage for faster database access
- Close unnecessary applications
- Use modern browser

### For Production
- Use production WSGI server (Gunicorn)
- Enable caching
- Optimize database queries
- Use CDN for static assets

### Example Gunicorn Configuration
```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🔄 Continuous Deployment

### GitHub Actions (Simple)
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
        heroku_app_name: ${{ secrets.HEROKU_APP_NAME }}
        heroku_email: ${{ secrets.HEROKU_EMAIL }}
```

## 📈 Monitoring

### Health Checks
The application includes a health check endpoint:
```
GET /api/data_summary
```

### Logging
Enable logging for production:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

## 🎯 Next Steps

1. **Choose a hosting platform** based on your needs
2. **Set up environment variables** for production
3. **Configure domain** (if needed)
4. **Set up monitoring** and logging
5. **Test thoroughly** before going live

## 📞 Support

For deployment issues:
- Check the [troubleshooting section](#troubleshooting)
- Review platform-specific documentation
- Open an issue on GitHub

---

**Happy Deploying! 🚀** 