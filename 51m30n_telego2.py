#version polling
import RPi.GPIO as GPIO
import OSC
import time
import threading
import socket


#Configuration OSCclient = OSC.OSCClient()
client = OSC.OSCClient()
msg = OSC.OSCMessage()
msg.setAddress("/gpio")
#IP = '192.168.1.100'
IP = '127.0.0.1'# cible
Port = 8889
value = 0
i = 0
print('IP = {IP} Port = {Port}').format(IP=IP, Port=Port)


#envoir un mess OSC a chaqie interruption
def read_and_send():
    for channel in range (0, 27):
        time.sleep(.0001)
        if GPIO.event_detected(channel):
            value = GPIO.input(channel)
#            print 'GPIO {channel} a {value}'.format(channel=channel, value=value)
            msg.append([channel, value])
            client.sendto(msg, (IP, Port))
            msg.clearData()
            
############################################################

#def check_IP():
#    temp = False
#    ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
#   while temp == False:
#        if ip == ('127.0.0.1' or '127.0.1.1' or '0.0.0.0'):
#            print('Wait for Network {ip}').format(ip=ip)
#            time.sleep(5)
#        else:
#            temp = True
#            print('ip = {ip}').format(ip=ip)
#    return ip
############################################################

#Configuration GPIO

#msg.append([check_IP(), IP, Port])
#client.sendto(msg, (IP, Port))
#msg.clearData()
#msg.setAddress("/gpio")

for channel in range (0,27):
    print('GPIO {channel} IN with pull_up resistor').format(channel=channel)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    channel += 1
    
time.sleep(3)

#edition des evenement
for channel in range (0, 27):
    GPIO.add_event_detect(channel, GPIO.BOTH)

#main
try:
    while True:
        read_and_send()
        time.sleep(0.02) #duree de l'antirebonds
except KeyboardInterrupt:
    exit()
