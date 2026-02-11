# IOT-Cloud-Connected-Weather-Data-Logger-Using-Raspberry-Pi-Pico-W-
an Edge-to-Cloud IoT Environmental Monitoring System

![FrontEnd Preview](Assets/Asset2.jpeg)

This project demonstrates an IoT-based environmental monitoring system using a Raspberry Pi Pico W and BME280 sensor. The device collects real-time temperature, pressure, and humidity data and sends it to a cloud-hosted Google Apps Script, which logs the readings into Google Sheets for remote monitoring and analysis.

---

## Features

- Reads temperature, pressure, and humidity using the BME280 sensor
- Connects to Wi-Fi and fetches real-time data from the device
- Sends data via HTTP GET requests to Google Apps Script
- Cloud-based storage in Google Sheets for historical data and visualization
- Automatic periodic data reporting with error handling and retries
- Lightweight, microcontroller-friendly Python (MicroPython) implementation

---

## Architecture

- **Device / Hardware:** Raspberry Pi Pico W, BME280 sensor, breadboard, I2C communication
- **Firmware / Embedded Software:** MicroPython scripts for sensor reading and HTTP requests
- **Cloud Backend:** Google Apps Script for receiving data and updating Google Sheets
- **Communication:** HTTP/REST over Wi-Fi

---

## Tech Stack

- **Hardware:** Raspberry Pi Pico W, BME280 sensor, Breadboard
- **Programming / Firmware:** MicroPython
- **Cloud / Backend:** Google Apps Script, Google Sheets, REST APIs
- **Tools & IDEs:** Thonny IDE, Wi-Fi networking

---

## Setup

1. **Hardware Wiring**
   - Connect BME280 sensor to Raspberry Pi Pico W using I2C (SDA → Pin 0, SCL → Pin 1)
   - Power the Pico W via USB

2. **MicroPython Setup**
   - Install MicroPython on the Pico W using Thonny IDE
   - Upload the main Python script (`main.py`) to the Pico

3. **Wi-Fi Credentials**
   - Update your SSID and password in the Python script

4. **Google Apps Script**
   - Create a Google Apps Script project and deploy as a web app (`doGet(e)`)
   - Use the script URL in your Pico W Python script

5. **Run**
   - Power on the Pico W
   - The script will read sensor values and send data to Google Sheets periodically

---

## Usage

- View live sensor data in the Google Sheet
- Access historical logs and create charts/graphs directly in Google Sheets
- Modify the update interval by changing the sleep time in the Python script

---

## Future Improvements

- Switch to HTTP POST for more secure data transmission
- Add local web dashboard for real-time monitoring
- Integrate MQTT for scalable IoT telemetry
- Use Firebase or other cloud services for advanced analytics

---

## License

This project is licensed under the MIT License. Feel free to use, modify, and share!

---

## Acknowledgements

- [Raspberry Pi Pico W Documentation](https://www.raspberrypi.com/documentation/microcontrollers/)
- [BME280 Sensor Datasheet](https://www.bosch-sensortec.com/products/environmental-sensors/bme280/)
- [Google Apps Script Documentation](https://developers.google.com/apps-script)


