# boot.py
import config
import network
import utime
import ntptime

from oledshow import oled

## ftp access
#from ftp import ftpserver

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    start = utime.time()
    timed_out = False

    if not sta_if.isconnected():
        print('Connexion au Wifi...')
        sta_if.active(True)
        sta_if.connect(config.wifi_config["ssid"], config.wifi_config["password"])
        while not sta_if.isconnected() and \
            not timed_out:        
            if utime.time() - start >= 20:
                timed_out = True
            else:
                pass

    if sta_if.isconnected():
        ntptime.settime()
        print('Config reseau :', sta_if.ifconfig())
        oled.fill(0) 
        oled.text('WiFi OK', 0, 0) 
        oled.text('IP :'+sta_if.ifconfig()[0], 0, 20) 
        oled.show()
    else: 
        print('internet non dispo')

do_connect()