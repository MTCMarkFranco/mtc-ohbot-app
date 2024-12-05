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
import sounddevice as sd
import numpy as np

# Globals
PORT = 8000
load_dotenv(dotenv_path="..\\local.env")

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("REGION")

# Initailise Ohbot
ohbot.reset()

# Move the HEADNOD motor to 9. 
ohbot.move(ohbot.HEADNOD,9)
# Move the HEADNOD motor to 5. 
ohbot.move(ohbot.HEADNOD,5)
# Set both eyes back to 5. 
ohbot.move(ohbot.EYETILT,8)

print("Initilizing OhBot...")
if (ohbot.connected == False):
    print("Ohbot Not connected!")
else:
    ohbot.setSynthesizer("sapi")
    ohbot.setVoice("-a100 -r10 -vZira")  # Adjusted pitch to a higher tone
    ohbot.wait(1)
    ohbot.say("I am ready for chatting!")

def narrow_range(num, min=0, max=10):
    if num <= max /2 - 1:
        return max /2 - 0.16
    elif num >= max /2 + 1:
        return max /2 + 0.16
    else:
        return max /2
    
def blink(velocity):
    for x in range(10,0,-1):
        ohbot.move(ohbot.LIDBLINK,x,eye = 0)
        ohbot.wait(velocity)

    for x in range(0,10):
        ohbot.move(ohbot.LIDBLINK,x,eye = 0)
        ohbot.wait(velocity)

def lookAt(HeadCoordinates,X,Y, velocity):
    ohbot.move(ohbot.HEADTURN,narrow_range(X * 10))
    ohbot.move(ohbot.HEADNOD,narrow_range(Y * 10))
    ohbot.move(ohbot.EYETURN, pos= X * 10,spd=velocity)
    ohbot.move(ohbot.EYETILT, pos= Y * 10,spd=velocity)

# print(sd.query_devices())

#async def move_lips():
    # def audio_callback(indata, frames, time, status):
    #     volume = float(np.linalg.norm(indata) / 10)
    #     ohbot.lipTopPos = (5 + (volume / 3))
    #     print("TOP: " + str(ohbot.lipTopPos))
    #     ohbot.lipBottomPos = (5 + (volume / 2))
    #     print("BOTTOM: " + str(ohbot.lipBottomPos))
    #     sleep(0.01)

    # Query the default output device
    # default_output_device = sd.default.device[1]
    # Set the device to the default output device
    # device = default_output_device
    
    # with sd.InputStream(callback=audio_callback, channels=1, samplerate=44100, device=device):
    #     while True:
    #         await asyncio.sleep(0.1)

# def start_lip_sync():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     loop.run_until_complete(move_lips())

# lip_sync_thread = threading.Thread(target=start_lip_sync)
# lip_sync_thread.start()

class MyHandler(http.server.SimpleHTTPRequestHandler):
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
                                                
                # Say it...
                ##############################################################################
                speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
                speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Changed to a voice with a higher pitch
                speech_config.speech_synthesis_language = "en-CA"  # Adjusted language to match the new voice

                audio_config = speechsdk.audio.AudioOutputConfig(filename=".\\ohbotData\\Sounds\\output.wav")
                synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
                
                result = synthesizer.speak_text_async(message).get()

                if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                    print("Speech synthesized to 'output.wav'")
                    
                    #ohbot.lipTopPos =  5 #5 + (ohbot.playSound("C:\Projects\new-oh-bot\mtc-ohbot-app\server\output.wav\output.wav")) /3
                    ohbot.playSound(untilDone=True, name= "output")

                    
                    # ohbot.playSound(name=".\output.wav",untilDone=True)
                    # need to find a way to play the wav file and move the lips to the wav file
                elif result.reason == speechsdk.ResultReason.Canceled:
                    cancellation_details = result.cancellation_details
                    print(f"Speech synthesis canceled: {cancellation_details.reason}")
                    if cancellation_details.reason == speechsdk.CancellationReason.Error:
                        print(f"Error details: {cancellation_details.error_details}")

                
                ##############################################################################
                #ohbot.say(message)
                #ohbot.sapivoice
                                
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

with socketserver.TCPServer(("127.0.0.1", PORT), MyHandler) as httpd:
    print("Ohbot is listening on port...", PORT)
    httpd.serve_forever()

