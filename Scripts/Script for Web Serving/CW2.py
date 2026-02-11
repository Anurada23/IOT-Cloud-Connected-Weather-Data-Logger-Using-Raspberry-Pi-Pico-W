import machine
from time import sleep
import network
import socket
from machine import Pin, I2C
import bme280  

# Initialize Wi-Fi
wlan = network.WLAN(network.STA_IF)  # STA mode (connect to router)
wlan.active(True)

# Check if Wi-Fi hardware is active
if not wlan.active():
    print("Wi-Fi interface is not active.")
    wlan.active(True)

# Scan for available networks (Optional)
nets = wlan.scan()
for net in nets:
    print(net[0].decode("utf-8"))  # Fix incorrect encoding

# Wi-Fi Credentials
ssid = 'SLT-Fiber-D5D7'  
password = 'passcode23'  

# Initialize I2C and BME280 sensor
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
bmp = bme280.BME280(i2c=i2c)  # Corrected initialization

def connect():
    if not wlan.isconnected():  # Only connect if not already connected
        print(f"Connecting to {ssid}...")
        wlan.connect(ssid, password)
        
        timeout = 10  # Set a timeout limit (10 seconds)
        while not wlan.isconnected() and timeout > 0:
            print(f"Waiting for connection... {timeout}s left")
            sleep(1)
            timeout -= 1

        if wlan.isconnected():
            ip = wlan.ifconfig()[0]
            print(f' Connected on {ip}')
            return ip
        else:
            print(" Failed to connect. Check Wi-Fi credentials or signal strength.")
            return None
    else:
        print(f'Already connected on {wlan.ifconfig()[0]}')
        return wlan.ifconfig()[0]

# Call the function
#connect()

def open_socket(ip):
    # Open a socket 
    address = (ip, 80) 
    connection = socket.socket() 
    connection.bind(address) 
    connection.listen(1) 
    print(connection) 
    return connection
        
def webpage(reading):
    # Template HTML 
    html = f""" 
            <!DOCTYPE html> 
            <html> 
            <head> 
            <title>Pico W Sensor Data</title> 
            <meta http-equiv="refresh" content="10"> 
            </head> 
            <body> 
            <h2>Sensor Readings</h2>
            <p>{reading}</p> 
            </body> 
            </html> 
            """ 
    return str(html)


def serve(connection):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)

        # Read sensor values
        temperature, pressure, humidity = bmp.values  # Returns strings already formatted

        # Format readings
        reading = f'Temperature: {temperature}, Pressure: {pressure}, Humidity: {humidity}'
        
        # Generate HTML response
        html = webpage(reading)
        client.send(html)
        client.close()

try: 
    ip = connect() 
    if ip:
        connection = open_socket(ip) 
        serve(connection) 
except KeyboardInterrupt: 
    machine.reset()
