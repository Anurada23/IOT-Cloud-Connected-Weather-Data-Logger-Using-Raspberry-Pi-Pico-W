import machine
import time
from machine import Pin, ADC
import network
import urequests
import json
import gc
from machine import Pin, I2C
import bme280

# WiFi Setup
wlan = network.WLAN(network.STA_IF)
board_led = machine.Pin("LED", machine.Pin.OUT)
ssid = 'SLT-Fiber-D5D7'  
password = 'passcode23'

# URLs
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx9pEC_4-mtpgh_Jl9SFPeXmfaasSEkTX7TtkbZ_rFRyI6_BokiFZB9RIerAD7rwpr5/exec"
TIME_URL = "https://timeapi.io/api/Time/current/zone?timeZone=Asia%2FColombo"



i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

bmp = bme280.BME280(i2c=i2c)

def getTime():
    try:
        res = urequests.get(url=TIME_URL)
        time_data = json.loads(res.text)["dateTime"]
        res.close()
        return time_data
    except Exception as e:
        print(f"Error fetching time: {e}")
        return "Error"

def connectWifi():
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(ssid, password)
        while not wlan.isconnected() and wlan.status() >= 0:
            print("Waiting to connect...")
            time.sleep(1)
            board_led.off()
            board_led.on()
        board_led.on()
        print("Connected:", wlan.ifconfig())
    else:
        print("WiFi already connected..")
        print(getTime())


def readBME280():
    try:
        # Retrieve the values from the sensor
        values = bmp.values
        
        # Print raw values for debugging
#         print("Raw sensor values:", values)

        # Extract the numeric values and remove units
        temperature_str = values[0].replace('C', '').strip()
        pressure_str = values[1].replace('hPa', '').strip()
        humidity_str = values[2].replace('%', '').strip()

        # Convert the cleaned-up strings to float
        temperature = float(temperature_str) if temperature_str else None
        pressure = float(pressure_str) if pressure_str else None
        humidity = float(humidity_str) if humidity_str else None

        # Ensure that all values are valid
        if temperature is None or pressure is None or humidity is None:
            raise ValueError("One or more sensor values are invalid.")

        return temperature, pressure, humidity
    except Exception as e:
        print(f"Error reading BME280 values: {e}")
        return None, None, None

def sendToSpreadsheet(time,sensor1,sensor2,sensor3):
    try:
        url = f"{SCRIPT_URL}?time={time}&sensor1={temperature}&sensor2={pressure}&sensor3={humidity}"
        print(f"Sending: {url}")
        res = urequests.get(url=url)
        res.close()
        gc.collect()
    except Exception as e:
        print(f"Error sending data: {e}")

# Connect to WiFi
connectWifi()

# Send temperature data 5 times
for i in range(5):
    try:
        timestamp = getTime()
        if timestamp == "Error":  # Skip iteration if timestamp retrieval fails
            print("Skipping iteration due to timestamp error.")
            continue
        
        temperature, pressure, humidity = readBME280()
        
        # Print the values
        print(f"Temperature: {temperature}°C")
        print(f"Pressure: {pressure} hPa")
        print(f"Humidity: {humidity}%")    
        
        sendToSpreadsheet(time=timestamp, sensor1=temperature, sensor2=pressure, sensor3=humidity)
    
    except Exception as e:
        print(f"Error occurred in iteration {i+1}: {e}")
    
    time.sleep(7)

board_led.off()

