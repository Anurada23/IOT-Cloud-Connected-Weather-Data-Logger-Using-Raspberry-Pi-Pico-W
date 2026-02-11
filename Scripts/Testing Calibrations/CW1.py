from machine import Pin, I2C
import bme280
import time

# Initialize I2C for the sensor
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Initialize BME280 sensor
bmp = bme280.BME280(i2c=i2c)

# Loop to read and print sensor values 5 times
for _ in range(5):
    # Read sensor values
    temperature, pressure, humidity = bmp.values  # Returns a tuple of strings

    # Print formatted output
    print(f'Temperature: {temperature}, Pressure: {pressure}, Humidity: {humidity}')

    # Wait for 2 seconds before the next reading
    time.sleep(2)
