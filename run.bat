@echo off
echo Starting the Cybersecurity Knowledge Chatbot...

REM Start the FastAPI backend server
echo Starting FastAPI Backend...
start cmd /k "python -m uvicorn api:app --host 0.0.0.0 --port 8006 --reload"

REM Wait a moment for backend to initialize
timeout /t 3

REM Start the React frontend
echo Starting React Frontend...
cd frontend
start cmd /k "npm install && npm start"

echo Both services are starting. The app will be available at http://localhost:3000