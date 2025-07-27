#!/usr/bin/env python3
"""
Ollama Setup Script for FitTrackAI

This script helps you set up Ollama for local LLM usage with FitTrackAI.
Ollama is REQUIRED for FitTrackAI to function.
"""

import subprocess
import sys
import os
import requests
import json
import time

def check_ollama_installed():
    """Check if Ollama is installed and running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def install_ollama():
    """Install Ollama based on the operating system."""
    system = sys.platform

    print("🚀 Installing Ollama...")

    if system == "win32":
        print("📥 Downloading Ollama for Windows...")
        print("Please visit: https://ollama.ai/download")
        print("Download and install the Windows version manually.")
        print("\nAfter installation:")
        print("1. Open Command Prompt as Administrator")
        print("2. Run: ollama serve")
        print("3. In another terminal: ollama pull llama2")
        return False

    elif system == "darwin":  # macOS
        try:
            subprocess.run(["brew", "install", "ollama"], check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ Homebrew not found. Please install Homebrew first:")
            print("https://brew.sh")
            return False

    elif system.startswith("linux"):
        try:
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh", "|", "sh"
            ], shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install Ollama. Please install manually:")
            print("https://ollama.ai/download")
            return False

    return False

def start_ollama_service():
    """Start the Ollama service."""
    print("🚀 Starting Ollama service...")
    try:
        if sys.platform == "win32":
            subprocess.Popen(["ollama", "serve"], start_new_session=True)
        else:
            subprocess.Popen(["ollama", "serve"], start_new_session=True)

        # Wait for service to start
        print("⏳ Waiting for Ollama service to start...")
        for i in range(30):  # Wait up to 30 seconds
            if check_ollama_installed():
                print("✅ Ollama service started successfully!")
                return True
            time.sleep(1)
            print(f"   {i+1}/30 seconds...")
        
        print("❌ Ollama service failed to start within 30 seconds")
        return False

    except Exception as e:
        print(f"❌ Error starting Ollama service: {e}")
        return False

def download_model(model_name="llama2"):
    """Download a model for Ollama."""
    print(f"📥 Downloading {model_name} model...")
    print("This may take several minutes depending on your internet connection...")

    try:
        response = requests.post(
            "http://localhost:11434/api/pull",
            json={"name": model_name},
            stream=True
        )

        if response.status_code == 200:
            print(f"✅ {model_name} model downloaded successfully!")
            return True
        else:
            print(f"❌ Failed to download {model_name} model")
            return False

    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def test_ollama():
    """Test Ollama with a simple query."""
    print("🧪 Testing Ollama...")

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama2",
                "prompt": "Hello, how are you?",
                "stream": False
            },
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            print("✅ Ollama is working correctly!")
            print(f"Response: {result.get('response', 'No response')[:100]}...")
            return True
        else:
            print("❌ Ollama test failed")
            return False

    except Exception as e:
        print(f"❌ Error testing Ollama: {e}")
        return False

def main():
    """Main setup function."""
    print("🤖 FitTrackAI - Ollama Setup (REQUIRED)")
    print("=" * 50)
    print("Ollama is REQUIRED for FitTrackAI to function.")
    print("This script will help you install and configure Ollama.")
    print()

    # Check if Ollama is already running
    if check_ollama_installed():
        print("✅ Ollama is already installed and running!")
        
        # Check if llama2 model is available
        try:
            response = requests.get("http://localhost:11434/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                if any("llama2" in model.get("name", "") for model in models):
                    print("✅ llama2 model is available!")
                    if test_ollama():
                        print("\n🎉 Setup complete! FitTrackAI is ready to use.")
                        print("\nTo use FitTrackAI:")
                        print("1. Make sure Ollama is running: ollama serve")
                        print("2. Start FitTrackAI: python start_app.py")
                        return True
                else:
                    print("⚠️ llama2 model not found. Downloading...")
                    if download_model("llama2"):
                        if test_ollama():
                            print("\n🎉 Setup complete! FitTrackAI is ready to use.")
                            return True
        except Exception as e:
            print(f"❌ Error checking models: {e}")
    else:
        print("❌ Ollama not found or not running.")

        # Try to install Ollama
        if install_ollama():
            print("✅ Ollama installed successfully!")
        else:
            print("❌ Please install Ollama manually from https://ollama.ai")
            return False

        # Start Ollama service
        if not start_ollama_service():
            print("❌ Could not start Ollama service. Please start it manually:")
            print("ollama serve")
            return False

    # Download model if needed
    model_name = input("Enter model name to download (default: llama2): ").strip() or "llama2"
    if download_model(model_name):
        # Test the model
        if test_ollama():
            print("\n🎉 Setup complete! FitTrackAI can now use Ollama for AI responses.")
            print("\nTo use FitTrackAI with Ollama:")
            print("1. Make sure Ollama is running: ollama serve")
            print("2. Start FitTrackAI: python start_app.py")
            print("3. The AI will automatically use Ollama for responses!")
            return True
        else:
            print("❌ Model test failed. Please check your Ollama installation.")
            return False
    else:
        print("❌ Failed to download model. Please try again.")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup failed. Please follow the manual installation steps:")
        print("1. Install Ollama: https://ollama.ai/download")
        print("2. Start Ollama: ollama serve")
        print("3. Download model: ollama pull llama2")
        sys.exit(1) 