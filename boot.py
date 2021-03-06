# boot.py -- run on boot-up
import os
import machine
from machine import Pin
from network import WLAN, Bluetooth

# Settings for WLAN STA mode
WLAN_SSID = ''
WLAN_AUTH = (WLAN.WPA2,'')

# Configure USB Serial
uart = machine.UART(0, 115200)
os.dupterm(uart)

# Turn off Bluetooth
bt = Bluetooth()
bt.deinit()

# Configure WLAN
wlan = WLAN()
wlan.deinit()

wlan_sta = Pin('P11', mode=Pin.IN, pull=Pin.PULL_UP)
wlan_ap = Pin('P12', mode=Pin.IN, pull=Pin.PULL_UP)

if not wlan_ap() and wlan_sta():
    print('WLAN: AP mode')
    wlan.init(mode=WLAN.AP, ssid='ttn-be-mapper', auth=(WLAN.WPA2,'reppam-eb-ntt'), channel=7, antenna=WLAN.INT_ANT)

elif not wlan_sta() and wlan_ap():
    print('WLAN: STA mode')
    wlan.init(mode=WLAN.STA)
    if not wlan.isconnected():
        wlan.connect(WLAN_SSID, auth=WLAN_AUTH, timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting

else:
    print('WLAN: Disabled')
