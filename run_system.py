import subprocess
import sys
import time

print("Starting Retail AI System...")

# Vision Engine
vision = subprocess.Popen(
    [sys.executable, "main.py"]
)

time.sleep(3)

# FastAPI
backend = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "backend:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000"
    ]
)

time.sleep(3)

# Chat Agent
chat = subprocess.Popen(
    [sys.executable, "chat_agent.py"]
)

print("System Started Successfully.")

try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:

    print("\nStopping system...")

    vision.terminate()
    backend.terminate()
    chat.terminate()

    print("System stopped.")