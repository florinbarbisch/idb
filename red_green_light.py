# A simple script that turns the LED green if it's dark and red if it's bright
import time
import board
import analogio
import digitalio
import adafruit_dht
import adafruit_scd30
from rgbled import ChainableLED


# Light
# A0 auf Shield und Feather
A0 = analogio.AnalogIn(board.A0)
 

# RGB LED
# A2(D16) auf Shield und Feather
A2 = ChainableLED(board.A2, board.A3, 1)


while True:
    LIGHT = int(A0.value)
    light_to_scale = LIGHT* 255//42_000 
    A2.setColorRGB(light_to_scale, 255-light_to_scale,   0)
    print((1, LIGHT))
   
    time.sleep(0.01)
