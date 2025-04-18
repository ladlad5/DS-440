@echo off
REM ──── Setup ───────────────────────────────────────────────────────────
REM Ensure we’re running from the folder where this script lives
cd /d %~dp0

REM Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install flask flask-cors flask-ngrok requests pandas ollama streamlit

REM ──── Launch Flask API (middlewaredeepseek) ───────────────────────────
start "Flask Server" cmd /k "python middlewaredeepseek.py"

REM ──── Launch Streamlit App (middlewareTest) ──────────────────────────
start "Streamlit App" cmd /k "python -m streamlit run middlewareTest.py --server.headless false"

REM ──── Keep this window open ──────────────────────────────────────────
pause
