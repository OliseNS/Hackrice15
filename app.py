#!/usr/bin/env python3
"""
Simple Flask app that serves index.html and starts camserve
"""

from flask import Flask, render_template
import subprocess
import sys
import os

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Global variable to track camera server process
camera_process = None

def start_camera_server():
    """Start the camera server in a separate process"""
    global camera_process
    
    try:
        print("🔄 Starting camera server...")
        
        # Start camera server process
        camera_process = subprocess.Popen([
            sys.executable, 
            os.path.join(os.path.dirname(__file__), 'camserve', 'camserve.py')
        ])
        
        print("✅ Camera server started successfully")
        print("📡 MJPEG stream available at: http://localhost:5001/stream")
        return True
            
    except Exception as e:
        print(f"❌ Error starting camera server: {e}")
        return False

def stop_camera_server():
    """Stop the camera server process"""
    global camera_process
    
    if camera_process:
        try:
            print("🛑 Stopping camera server...")
            camera_process.terminate()
            camera_process.wait(timeout=5)
            print("✅ Camera server stopped")
        except subprocess.TimeoutExpired:
            print("⚠️ Camera server didn't stop gracefully, forcing...")
            camera_process.kill()
        except Exception as e:
            print(f"❌ Error stopping camera server: {e}")
        finally:
            camera_process = None

@app.route('/')
def index():
    """Serve the dashboard page"""
    return render_template('index.html')

if __name__ == '__main__':
    print("🚀 Starting Aegis AI application...")
    print("📊 Dashboard available at: http://localhost:5000/")
    print("📦 Packages available at: http://localhost:5000/packages")
    
    # Auto-start camera server
    if start_camera_server():
        print("✅ Camera server started automatically")
    else:
        print("⚠️ Failed to start camera server automatically")
        print("📡 You can start it manually: python camserve/camserve.py")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down application...")
        stop_camera_server()
    except Exception as e:
        print(f"❌ Error: {e}")
        stop_camera_server()
