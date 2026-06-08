$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

& "$ProjectRoot\.venv\Scripts\python.exe" -m streamlit run app.py `
    --server.port 8501 `
    --server.headless true `
    --server.runOnSave false `
    --browser.gatherUsageStats false
