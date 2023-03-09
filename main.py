from machine import UART, Pin, I2C
import time
import re
from esp8266 import ESP8266
from Elink import EPD_2in9

esp01 = ESP8266()
esp8266_at_ver = None
led=Pin(25,Pin.OUT)
# led = Pin("LED", Pin.OUT)
print("StartUP",esp01.startUP())
#print("ReStart",esp01.reStart())
print("StartUP",esp01.startUP())
print("Echo-Off",esp01.echoING())
print("\r\n\r\n")
'''
Print ESP8266 AT command version and SDK details
'''
esp8266_at_var = esp01.getVersion()
if(esp8266_at_var != None):
    print(esp8266_at_var)
'''
set the current WiFi in SoftAP+STA
'''
esp01.setCurrentWiFiMode()
#apList = esp01.getAvailableAPs()
#for items in apList:
#    print(items)
    #for item in tuple(items):
    #    print(item)
print("\r\n\r\n")
'''
Connect with the WiFi
'''
print("Try to connect with the WiFi..")

button = Pin(14, Pin.IN, Pin.PULL_DOWN)

while (1):
    if "WIFI CONNECTED" in esp01.connectWiFi("MGTS_GPON5_Nf9A","MdhG3pMW"):
        print("ESP8266 connect with the WiFi..")
        break;
    else:
        print(".")
        time.sleep(2)
print("\r\n\r\n")
print("Now it's time to start HTTP Get/Post Operation.......\r\n")
while(1):
    if button.value():
        led.toggle()
        httpCode, httpRes = esp01.doHttpGet("192.168.1.10","/add","RaspberryPi-Pico", port=5000)
        print(httpRes)
        pattern = r"k=(\d+)&n=(\d+)"

        match = re.search(pattern, httpRes)
        if match:
            k = int(match.group(1))
            n = int(match.group(2))
            print("k =", k)
            print("n =", n)

        epd = EPD_2in9()
        epd.Clear(0xff)

        epd.fill(0xff)
        epd.text("User added", 5, 10, 0x00)
        epd.text("to queue !", 5, 40, 0x00)
        epd.text("Your id - " + str(k), 5, 70, 0x00)
        epd.text("Position - " + str(n), 5, 100, 0x00)

        epd.rect(10, 180, 50, 80, 0x00)
        epd.fill_rect(70, 180, 50, 80, 0x00)
        epd.display_Base(epd.buffer)
        epd.delay_ms(2000)

        epd.init()
        epd.Clear(0xff)
        epd.delay_ms(2000)
        print("sleep")
        epd.sleep()
        led.toggle()
        continue
