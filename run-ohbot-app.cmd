@echo off
@REM @echo Starting Service...
@REM start %USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe .\server\ohbot_service.py

@REM timeout 10

@echo Starting App...
start %USERPROFILE%\AppData\Local\Programs\Python\Python312\python.exe .\app\ohbot_openai_app.py
