import http.server
import socketserver
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

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
            
            try:
                content_length = int(self.headers['Content-Length'])
                body = self.rfile.read(content_length)
                message = body.decode('utf-8')
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"Received your message")
                
                # Blink
                for x in range(10,0,-1):
                    ohbot.move(ohbot.LIDBLINK,x,eye = 0)
                    ohbot.wait(0.01)

                for x in range(0,10):
                    ohbot.move(ohbot.LIDBLINK,x,eye = 0)
                    ohbot.wait(0.01)
                
                # Say it...
                ohbot.say(message)
                                
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

   