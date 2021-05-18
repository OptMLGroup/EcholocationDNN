import cv2
import imageio
import pyrealsense2 as rs
import os
import shutil
import datetime
import pyaudio
import http.client
import io
import numpy as np
import json
import zlib
import base64
import datetime
import threading
import wave
import pygame as pg
import time

class CollectData:
	def __init__(self):
		self.dct = {'a':0, 'b':0}
        
	def woofer(self):
		pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
		sound1 = pg.mixer.Sound('sub_woofer_3.wav')
		channel1 = sound1.play()
		channel1.set_volume(0.9, 0.0)
        
	def camera(self, fileprefix):

		pipeline = rs.pipeline()

		config = rs.config()
		config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
		config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

		profile = pipeline.start(config)

		depth_sensor = profile.get_device().first_depth_sensor()
		depth_sensor.set_option(rs.option.visual_preset, 3)  # Set high accuracy for depth sensor
		depth_scale = depth_sensor.get_depth_scale()

		clipping_distance_in_meters = 1
		clipping_distance = clipping_distance_in_meters / depth_scale

		align_to = rs.stream.color
		align = rs.align(align_to)

		try:
			frames = pipeline.wait_for_frames()
			aligned_frames = align.process(frames)
			aligned_depth_frame = aligned_frames.get_depth_frame()
			color_frame = aligned_frames.get_color_frame()

			if not aligned_depth_frame or not color_frame:
				raise RuntimeError("Could not acquire depth or color frames.")

			depth_image = np.asanyarray(aligned_depth_frame.get_data())
			color_image = np.asanyarray(color_frame.get_data())

			grey_color = 153
			depth_image_3d = np.dstack(
				(depth_image, depth_image, depth_image)
			)  # Depth image is 1 channel, color is 3 channels
			bg_removed = np.where(
				(depth_image_3d > clipping_distance) | (depth_image_3d <= 0),
				grey_color,
				color_image,
			)

			color_image = color_image[..., ::-1]
			
# 			depth_path = '../Sample_8/Images/Depth/%s.png' % fileprefix
			rgb_path = '../Sample_9/Images/%s.png' % fileprefix

# 			imageio.imwrite(depth_path, depth_image)
			imageio.imwrite(rgb_path, color_image)
			

		finally:
			pipeline.stop()

		#return color_image, depth_image
    
	def emitsound(self):
        
		time.sleep(1)        
      
		pg.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
		sound0 = pg.mixer.Sound('emit_sound_single_frequency.wav')
		channel0 = sound0.play()
		channel0.set_volume(0.0, 1.0)
        
		self.dct['a'] = datetime.datetime.now()  
# 		print("Emit Sound is running at : ", datetime.datetime.now())

	def recording(self,fileprefix):
                
# 		print("Recording function is running at ", datetime.datetime.now())
		
# 		The server file will be running on respeaker which should be pinged from here 
# 		and return us the audio ouput of 6 arrays. Modifiy the client and server file
		
		BODY = "***filecontents***"
		conn = http.client.HTTPConnection('172.31.37.131', 8882)
		conn.request("GET", "/file")
		response = conn.getresponse()
		print(response.status, response.reason)
		
		data = response.read()
		data2 = base64.b64decode(data)
		data2 = zlib.decompress(data2)
		fdata = np.frombuffer(data2, dtype=np.int16)
		
		with open('../Sample_9/Recording/%s.npy' % fileprefix, 'wb') as f:
			np.save(f, fdata)
            
		self.dct['b'] = datetime.datetime.now()

	def simul_thread(self, fileprefix):


		thread_lst = []

		t0 = threading.Thread(target=self.recording, args=(fileprefix,))
		thread_lst.append(t0)
		t0.start()

		t1 = threading.Thread(target=self.emitsound)
		thread_lst.append(t1)
		t1.start()

		for thread in thread_lst:
			thread.join()
        
        
