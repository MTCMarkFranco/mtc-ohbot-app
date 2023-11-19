# Download python 3.11.0 https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
# Download python 3.6.4 (https://www.python.org/downloads/release/python-364/)
# https://aka.ms/vs/17/release/vs_BuildTools.exe

set PY311=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
set PY364=%USERPROFILE%\AppData\Local\Programs\Python\Python36\python.exe

%PY311% -m pip install --upgrade pip
%PY364% -m pip install --upgrade pip

@echo 3.11.0 Libraries

%PY311% -m pip install aiofiles==23.2.1
%PY311% -m pip install aiohttp==3.9.0b0
%PY311% -m pip install aiosignal==1.3.1
%PY311% -m pip install amqp==5.1.1
%PY311% -m pip install anyio==3.7.1
%PY311% -m pip install asgiref==3.7.2
%PY311% -m pip install asyncio==3.4.3
%PY311% -m pip install attrs==23.1.0
%PY311% -m pip install azure-cognitiveservices-speech==1.32.1
%PY311% -m pip install azure-cognitiveservices-vision-computervision==0.9.0
%PY311% -m pip install azure-common==1.1.28
%PY311% -m pip install azure-core==1.29.5
%PY311% -m pip install billiard==4.1.0
%PY311% -m pip install blinker==1.6.3
%PY311% -m pip install celery==5.3.4
%PY311% -m pip install certifi==2023.7.22
%PY311% -m pip install chardet==5.2.0
%PY311% -m pip install charset-normalizer==3.3.0
%PY311% -m pip install click-didyoumean==0.3.0
%PY311% -m pip install click-plugins==1.1.1
%PY311% -m pip install click-repl==0.3.0
%PY311% -m pip install click==8.1.7
%PY311% -m pip install colorama==0.4.6
%PY311% -m pip install comtypes==1.2.0
%PY311% -m pip install distro==1.8.0
%PY311% -m pip install dlib==19.24.2
%PY311% -m pip install flask==3.0.0
%PY311% -m pip install frozenlist==1.4.0
%PY311% -m pip install future==0.18.3
%PY311% -m pip install github==1.2.7
%PY311% -m pip install h11==0.14.0
%PY311% -m pip install httpcore==1.0.2
%PY311% -m pip install httpx==0.25.1
%PY311% -m pip install idna==3.4
%PY311% -m pip install iso8601==2.1.0
%PY311% -m pip install isodate==0.6.1
%PY311% -m pip install itsdangerous==2.1.2
%PY311% -m pip install jinja2==3.1.2
%PY311% -m pip install jsonschema-spec==0.2.4
%PY311% -m pip install jsonschema-specifications==2023.7.1
%PY311% -m pip install jsonschema==4.19.1
%PY311% -m pip install keyboard==0.13.5
%PY311% -m pip install kombu==5.3.2
%PY311% -m pip install lazy-object-proxy==1.9.0
%PY311% -m pip install markupsafe==2.1.3
%PY311% -m pip install more-itertools==10.1.0
%PY311% -m pip install msrest==0.7.1
%PY311% -m pip install multidict==6.0.4
%PY311% -m pip install numpy==1.26.1
%PY311% -m pip install oauthlib==3.2.2
%PY311% -m pip install openai --upgrade
%PY311% -m pip install openapi-core --upgrade
%PY311% -m pip install openapi-schema-validator --upgrade
%PY311% -m pip install openapi-spec-validator --upgrade
%PY311% -m pip install packaging==23.2
%PY311% -m pip install parse==1.19.1
%PY311% -m pip install pathable==0.4.3
%PY311% -m pip install pip==23.3.1
%PY311% -m pip install prance==23.6.21.0
%PY311% -m pip install prompt-toolkit==3.0.39
%PY311% -m pip install psutil==5.9.6
%PY311% -m pip install pycaw==20230407
%PY311% -m pip install pydantic==1.10.13
%PY311% -m pip install pygame==2.5.2
%PY311% -m pip install pyqt5-qt5==5.15.2
%PY311% -m pip install pyqt5-sip==12.13.0
%PY311% -m pip install pyqt5==5.15.10
%PY311% -m pip install python-dateutil==2.8.2
%PY311% -m pip install python-dotenv==1.0.0
%PY311% -m pip install pyyaml==6.0.1
%PY311% -m pip install referencing==0.30.2
%PY311% -m pip install regex==2023.10.3
%PY311% -m pip install requests-oauthlib==1.3.1
%PY311% -m pip install requests==2.31.0
%PY311% -m pip install rfc3339-validator==0.1.4
%PY311% -m pip install rpds-py==0.10.6
%PY311% -m pip install ruamel.yaml.clib==0.2.8
%PY311% -m pip install ruamel.yaml==0.18.0
%PY311% -m pip install semantic-kernel==0.3.13.dev0
%PY311% -m pip install serial==0.0.97
%PY311% -m pip install setuptools==68.2.2
%PY311% -m pip install six==1.16.0
%PY311% -m pip install sniffio==1.3.0
%PY311% -m pip install tqdm==4.66.1
%PY311% -m pip install typing-extensions==4.8.0
%PY311% -m pip install typing==3.7.4.3
%PY311% -m pip install tzdata==2023.3
%PY311% -m pip install urllib3==2.0.7
%PY311% -m pip install vine==5.0.0
%PY311% -m pip install wcwidth==0.2.8
%PY311% -m pip install werkzeug==3.0.0
%PY311% -m pip install yarl==1.9.2 


