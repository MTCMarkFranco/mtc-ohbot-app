import os
import random
import azure.cognitiveservices.speech as speechsdk
import openai
from dotenv import load_dotenv
import time
import requests
import cv2
import dlib
import math

load_dotenv(dotenv_path=".\\ENV\\local.env")

# Globals
messages = []
engageWithPerson = False
look_counter = 0
start_time = None

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
def send_message_to_ohbot_service(text):
    try:
        url = "http://127.0.0.1:8000"
        headers = {"Content-Type": "text/html"}
        response = requests.post(url, headers=headers, data=text)
        response.raise_for_status()
        return True
    except Exception as ex:
        print(f"Error sending to Ohbot service: {ex}")
        return False
    
# Define the text-to-speech function
def send_gesture_to_ohbot_service(gesture):
    try:
        url = "http://127.0.0.1:8000/gesture"
        headers = {"Content-Type": "text/html"}
        response = requests.post(url, headers=headers, json=gesture)
        response.raise_for_status()
        return True
    except Exception as ex:
        print(f"Error sending to Ohbot service: {ex}")
        return False
 
def interact():
    
    #global start_time
    
    # Get input from user using speech-to-text
    user_input = speech_to_text()
    
    if user_input != "":
        #start_time =  None
        print(f"You said: {user_input}")

        # Generate a response using OpenAI
        prompt = f"Q: {user_input}\nA:"
        response = generate_text(prompt)
        #response = user_input
        print(f"AI said: {response}")

        # Convert the response to speech using text-to-speech
          
        gestureBlink = {
            "gesture": "blink",
            "velocity": 0.01
        }
        
        send_gesture_to_ohbot_service(gestureBlink)
        send_message_to_ohbot_service(response)
        
        
    # else:
    #     # if there are no questions within 20 seconds, start a new conversation 
    #     if start_time is None:
    #         start_time = time.time()
    #         print("Starting timer")    
        
    #     if time.time() - start_time >= 20:
    #         start_new_conversation()
    #         start_time = time.time()
            
        time.sleep(1)

def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = math.dist(eye[1], eye[5])
    B = math.dist(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = math.dist(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

def initalize_face_Detection():
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("recognition_models\\shape_predictor_68_face_landmarks.dat")
    captureDevice = cv2.VideoCapture(0)   
    
    return captureDevice, detector, predictor

def is_person_looking_at(captureDevice,detctor,predictor):
    
    global look_counter
    EYE_AR_THRESH = 0.15
        
    # Capture frame-by-frame
    ret, frame = captureDevice.read()

    # Convert the image to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = detctor(gray, 0)
    
    if len(faces) == 0:
        engageWithPerson = False
        look_counter = 0
    else:
        # Loop over the face detections
        for face in faces:
            # Determine the facial landmarks for the face region
            x1 = face.left()  # left point
            y1 = face.top()  # top point
            x2 = face.right()  # right point
            y2 = face.bottom()  # bottom point

            # Create landmark object
            landmarks = predictor(image=gray, box=face)
            
            # Initialize lists to hold eye coordinates
            left_eye = []
            right_eye = []

            # Loop through all the points
            for n in range(36, 42):  # Loop for left eye
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                left_eye.append((x, y))

            for n in range(42, 48):  # Loop for right eye
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                right_eye.append((x, y))

            # Calculate the Eye Aspect Ratio for both eyes
            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)

            # Average the eye aspect ratio together for both eyes
            ear = (leftEAR + rightEAR) / 2.0

            # If the eye aspect ratio is below a certain threshold, consider that the eyes are closed
            if ear < EYE_AR_THRESH:
                #print('The person is not looking at the camera')
                look_counter = 0
            else:
                #print('The person is looking at the camera')
                look_counter += 1

    # If the person has been looking at the camera for 5 seconds, set the flag
    if look_counter >= 2:
        return True, random.randint(1, 10), random.randint(1, 10)
    else:
        return False,random.randint(1, 10),random.randint(1, 10)
            
#  *****************************************************
#  ************** MAIN PROGRAM FLOW ********************
#  *****************************************************


# Initialize a new conversation
start_new_conversation()

# Initialize Cature device, face detector and facial landmark predictor
captureDevice, detector, predictor = initalize_face_Detection()

while True:
    
    # Check if there is a person looking at the camera(Ohbot) and get the coordinates of the person's face    
    isLookingAtMe, X,Y = is_person_looking_at(captureDevice, detector, predictor)

    # Keep head tracking continuously
    gestureLookAt = {
            "gesture": "lookAt",
            "head_coordinates": {
                "X": X,
                "Y": Y
            },
            "eye_coordinates": {
                "X": 5,
                "Y": 5
            },
            "velocity": 0.01
        }
    
    send_gesture_to_ohbot_service(gestureLookAt)
        
    # if the person is looking at the camera, conserate, new or existing....  
    if isLookingAtMe:
                 
        # If i am in a converation do not say hi and just continue conversation...
        if len(messages) == 1:
            print('New Conversation, Saying Hi!')
            send_message_to_ohbot_service("Hi there,  I am Art Vandelay, what is your name?")
        else:
            print('Conversation in Flight...')
        interact()
                
        
    else:
        print('Wipe out previous conversation, and voice to text will continue the next time someone looks at the ohbot(camera)')
        start_new_conversation()
        
    time.sleep(0.5)