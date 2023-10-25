# Download python 3.11.0 https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
# Download python 3.6.4 (https://www.python.org/downloads/release/python-364/)
# https://aka.ms/vs/17/release/vs_BuildTools.exe

set PY311=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
set PY364=%USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe

%PY311% -m pip install --upgrade pip
%PY364% -m pip install --upgrade pip

%PY311% -m pip install azure-cognitiveservices-speech
%PY311% -m pip install yarl
%PY311% -m pip install frozenlist
%PY311% -m pip install aiohttp==3.8.2
%PY311% -m pip install openai
%PY311% -m pip install python-dotenv 
%PY311% -m pip install time
%PY311% -m pip install requests

%PY364% -m pip install http
%PY364% -m pip install socketserver
%PY364% -m pip install lxml
%PY364% -m pip install comtypes
%PY364% -m pip install ohbot