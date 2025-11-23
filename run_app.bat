@echo off
cd /d "%~dp0"
echo Starting EasyScrapePa...
..\venv\Scripts\python.exe -m streamlit run app.py
pause
