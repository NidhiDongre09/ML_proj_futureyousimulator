$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = "C:\Users\Nidhi Dongre\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$LogPath = Join-Path $ProjectRoot "streamlit.log"

Set-Location -LiteralPath $ProjectRoot
& $Python -m streamlit run app/app.py --server.port 8501 --server.headless true *> $LogPath
