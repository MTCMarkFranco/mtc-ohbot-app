import os
import azure.cognitiveservices.speech as speechsdk
import openai
from dotenv import load_dotenv
import time
import requests

load_dotenv(dotenv_path=".\\ENV\\local.env")

# Globals
messages = []

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_ENDPOINT")
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("AOAI_KEY")
# Set up engine name
engine_name = os.getenv("MODEL")

# Set up Azure Speech-to-Text and Text-to-Speech credentials
speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("REGION")
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Set up Azure Text-to-Speech language 
speech_config.speech_synthesis_language = os.getenv("RECOGNITION_LANGUAGE")
# Set up Azure Speech-to-Text language recognition
speech_config.speech_recognition_language = os.getenv("RECOGNITION_LANGUAGE")

# Set up the voice configuration
speech_config.speech_synthesis_voice_name = "en-CA-ClaraNeural"
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# start a new conversation context
def start_new_conversation():
    global messages
     
    messages.clear()
    # setup the messages and system prompt List defaults
    Instruction =   "You are a friendly person, looking to have friendly dialogue with whoever you speak with. " \
                    "You will answer questionsand ask questions. " \
                    "You will not be rude or mean. " \
                    "You will not use profanity. " \
                    "You will not be racist or sexist. " \
                    "Please be friendly and have a good conversation. " \
                    "add some humour to your responses including some laughing text in the form of 'hahaha' in the form of text, no emojis. " \
                    "Only return responses that can be converted safely to UTF-8 format. " \
                    "Your name is Art vandelay." \
                    "if not provided, you should ask for their name before giving a response. " \
                    "start off every response with the person's name. " \
                    "if you didn't understand the question or were given a partial sentence, response with 'I didn't quite get that, please try again.' " \
                    "try to make small talk if there isn't a direct question being asked" \
                    "Your first response back to the user should be 'Hi There, what is your name?'"

    messages=[
                {
                    "role": "system", 
                    "content": Instruction
                }
        ]
    print("Starting a new conversation")

# Define the speech-to-text function
def speech_to_text():
    # Set up the audio configuration
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create a speech recognizer and start the recognition
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    print("Your turn to speak...")

    result = speech_recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        return ""
    elif result.reason == speechsdk.ResultReason.Canceled:
        return ""

# Define the text-to-speech function
# def text_to_speech(text):
#     try:
#         result = speech_synthesizer.speak_text_async(text).get()
#         if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
#             print("Text-to-speech conversion successful.")
#             return True
#         else:
#             print(f"Error synthesizing audio: {result}")
#             return False
#     except Exception as ex:
#         print(f"Error synthesizing audio: {ex}")
#         return False

# Define the Azure OpenAI language generation function
def generate_text(prompt):
   
   global messages
    
   messages.insert(messages.__len__(), 
                    {
                        "role": "user", 
                        "content": prompt
                    })
   
   
   response = openai.ChatCompletion.create(
        engine=engine_name,
        messages=messages,
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
      
   messages.insert(messages.__len__(), 
                    {
                        "role": "assistant", 
                        "content": response['choices'][0]['message']['content']
                    })
    

   return response['choices'][0]['message']['content']

# Define the text-to-speech function
def send_to_ohbot_service(text):
    try:
        url = "http://127.0.0.1:8000"
        headers = {"Content-Type": "text/html"}
        response = requests.post(url, headers=headers, data=text)
        response.raise_for_status()
        return True
    except Exception as ex:
        print(f"Error sending to Ohbot service: {ex}")
        return False
    

#  *****************************************************
#  ************** MAIN PROGRAM FLOW ********************
#  *****************************************************

# Initialize the start time
start_time = None

# Initialize a new conversation
start_new_conversation()

# Main program loop
while True:
    # Get input from user using speech-to-text
    user_input = speech_to_text()
    
    if user_input != "":
        start_time =  None
        print(f"You said: {user_input}")

        # Generate a response using OpenAI
        prompt = f"Q: {user_input}\nA:"
        response = generate_text(prompt)
        #response = user_input
        print(f"AI said: {response}")

        # Convert the response to speech using text-to-speech
        send_to_ohbot_service(response)
        
    else:
        # if there are no questions within 1 minute, start a new conversation 
        if start_time is None:
            start_time = time.time()
            print("Starting timer")    
        
        if time.time() - start_time >= 20:
            start_new_conversation()
            start_time = time.time()
            
        time.sleep(1)
        