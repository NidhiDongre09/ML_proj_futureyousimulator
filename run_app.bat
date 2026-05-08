@echo off
cd /d "%~dp0"
"C:\Users\Nidhi Dongre\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m streamlit run app/app.py --server.port 8501 --server.headless true

