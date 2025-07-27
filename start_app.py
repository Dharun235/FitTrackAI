#!/usr/bin/env python3
"""
FitTrackAI Startup Script

This script handles port conflicts and starts the application cleanly.
"""

import os
import sys
import subprocess
import time
import signal
import psutil

def kill_process_on_port(port):
    """Kill any process using the specified port."""
    try:
        # Find processes using the port
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                connections = proc.info['connections']
                if connections:
                    for conn in connections:
                        if conn.laddr.port == port:
                            print(f"🔄 Killing process {proc.info['name']} (PID: {proc.info['pid']}) on port {port}")
                            proc.terminate()
                            proc.wait(timeout=5)
                            return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                continue
        return False
    except Exception as e:
        print(f"⚠️ Error killing process: {e}")
        return False

def check_port_available(port):
    """Check if port is available."""
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def start_application():
    """Start the FitTrackAI application."""
    port = 5000
    
    print("🚀 Starting FitTrackAI...")
    print("=" * 50)
    
    # Check if port is available
    if not check_port_available(port):
        print(f"⚠️ Port {port} is in use. Attempting to free it...")
        if kill_process_on_port(port):
            print("✅ Port freed successfully")
            time.sleep(2)  # Wait for port to be released
        else:
            print(f"❌ Could not free port {port}")
            print("Please manually close any applications using port 5000")
            return False
    
    # Check if database exists
    db_path = "data/db/processed_apple_health_data.db"
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        print("Please ensure your Apple Health data is processed")
        return False
    
    # Start the application
    try:
        print(f"📊 Using database: {db_path}")
        print(f"🌐 Starting server on port {port}...")
        
        # Import and run the app
        from app import app, socketio
        
        print("✅ Application started successfully!")
        print(f"🌐 Open your browser to: http://localhost:{port}")
        print("📱 Press Ctrl+C to stop the application")
        
        socketio.run(app, debug=True, host='0.0.0.0', port=port)
        
    except KeyboardInterrupt:
        print("\n🛑 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False
    
    return True

def main():
    """Main function."""
    print("🤖 FitTrackAI - Health Data Assistant")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check required files
    required_files = [
        "app.py",
        "requirements.txt",
        "data/db/processed_apple_health_data.db"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Required file not found: {file_path}")
            return False
    
    print("✅ All required files found")
    
    # Start the application
    return start_application()

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 