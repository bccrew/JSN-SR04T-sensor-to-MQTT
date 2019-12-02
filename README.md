## Use JSN-SR04T sensor on Raspberry Pi to calculate the cylindrical volume or a raintank and publish to MQTT broker
```

Installation instruction:

1) Install the paho-mqtt library

sudo pip3 install paho-mqtt

2) Place the script wherever you want on the raspberry pi

3) Edit the script to the measurements of your rainwater tank

TankHeight = 200  # distance from sensor to bottom of tank ( cm )
TankRadius = 91  # radius of tank ( cm )
BrokerAddr = '192.168.1.41'  # Address of MQTT brocker

```
