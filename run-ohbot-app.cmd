@echo off
rem @echo killing existing processes
rem tskill cmd
rem timeout 10

@echo Starting Service...
start /MIN %USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe .\server\ohbot_service.py

timeout 20

@echo Starting App...
%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe .\app\ohbot_openai_app.py
