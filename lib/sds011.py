import serial
import time

class SDS011(object):
    msg_start  = 170
    msg_cmd    = 192
    msg_end    = 171

    sleep_time = 0.01

    device_usb = serial.Serial('/dev/ttyUSB0', baudrate=9600, stopbits=1, parity="N",  timeout=2)
    device_ama = serial.Serial('/dev/ttyAMA0', baudrate=9600, stopbits=1, parity="N",  timeout=2)

    def __init__(self , usb):
        if usb:
            self.device = SDS011.device_usb
        else:
            self.device = SDS011.device_ama
    
    def read(self):

        # Read in loop until message start: AAC0
        while True:
            s = self.device.read(1)
            if ord(s) == msg_start:
                s = self.device.read(1)
                if ord(s) == msg_cmd:
                    break
            time.sleep( sleep_time )

        s = self.device.read(8)
                
        pm25hb = ord(s[0])
        pm25lb = ord(s[1])
        pm10hb = ord(s[2])
        pm10lb = ord(s[3])
        d5     = ord(s[4])
        d6     = ord(s[5])

        cs     = ord(s[6])
        tail   = ord(s[7]) 
        
        cs_expected = (pm25hb + pm25lb + pm10hb + pm10lb + d5 + d6) % 256
        if cs != cs_expected:
            raise Exception("Checksum test failed")

        pm25 = float(pm25hb + pm25lb*256)/10.0
        pm10 = float(pm10hb + pm10lb*256)/10.0
                
        return (pm10 , pm25)
