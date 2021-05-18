
from http.server import HTTPServer, BaseHTTPRequestHandler
import time
import numpy as np
import pyaudio
import wave
import io
import json
import base64
import zlib

HOST_NAME='172.31.59.128'
PORT_NUMBER = 8895

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        
    def do_GET(self):
#         self.send_response(200)
#         self.end_headers()
#         self.wfile.write(b'Hello, from the server 8895!')

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Start Recording
        RESPEAKER_WIDTH = 2
        RESPEAKER_INDEX = 0
        RESPEAKER_CHANNELS = 6
        RESPEAKER_RATE = 16000
        CHUNK = 1024
        RECORD_SECONDS = 5
        
        p = pyaudio.PyAudio()
        
        stream = p.open(format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                rate=RESPEAKER_RATE,
                input=True,
                input_device_index=RESPEAKER_INDEX,
                frames_per_buffer=CHUNK)
        
        print ("recording")
        
        frames = []

        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            
            data = stream.read(CHUNK)
            data_array = np.fromstring(data, dtype=np.int16)
#             channel11 = data_array[0::RESPEAKER_CHANNELS]
#             channel12 = data_array[1::RESPEAKER_CHANNELS]
#             channel13 = data_array[2::RESPEAKER_CHANNELS]
#             channel14 = data_array[3::RESPEAKER_CHANNELS]
#             channel15 = data_array[4::RESPEAKER_CHANNELS]
#             channel16 = data_array[5::RESPEAKER_CHANNELS]
#             data = channel10.tostring()
            frames.append(data)
        

        print ("done recording")
        print(data_array.shape)
        
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Compressing using zlib and base64 (might be slower for big array's)
        data = zlib.compress(data_array)
        data = base64.b64encode(data)
        
        self.wfile.write(data)
#         print(data_array.shape)
              

httpd = HTTPServer((HOST_NAME, PORT_NUMBER), SimpleHTTPRequestHandler)
print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()
print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))



