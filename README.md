# Raspberry Pi Dashboard

This project is a speedometer system built using a Raspberry Pi, IR sensor, fuel sensor, GPS module, and GSM module. It calculates the speed of a moving object, retrieves GPS location, and sends location and speed updates via SMS to a predefined phone number.

## Components Used

- **Raspberry Pi** (Any model with GPIO support)
- **IR Sensor** (To measure speed through pulse detection)
- **Fuel Sensor** (To detect low fuel levels)
- **GPS Module** (To get latitude and longitude coordinates)
- **GSM Module** (To send SMS messages)
- **Wires and Connectors** for connections

## Features

- **Speed Calculation**: The system detects the IR sensor's pulses, calculates the RPM, and then computes the speed of the object.
- **GPS Location Tracking**: The GPS module provides the current latitude and longitude of the object.
- **SMS Notifications**: The system sends the speed and location updates via SMS to a predefined phone number when certain events occur (e.g., location update, speed update).
- **Low Fuel Warning**: If the fuel sensor detects low fuel, the system will display a warning on the UI.

## Installation

1. **Hardware Setup**:
   - Connect the IR sensor to GPIO pin 2 on the Raspberry Pi.
   - Connect the fuel sensor to GPIO pin 18 on the Raspberry Pi.
   - Connect the GPS module to `/dev/ttyUSB0` on the Raspberry Pi.
   - Connect the GSM module to `/dev/ttyAMA0` on the Raspberry Pi.

2. **Software Setup**:
   - Install required Python libraries:
     ```bash
     pip install RPi.GPIO pyserial tkinter
     ```
   - Ensure your Raspberry Pi has access to the serial ports used by the GPS and GSM modules.

## Code Explanation

- **GPIO Setup**: Configures GPIO pins for the IR sensor and fuel sensor, with appropriate pull-up resistors.
- **Serial Communication**: Configures serial communication for GPS and GSM modules.
- **Speed Calculation**: Detects pulses from the IR sensor to calculate speed using RPM.
- **GPS Reading**: Reads GPS data from the GPS module and extracts latitude and longitude.
- **SMS Sending**: Sends SMS updates using the GSM module with the speed and location data.
- **UI**: Displays the calculated speed and GPS location in a GUI created with Tkinter.

## How It Works

1. The program continuously listens for pulses from the IR sensor to calculate speed.
2. It reads GPS data and extracts latitude and longitude.
3. If the fuel level is low, a warning is displayed on the UI.
4. The calculated speed and GPS location are sent via SMS using the GSM module.
5. The GUI updates in real time, showing the speed and GPS location.

## Running the Program

1. Connect your Raspberry Pi to the IR sensor, fuel sensor, GPS module, and GSM module as described in the hardware setup.
2. Run the Python script on your Raspberry Pi:
   ```bash
   python3 speedometer_gps_gsm.py
