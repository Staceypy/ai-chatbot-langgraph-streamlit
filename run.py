import subprocess
import sys
import os
from multiprocessing import Process
import time
import webbrowser
import platform

def get_venv_activate_command():
    # Determine the correct activate script based on the OS
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "activate.bat")
    return f"source venv/bin/activate"

def run_backend():
    if platform.system() == "Windows":
        cmd = f'"{os.path.join("venv", "Scripts", "activate.bat")}" && python app.py'
        subprocess.run(cmd, shell=True)
    else:
        cmd = f'source venv/bin/activate && python app.py'
        subprocess.run(cmd, shell=True, executable='/bin/bash')

def run_frontend():
    # Small delay to ensure backend starts first
    time.sleep(2)
    if platform.system() == "Windows":
        cmd = f'"{os.path.join("venv", "Scripts", "activate.bat")}" && python -m streamlit run ui.py'
        subprocess.run(cmd, shell=True)
    else:
        cmd = f'source venv/bin/activate && python -m streamlit run ui.py'
        subprocess.run(cmd, shell=True, executable='/bin/bash')

def open_browser():
    # Small delay to ensure servers are up
    time.sleep(3)
    webbrowser.open('http://localhost:8501')  # Streamlit default port

if __name__ == "__main__":
    print("Starting the application...")
    
    # Start backend process
    backend = Process(target=run_backend)
    backend.start()
    print("Backend server starting on http://localhost:8000")
    
    # Start frontend process
    frontend = Process(target=run_frontend)
    frontend.start()
    print("Frontend server starting on http://localhost:8501")
    
    # Open browser automatically
    browser = Process(target=open_browser)
    browser.start()
    
    try:
        # Keep the main process running
        backend.join()
        frontend.join()
        browser.join()
    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        browser.terminate()
        backend.join()
        frontend.join()
        browser.join()
        print("Servers shut down successfully")
        sys.exit(0)