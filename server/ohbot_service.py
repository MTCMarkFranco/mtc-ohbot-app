import http.server
import socketserver
import json
from ohbot import ohbot
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
from time import sleep
import asyncio
import threading
import pyaudiowpatch as pyaudio
import numpy as np
import random
import time

# Globals
PORT = 8000
load_dotenv(dotenv_path="..\\local.env")

#initialize lip_synch Thread Object
lip_synch_thread = None

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("REGION")

# Constants for audio listener
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
CHANNELS = 1  # Mono audio

# Initailise Ohbot
ohbot.reset()

# Move the HEADNOD motor to 9. 
ohbot.move(ohbot.HEADNOD,9)
# Move the HEADNOD motor to 5. 
ohbot.move(ohbot.HEADNOD,5)
# Set both eyes back to 5. 
ohbot.move(ohbot.EYETILT,8)

ohbot.move(ohbot.BOTTOMLIP, 5)
ohbot.move(ohbot.TOPLIP, 5)


print("Initilizing OhBot...")
if (ohbot.connected == False):
    print("Ohbot Not connected!")
    exit()
else:
    ohbot.setSynthesizer("sapi")
    ohbot.setVoice("-a100 -r0 -vZira")  # Adjusted rate to normal speed
    ohbot.wait(1)
    ohbot.say("I am ready for chatting!")

def narrow_range(num, min=0, max=10):
    # Map the input range [0, 10] to the output range [4, 6]
    return round(abs(4 + (num / (max - min)) * (6 - 4)))

def blink(velocity):
    for x in range(10,0,-1):
        ohbot.move(ohbot.LIDBLINK,x,eye = 0)
        ohbot.wait(velocity)

    for x in range(0,10):
        ohbot.move(ohbot.LIDBLINK,x,eye = 0)
        ohbot.wait(velocity)

def blink_randomly():
    while True:
        # Generate a random delay between 3 and 10 seconds
        delay = random.uniform(1, 10)
        time.sleep(delay)
        blink(0.01)

def lookAt(HeadCoordinates,X,Y, velocity):
    
    print (f"New pos(X): {X}")
    ohbot.move(ohbot.HEADTURN,narrow_range(round(X * 10)))
    ohbot.move(ohbot.HEADNOD,narrow_range(round(Y * 10)))
    ohbot.move(ohbot.EYETURN, pos= narrow_range(round(X * 10)),spd=velocity)
    ohbot.move(ohbot.EYETILT, pos= narrow_range(round(Y * 10)),spd=velocity)

def get_rms(audio_data):
    # Convert audio data to numpy array
    samples = np.frombuffer(audio_data, dtype=np.int16)
    # Calculate RMS
    rms = np.sqrt(np.mean(samples**2))
    return rms

# create an thread to ruun in the background called LipSynch
def LipSynch():
    with pyaudio.PyAudio() as p:
        device_index = -1
        sample_rate = -1
        device_name = ""
       
        # loopback audio device
        for loopback in p.get_loopback_device_info_generator():
            print(f"{loopback}\r")
            print ("Success, loopback device was found!")
            device_index = loopback.get('index')
            sample_rate = (int)(loopback.get('defaultSampleRate'))
            device_name = loopback.get('name')

        if (device_index < 0):
            print ("Sorry, no loopback device was found")
            p.terminate()
            exit()
            
        # Open audio stream
        stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=sample_rate,
                    input=True,
                    input_device_index=device_index,
                    frames_per_buffer=CHUNK)

        print("Monitoring audio... press ctrl C to stop")

        try:
            while True:
                # Read a chunk of data from the stream
                data = stream.read(CHUNK)
                # Get the RMS value
                rms = get_rms(data)
                # Print the audio level.  Uncomment this to see the audio levels
                # print(f"Audio Level: {rms:.2f}")
                # Move Ohbot's lips.  You may need to adjust this if the lips
                # are moving too much or too little
                if (not np.isnan(rms)):
                    level = int(rms / 10)
                    if(level > 0):
                        ohbot.move(ohbot.TOPLIP, 5 + level / 3)
                        ohbot.move(ohbot.BOTTOMLIP, 5 + level)
                    else:
                        ohbot.move(ohbot.TOPLIP, 5)
                        ohbot.move(ohbot.BOTTOMLIP, 5)

        except KeyboardInterrupt:
            print("Stopped Listening Rendered Audio....")

        # Close the stream and clean up
        ohbot.close()
        stream.stop_stream()
        stream.close()
        p.terminate()

# Run background threads
lip_synch_thread = threading.Thread(target=LipSynch)
lip_synch_thread.daemon = True
lip_synch_thread.start()

blink_thread = threading.Thread(target=blink_randomly)
blink_thread.daemon = True
blink_thread.start()

# Continue execution below
class ohbotHttpServer(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
            
            path = self.path

            if path == '/gesture':
                self.handle_gesture()
                return
            
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                message = body.decode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Received your message")
                                                
                speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
                speech_config.speech_synthesis_voice_name = "en-US-CoraMultilingualNeural"  # Changed to a voice with a higher pitch
                speech_config.speech_synthesis_language = "en-CA"  # Adjusted language to match the new voice

                audio_config = speechsdk.audio.AudioOutputConfig(filename=".\\ohbotData\\Sounds\\output.wav")
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
                
                result = synthesizer.speak_text_async(message).get()

                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    print("Speech synthesized to 'output.wav'")
                    ohbot.playSound(untilDone=True, name= "output")

                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    print(f"Speech synthesis canceled: {cancellation_details.reason}")
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print(f"Error details: {cancellation_details.error_details}")
                                
            except Exception as ex:
                print(f"Error: {ex.line_no}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Error")
                return            
    
    def handle_gesture(self):
            
            x = 0.5
            y = 0.5
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                gesture = json.loads(body.decode('utf-8'))
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Received your message")
                
                if gesture['gesture'] == "blink":
                   blink(gesture['velocity'])
                   
                if gesture['gesture'] == "lookAt":
                                if x != gesture['eye_coordinates']["X"] or y != gesture['eye_coordinates']["Y"]: 
                                                x = gesture['eye_coordinates']["X"]
                                                y = gesture['eye_coordinates']["Y"]
                                                lookAt(gesture['head_coordinates'],x,y, gesture['velocity'])
                                
                                
            except Exception as ex:
                print(f"Error: {ex.line_no}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Error")
                return            

with socketserver.TCPServer(("127.0.0.1", PORT), ohbotHttpServer) as httpd:
    print("Ohbot is listening on port...", PORT)
    httpd.serve_forever()

