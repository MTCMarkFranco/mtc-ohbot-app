@echo off
@echo Starting Service...
start %USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe .\server\ohbot_service.py

timeout 10

@echo Starting App...
start %USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe .\app\ohbot_openai_app.py
