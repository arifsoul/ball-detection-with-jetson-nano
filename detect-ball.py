import jetson.inference
import jetson.utils
import time
import threading
import serial
import socket
import sys


#ser0 = serial.Serial('/dev/ttyUSB0')
#ser1 = serial.Serial('/dev/ttyUSB0') 


net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)



s = socket.socket()
port = 3128

det0_X = "-1"
det0_Y = "-1"
det1_X = "-1"
det1_Y = "-1"

imu = "000"
sismin = "0#0#0#0"

def detection0():
	camera0 = jetson.utils.videoSource("/dev/video0") # camera 1
	display0 = jetson.utils.videoOutput("display://0") # display on camera 1
	global det0_X
	global det0_Y

	while display0.IsStreaming():
		img0 = camera0.Capture()
		detections = net.Detect(img0)

		det0_X = "-1"
		det0_Y = "-1"

		for detection in detections:
			coor = str(detection.Center)
			#print(coor)
		
			sp = coor.find(',')
			det0_X = coor[1:sp]
			det0_Y = coor[sp+2:-1]
	
		#print(det0_X)
		#print(det0_Y)

		display0.Render(img0)
		display0.SetStatus("MOBO-EVO Cam 0 - {:.0f} FPS".format(net.GetNetworkFPS())+"  X "+det0_X+"  Y "+det0_Y)

def detection1():
	camera1 = jetson.utils.videoSource("/dev/video1") # camera 2
	display1 = jetson.utils.videoOutput("display://1") # display on camera 2
	global det1_X
	global det1_Y
	while display1.IsStreaming():
		img1 = camera1.Capture()
		detections = net.Detect(img1)

		det1_X = "-1"
		det1_Y = "-1"

		for detection in detections:
			coor = str(detection.Center)
			#print(coor)
		
			sp = coor.find(',')
			det1_X = coor[1:sp]
			det1_Y = coor[sp+2:-1]
	
			#print(det1_X)
			#print(det1_Y)

		display1.Render(img1)
		display1.SetStatus("MOBO-EVO Cam 1 - {:.0f} FPS".format(net.GetNetworkFPS())+"  X "+det1_X+"  Y "+det1_Y)

def SerialMonitor():
	global imu
	global sismin

	imu = ser0.readline()
	sismin = ser0.readline()

	#data_sismin[] = sismin.split('#')

def ConServer():
	s.connect(('127.0.0.1', port))
	if s.connected == True:
		print("Server Connected")
		server_stat = True

	else:
		print("Server Disconnected")
		server_stat = False

def main():
	th0 = threading.Thread(target=detection0)
	th1 = threading.Thread(target=detection1)
	th2 = threading.Thread(target=SerialMonitor)
	th0.start()
	th1.start()


	while True:
		ConServer()

if __name__ == "__main__":
	main()