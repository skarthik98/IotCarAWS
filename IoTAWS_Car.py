from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import RPi.GPIO as GPIO

global direc
direc = " "
GPIO.setwarnings(False)
motor1_pin1 = 16
motor1_pin2 = 18
motor_enable1 = 22
motor2_pin1 = 19
motor2_pin2 = 21
motor_enable2 = 23
GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor1_pin1,GPIO.OUT)
GPIO.setup(motor1_pin2,GPIO.OUT)
GPIO.setup(motor2_pin1,GPIO.OUT)
GPIO.setup(motor2_pin2,GPIO.OUT)
GPIO.setup(motor_enable1,GPIO.OUT)
GPIO.setup(motor_enable2,GPIO.OUT)
print "hello"

#converts JSON message to python
def jsonCall(client, userdata, message):
	payload_json = json.loads(message.payload)
	global direc
	direc = payload_json["state"]["desired"]["Direction"]

#connects the thing to aws
host = "" #enter endpoint for thing
rootCAPath = "/home/pi/certificates/rootCA.pem"
certificatePath = "/home/pi/certificates/certificate.pem.crt"
privateKeyPath = "/home/pi/certificates/private.pem.key"
clientId = "RPI3"
topic = "$aws/things/iotthing/shadow/update/accepted" #enter specific iot thing name

myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureDrainingFrequency(2)  
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  

myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe(topic, 1, jsonCall)
time.sleep(2)
#commands and motor instructions for specific directions. Will continue
#to loop until program is stopped
try:	
	while True:
            if direc=='forward':
                            print("Going Forward")
                            GPIO.output(motor1_pin1,GPIO.HIGH)
                            GPIO.output(motor1_pin2,GPIO.LOW)
                            GPIO.output(motor_enable1,GPIO.HIGH)
                            GPIO.output(motor2_pin1,GPIO.LOW)
                            GPIO.output(motor2_pin2,GPIO.HIGH)
                            GPIO.output(motor_enable2,GPIO.HIGH)
                            time.sleep(0.5)
                            GPIO.output(motor_enable1,GPIO.LOW)
                            GPIO.output(motor_enable2,GPIO.LOW)
            elif direc=='backward':
                            print ("Going Backward")
                            GPIO.output(motor1_pin1,GPIO.LOW)
                            GPIO.output(motor1_pin2,GPIO.HIGH)
                            GPIO.output(motor_enable1,GPIO.HIGH)
                            GPIO.output(motor2_pin1,GPIO.HIGH)
                            GPIO.output(motor2_pin2,GPIO.LOW)
                            GPIO.output(motor_enable2,GPIO.HIGH)
                            time.sleep(0.5)
                            GPIO.output(motor_enable1,GPIO.LOW)
                            GPIO.output(motor_enable2,GPIO.LOW)
            elif direc=='right':
                            print ("Going Right")
                            GPIO.output(motor1_pin1,GPIO.HIGH)
                            GPIO.output(motor1_pin2,GPIO.LOW)
                            GPIO.output(motor_enable1,GPIO.HIGH)
                            GPIO.output(motor2_pin1,GPIO.HIGH)
                            GPIO.output(motor2_pin2,GPIO.LOW)
                            GPIO.output(motor_enable2,GPIO.HIGH)
                            time.sleep(0.3)
                            GPIO.output(motor_enable1,GPIO.LOW)
                            GPIO.output(motor_enable2,GPIO.LOW)
            elif direc=='left':
                
                            print ("Going Left")
                            GPIO.output(motor1_pin1,GPIO.LOW)
                            GPIO.output(motor1_pin2,GPIO.HIGH)
                            GPIO.output(motor_enable1,GPIO.HIGH)
                            GPIO.output(motor2_pin1,GPIO.LOW)
                            GPIO.output(motor2_pin2,GPIO.HIGH)
                            GPIO.output(motor_enable2,GPIO.HIGH)
                            time.sleep(0.3)
                            GPIO.output(motor_enable1,GPIO.LOW)
                            GPIO.output(motor_enable2,GPIO.LOW)
            direc = " "
            time.sleep(1)
#keyboard interrupt for motor loop
except KeyboardInterrupt:
		GPIO.cleanup()