@echo 3.6.4 Libraries
azure-cognitiveservices-speech==1.19.0
%PY364% -m pip install azure-common==1.1.28
%PY364% -m pip install azure-core==1.24.2
%PY364% -m pip install certifi==2023.7.22
%PY364% -m pip install charset-normalizer==2.0.12
%PY364% -m pip install click==8.0.4
%PY364% -m pip install colorama==0.4.5
%PY364% -m pip install comtypes==1.2.0
%PY364% -m pip install dataclasses==0.8
%PY364% -m pip install distlib==0.3.7
%PY364% -m pip install dlib==19.24.2
%PY364% -m pip install filelock==3.4.1
%PY364% -m pip install flask==2.0.3
%PY364% -m pip install gtts==2.2.4
%PY364% -m pip install idna==3.4
%PY364% -m pip install importlib-metadata==4.8.3
%PY364% -m pip install importlib-resources==5.4.0
%PY364% -m pip install isodate==0.6.1
%PY364% -m pip install itsdangerous==2.0.1
%PY364% -m pip install jinja2==3.0.3
%PY364% -m pip install lxml==4.9.3
%PY364% -m pip install markupsafe==2.0.1
%PY364% -m pip install msrest==0.7.1
%PY364% -m pip install numpy==1.19.5
%PY364% -m pip install oauthlib==3.2.2
%PY364% -m pip install ohbot==4.0.8
%PY364% -m pip install pip==21.3.1
%PY364% -m pip install platformdirs==2.4.0
%PY364% -m pip install playsound==1.3.0
%PY364% -m pip install pydub==0.25.1
%PY364% -m pip install pyserial==3.5
%PY364% -m pip install python-dotenv==0.20.0
%PY364% -m pip install requests-oauthlib==1.3.1
%PY364% -m pip install requests==2.27.1
%PY364% -m pip install setuptools==40.6.2
%PY364% -m pip install simpleaudio==1.0.4
%PY364% -m pip install six==1.16.0
%PY364% -m pip install touch==2020.12.3
%PY364% -m pip install typing-extensions==4.1.1
%PY364% -m pip install urllib3==1.26.17
%PY364% -m pip install values==2020.12.3
%PY364% -m pip install virtualenv==20.17.1
%PY364% -m pip install werkzeug==2.0.3
%PY364% -m pip install zipp==3.6.0
