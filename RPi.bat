@echo off

cd .\RPi\

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
start "Server" /B python .\RPiServer.py