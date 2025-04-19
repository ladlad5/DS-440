@echo off
REM ──── Setup ───────────────────────────────────────────────────────────
REM Ensure we’re running from the folder where this script lives
cd /d %~dp0

REM Upgrade pip and install dependencies
python -m pip install --upgrade pip
python -m pip install flask flask-cors flask-ngrok requests pandas ollama streamlit

REM ──── 2) Check Ollama CLI ────────────────────────────────────────────
where ollama >nul 2>&1
IF ERRORLEVEL 1 (
  echo.
  echo ERROR: Ollama CLI not found in PATH.
  echo Please install it from https://ollama.com and restart this script.
  pause
  exit /b 1
)

REM ──── 3) Pull Deepseek model ─────────────────────────────────────────
echo Pulling deepseek-r1:1.5b (if not already present)...
ollama pull deepseek-r1:1.5b

REM ──── Launch Flask API (middlewaredeepseek) ───────────────────────────
start "Flask Server" cmd /k "python middlewaredeepseek.py"

REM ──── Launch Streamlit App (middlewareTest) ──────────────────────────
start "Streamlit App" cmd /k "python -m streamlit run middlewareTest.py --server.headless false --theme.base dark"

REM ──── Keep this window open ──────────────────────────────────────────
pause
