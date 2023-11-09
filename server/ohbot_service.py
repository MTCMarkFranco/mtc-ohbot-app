import http.server
import socketserver
import json
from ohbot import ohbot

# Globals
PORT = 8000

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
    ohbot.setVoice("-a100 -r0 -vZira")
    ohbot.wait(1)

def blink(velocity):
    for x in range(10,0,-1):
        ohbot.move(ohbot.LIDBLINK,x,eye = 0)
        ohbot.wait(velocity)

    for x in range(0,10):
        ohbot.move(ohbot.LIDBLINK,x,eye = 0)
        ohbot.wait(velocity)

def lookAt(coordinates, velocity):
    ohbot.move(ohbot.HEADTURN,coordinates['X'])
    ohbot.move(ohbot.HEADNOD,coordinates['Y'])
    ohbot.move(ohbot.EYETURN, pos= coordinates['X'],spd=velocity)
    ohbot.move(ohbot.EYETILT, pos= coordinates['Y'],spd=velocity)
    
    
        
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
                ohbot.say(message)
                                
            except Exception as ex:
                print(f"Error: {ex.line_no}")
                self.send_response(500)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Error")
                return            
    
    def handle_gesture(self):
            
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                gesture = json.loads(body.decode('utf-8'))
                print(f"Gesture: {gesture['gesture']}")
                print(f"Coordinates: {gesture['coordinates']}")
                print(f"Velocity: {gesture['velocity']}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Received your message")
                
                if gesture['gesture'] == "blink":
                   blink(gesture['velocity'])
                   
                if gesture['gesture'] == "lookAt":
                   lookAt(gesture['coordinates'], gesture['velocity'])
                                
                                
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

   