#!/usr/bin/python

# Import required Python libraries
import time  # library for time reading time
import RPi.GPIO as GPIO  # library to control Rpi GPIOs
import math
import myMQTT as mq

TankHeight = 200  # distance from sensor to bottom of tank ( cm )
TankRadius = 91  # radius of tank ( cm )
BrokerAddr = '192.168.1.41'  # Address of MQTT brocker

# Select which GPIOs you will use
GPIO_TRIGGER = 17
GPIO_ECHO = 27


def setGPIO():
    # We will be using the BCM GPIO numbering
    GPIO.setmode(GPIO.BCM)

    # Set TRIGGER to OUTPUT mode
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    # Set ECHO to INPUT mode
    GPIO.setup(GPIO_ECHO, GPIO.IN)


def getDistance():
    # Set TRIGGER to LOW
    GPIO.output(GPIO_TRIGGER, False)

    # Let the sensor settle for a while
    time.sleep(0.5)

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
    distanceBothWays = measuredTime * 35100  # cm/s in 20 degrees Celsius
    # Divide the distance by 2 to get the actual distance from sensor to obstacle
    distance = distanceBothWays / 2
    # Print the distance
    print("Distance : {0:5.1f}cm".format(distance))

    return distance


def getData():
    global TankHeight, TankRadius
    temp = 0
    measurements = 10
    setGPIO()
    for i in range(measurements):
        temp += getDistance()
    # Reset GPIO settings
    GPIO.cleanup()
	
	# To calculate the total amount of liters, we'll use the standard formula to calculate cylindrical volume: V = π . r² . h (Where r : radius and h = height)
	# First we'll subtract the distance from the sensor to the water surface from the distance between the sensor and the bottom of the raintank. This will give us te height of the water level.

    WaterHeight = TankHeight - temp / measurements
    print("Water level: {0:5.1f}cm".format(WaterHeight))
	
	# Calculate the volume.
    liters = WaterHeight * TankRadius * TankRadius * math.pi / 1000
    print("In liters: {0:5.1f}".format(liters))
    percentage = liters / 50
    print("Filled: {0:5.1f}%".format(percentage))
    return (int(WaterHeight),int(liters),int(percentage))


def main():
    global BrokerAddr
    c = mq.myMQTT()
    c.run(addr=BrokerAddr)  # connect to broker
    height, liters, percentage = getData()
    c.publish('sensors/rainwatertank/Height', height)
    c.publish('sensors/rainwatertank/Total', liters)
    c.publish('sensors/rainwatertank/Percentage', percentage)
    c.disconnect()


# Run the main function when the script is executed
if __name__ == "__main__":
    main()

