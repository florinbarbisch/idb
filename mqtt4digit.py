import json
import time
from grove.grove_4_digit_display import Grove4DigitDisplay
import paho.mqtt.subscribe as subscribe

# configure display
display = Grove4DigitDisplay(16, 17)  # Using 4 digit display

# initialize display
print("----")
display.show("----")

# callback
def on_message(client, userdata, message):
    payload = json.loads(message.payload)
    co2 = payload["uplink_message"]["decoded_payload"]["co2"]
    print(f"{co2} ppm CO2")
    display.show(f"{co2:>4}")

# subscribe
subscribe.callback(on_message, topics=['v3/fhnw-idb@ttn/devices/fhnw-idb-device-0/up'], hostname="eu1.cloud.thethings.network", port=1883, auth={'username':"fhnw-idb@ttn",'password':"NNSXS.XTNOWVYHW34HY3KESJ7ASAZLVZFQFPDJDU2XGCA.ORIOY33IQMMA5RN6W7M53X22C3GPYKSX63BWXPPYHTOU2TVURPSA"})
