#!/usr/bin/python
import time
import RPi.GPIO as GPIO  # Control library for Rpi GPIOs
import paho.mqtt.subscribe as subscribe  # library to send MQTT messages to broker
import paho.mqtt.client as mqtt  # import the client1
import math


def main():
    Total = 0
    for i in range(1, 11):
        # We will be using BCM GPIO numbering
        GPIO.setmode(GPIO.BCM)

        # Select the GPIOs numbers
        GPIO_TRIGGER = 17
        GPIO_ECHO = 27

        # Set TRIGGER to OUTPUT mode
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        # Set ECHO to INPUT mode
        GPIO.setup(GPIO_ECHO, GPIO.IN)

        # Set TRIGGER to LOW
        GPIO.output(GPIO_TRIGGER, False)                                                                                                                                                                                                                                                                                                                                                                                                                                                          # Let the sensor settle for a while                                                                                                                                                                                                          time.sleep(0.5)

        # Send 10 microsecond pulse to TRIGGER
        GPIO.output(GPIO_TRIGGER, True)  # set TRIGGER to HIGH
        time.sleep(0.00001)  # wait 10 microseconds
        GPIO.output(GPIO_TRIGGER, False)  # set TRIGGER back to LOW

        # Create variable start and give it current time
        start = time.time()
        # Refresh start value until the ECHO goes HIGH = until the wave is send
        while GPIO.input(GPIO_ECHO) == 0:
            start = time.time()
        # Assign the actual time to stop variable until the ECHO goes back from HIGH to LOW
        while GPIO.input(GPIO_ECHO) == 1:
            stop = time.time()

        # Calculate the time it took the wave to travel there and back
        measuredTime = stop - start
        # Calculate the travel distance by multiplying the measured time by speed of sound
	# Speed of sound is depending on the environment temperature
        distanceBothWays = measuredTime * 35100  # cm/s in 20 degrees Celsius
        # Divide the distance by 2 to get the actual distance from sensor to obstacle
        distance = distanceBothWays / 2
        # Print the distance
        print("Distance : {0:5.1f}cm".format(distance))
	
# Print the median of 10 measurements	
print(Total)
average = Total / 10
print(average)
# Subtract the distance from the sensor to the water surface from the measured height between the bottom of your collector 
# and the position of the sensor. In my case the sensor is mounted 200cm above bottom of the collector.
afstand = 200 - average
print(afstand)

# If you have a cylindrical shaped rain water collector, you will need to measure the radius.
# 8281 = kwadraat van 91 (straal van de regenput cilinder)
# To calculate the volume of a cylinder, the following formula is used.
# V = π x r² x h (where r = radius and h = height)

radius = 91
liters = afstand * 8281 * math.pi
print(liters)


client = mqtt.Client("P1")  # create new instance
client.connect('192.168.1.195')  # connect to broker
client.publish("/sensors/rainwatertank/Total", liters)  # publish
# Reset GPIO settings
GPIO.cleanup()

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
