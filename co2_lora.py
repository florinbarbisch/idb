import time
import board
import busio
import digitalio
from adafruit_tinylora import adafruit_tinylora
import adafruit_scd30
from rgbled import ChainableLED



## LORA
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)

# FeatherWing RFM95, nRF52840
cs = digitalio.DigitalInOut(board.D5)
irq = digitalio.DigitalInOut(board.D10)
rst = digitalio.DigitalInOut(board.D6)

# TTN https://console.thethingsnetwork.org/
ttn_dev_address_msb = bytearray([0x26, 0x0B, 0xEF, 0x24])

ttn_net_session_key_msb = bytearray(
    [0xAA, 0x9B, 0xC7, 0x3A, 0xAB, 0x36, 0xFB, 0x8D,
     0x20, 0xF8, 0x7F, 0x93, 0xD0, 0x70, 0xF1, 0x70])

ttn_app_session_key_msb = bytearray(
    [0x6C, 0x8B, 0xD7, 0x06, 0x01, 0x2F, 0x90, 0xE0,
     0x02, 0x61, 0x0D, 0x3B, 0x8B, 0x76, 0x84, 0x79])

ttn_region = "EU" # 868 MHz
ttn_config = adafruit_tinylora.TTN(
    ttn_dev_address_msb,
    ttn_net_session_key_msb,
    ttn_app_session_key_msb,
    ttn_region)

lora = adafruit_tinylora.TinyLoRa(spi, cs, irq, rst, ttn_config)



## Sensors and Actuators
# CO2, Humidity and Temperature
# I2C-1 auf Shield, D23 auf Feather
SCD30 = adafruit_scd30.SCD30(board.I2C())

# Button
# A0 auf Shield und Feather
button = digitalio.DigitalInOut(board.A0)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# RGB LED
# A2(D16) auf Shield und Feather
led = ChainableLED(board.A2, board.A3, 1)


read_interval = 600 # in seconds
refreshs_per_seconds = 30 # like fps for the LED

while True:
    print("Reading values...")

    # read values
    co2_val = int(SCD30.CO2)
    temp_val = int(SCD30.temperature * 100)
    humidity_val = int(SCD30.relative_humidity * 100)
    print("CO2", co2_val, "TEMP", temp_val, "HUM", humidity_val)

    # send over LoRaWAN
    print("Sending packet...")
    order = 'big'
    raw_data = str(co2_val) + ";" + str(temp_val) + ";" + str(humidity_val)
    byte_data = bytearray()
    byte_data.extend(raw_data.encode())
    print("byte_data", byte_data)
    lora.send_data(byte_data, len(byte_data), lora.frame_counter)
    lora.frame_counter += 1
    print("done.")

    for i in range(read_interval * refreshs_per_seconds):
        if button.value:
            if co2_val >= 1000: # some one needs to open the windows for fresh air
                led.setColorRGB(255,0,0)
            else:
                led.setColorRGB(0,255,0)
        else:
            led.setColorRGB(0,0,0)
        time.sleep(1/refreshs_per_seconds)
