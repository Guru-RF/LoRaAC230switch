import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_rfm9x
import config

def purple(data):
  stamp = time.time()
  return "\x1b[38;5;104m[" + str(stamp) + "] " + data + "\x1b[0m"

def yellow(data):
  return "\x1b[38;5;220m" + data + "\x1b[0m"

def red(data):
  return "\x1b[1;5;31m -- " + data + "\x1b[0m"

# our version
VERSION = "RF.Guru_AC230_Switch_LoRa 0.1" 

sw = DigitalInOut(board.GP16)
sw.direction = Direction.OUTPUT
sw.value = True
time.sleep(0.01)
if config.default_on is False:
  sw.value = False

print(red(config.name + " -=- " + VERSION))

# Lora Stuff
RADIO_FREQ_MHZ = 868.000
CS = DigitalInOut(board.GP21)
RESET = DigitalInOut(board.GP20)
spi = busio.SPI(board.GP10, MOSI=board.GP11, MISO=board.GP8)
rfm9x = adafruit_rfm9x.RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ, baudrate=1000000, agc=False,crc=True)
rfm9x.tx_power = 5

while True:
    msg = yellow("Waiting for LoRa packet ...")
    print(f"{msg}\r", end="")
    packet = rfm9x.receive(with_header=True,timeout=10)

    if packet is not None:
        #print(packet)
        if packet[:3] == (b'<\xaa\x01'):
                rawdata = bytes(packet[3:]).decode('utf-8')
                if rawdata.startswith(config.name):
                    if sw.value is False:
                        sw.value = True
                        print(purple("PORT REQ: Turned port on"))
                    elif sw.value is True:
                        sw.value = False
                        print(purple("PORT REQ: Turned port off"))
                else:
                    print(yellow("Received another switch port req packet: " + str(rawdata)))
        else:
            print(yellow("Received an unknown packet: " + str(packet)))