# mtc-ohbot-app

## Description
This is a sample application for the MTC OHBot.

## Pre-Requesites

**NOTE** You Need both versions of Python intlled to circumvent the antiquated OhBot libraries...

[Download python 3.11.0](https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe)

[Download python 3.6.4](https://www.python.org/downloads/release/python-364/)

[Microsoft Visual C++ 14+ Build Tools](https://aka.ms/vs/17/release/vs_BuildTools.exe)


## Configuration
1. Create a `.\env\local.env`
2. Set the contents as follows:
   
   `SPEECH_KEY=<Your Azure Speech Key>`
   
   `AOAI_KEY=<Your Open AI Key>`
   
   `OPENAI_ENDPOINT=<Your OpenAI EndPoint>`

   `MODEL=GPT35`
   
   `REGION=canadacentral`

   `RECOGNITION_LANGUAGE=en-CA`
   
   
## Installation
1. Clone the repository
2. Install dependencies with `.\install-dependencies.cmd`

## Usage
1. Run the application with `.\run-ohbot-app.cmd`

## Contributing
1. Fork the repository
2. Create a new branch with your feature or bug fix
3. Make changes and commit them
4. Push your changes to your fork
5. Submit a pull request to the original repository

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
