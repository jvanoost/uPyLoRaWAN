import utime
import struct
import urandom
from sx127x import TTN, SX127x
from machine import Pin, SPI
from config import *
from time import *

from hx711_gpio import *

__DEBUG__ = True

# micro python epoch is since 01/01/2000 need to give timediff since 01/01/1970
timediff = 946684800


ttn_config = TTN(ttn_config['devaddr'], ttn_config['nwkey'], ttn_config['app'], country=ttn_config['country'])

device_spi = SPI(device_config['spi_unit'], baudrate = 10000000, 
        polarity = 0, phase = 0, bits = 8, firstbit = SPI.MSB,
        sck = Pin(device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
        mosi = Pin(device_config['mosi'], Pin.OUT, Pin.PULL_UP),
        miso = Pin(device_config['miso'], Pin.IN, Pin.PULL_UP))

lora = SX127x(device_spi, pins=device_config, lora_parameters=lora_parameters, ttn_config=ttn_config, channel=None)
frame_counter = 0

pinData = Pin(16, Pin.IN, pull=Pin.PULL_DOWN)
pinSCK = Pin(4, Pin.OUT)

hx711 = HX711(pinSCK, pinData)
hx711.tare()

sleep_ms(2000)

hx711.set_scale(1)

def on_receive(lora, outgoing):
    payload = lora.read_payload()
    print("Recu :")
    print(payload)
    print("#############")

lora.on_receive(on_receive)
lora.receive()

while True:
    epoch = utime.time() + timediff
    temperature = urandom.randint(0,30)

    weight = hx711.get_units()
    weight = urandom.randint(0,15) + urandom.random()
    weightReal = int(weight)
    weightDec = int((weight % 1) * 100)

    payload = struct.pack('@Qh', int(epoch), int(temperature))
    payload = struct.pack('@Qh', int(epoch), int(temperature), int(weightReal), int(weightDec))
    payload1 = struct.pack('@Qh', int(weightReal), int(weightDec))

    if __DEBUG__:
        print("Epoch: %s" % (epoch))
        print("Temperature: %s" % (temperature))
        print("Weight : %s" % weight)
        print("Weight real : %s" % weightReal)
        print("Weight dec : %s" % weightDec)
        print(type(payload))
        print(payload)
        print(type(payload1))
        print(payload1)

    lora.send_data(data=payload, data_length=len(payload), frame_counter=frame_counter)
    lora.receive()
    
    frame_counter += 1

    for i in range(app_config['loop']):
        utime.sleep_ms(app_config['sleep'])