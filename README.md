**Dashboard\n**
This project demonstrates the integration of GPS, speedometer (IR sensor), fuel sensor, and GSM module on a Raspberry Pi. The system provides real-time updates of speed and location (latitude and longitude) and sends this data via SMS using the GSM module. It also monitors the fuel level and triggers a low-fuel warning.

**Features:**
Real-Time GPS Data: Latitude and longitude are read from the GPS module and displayed in real-time on a Tkinter GUI.
Speedometer: The system calculates speed based on pulses from an IR sensor.
Fuel Monitoring: The fuel sensor checks for low fuel and displays a warning if needed.
SMS Updates: Sends real-time updates of speed and location via SMS using the GSM module.

**Hardware Required:**
Raspberry Pi (any model with GPIO pins)
GPS Module (e.g., Neo-6M GPS)
IR Sensor (for speed measurement)
Fuel Sensor (Digital input for fuel level)
GSM Module (e.g., SIM800L or SIM900)
**Software Required:**
Raspberry Pi OS (or any Linux-based OS for Raspberry Pi)
Python 3: Ensure Python 3 is installed.
PySerial: Used for serial communication with GPS and GSM modules.
Install PySerial using pip:

**Code Explanation:**
GPS Module: The script reads GPS data using the serial communication and parses $GPGGA sentences to extract latitude and longitude.
IR Sensor: The speed is calculated based on pulse counts from the IR sensor.
Fuel Sensor: A digital GPIO input checks if the fuel is low.
GSM Module: The GSM module is used to send SMS messages with speed and location updates.
**Customization:**
Phone Number: Replace "<Recipient_Phone_Number>" in the code with the phone number to which you want to send the SMS updates.
GPIO Pins: If your sensors are connected to different GPIO pins, change the sensor_pin and fuel variables in the script.
