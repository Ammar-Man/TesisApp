@echo off

cd .\Linux\Flask\

if exist .venv\ (
    @REM Server found
    call .venv\Scripts\activate
) else (
    @REM Install server and dependencies
    echo Installing...
    python -m venv .venv
    call .venv\Scripts\activate
    pip install -r .\requirements.txt
)

@REM Start servers
echo Starting servers...
start "Camera" /B python .\Camera\Camera_expression.py
start "Server" /B python .\LinuxServer.py
start "Tablet" /B python .\Start_Tablet_html.py