import RPi.GPIO as GPIO
import time
import serial
import tkinter as tk

# Pin definitions
sensor_pin = 2  # IR sensor connected to GPIO pin 2
fuel = 18  # Fuel sensor connected to GPIO pin 18

# Set up GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(fuel, GPIO.IN)
GPIO.setup(sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Serial port configuration for GPS and GSM
gps_ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # GPS module connected to Raspberry Pi
gsm_ser = serial.Serial('/dev/ttyAMA0', 9600, timeout=1)  # GSM module connected to Raspberry Pi

# Initialize speed counter and time
count = 0
start_time = time.time()

# GPS data initialization
lat = None
lon = None

# GUI setup
root = tk.Tk()
root.title("Speedometer with GPS and GSM")
root.geometry("400x300")
root.configure(bg="#cc8b6a")

# Speed and fuel labels
speed_label = tk.Label(root, text="Speed: 0 Km/hr", font=("Helvetica", 42), bg="#cc8b6a", fg="#000000")
speed_label.pack(fill="both", expand=True, padx=10, pady=10)

# Function to send SMS via GSM
def send_sms(message, phone_number):
    try:
        gsm_ser.write(b'AT+CMGF=1\r')  # Set SMS mode to text
        time.sleep(0.5)
        gsm_ser.write(f'AT+CMGS="{phone_number}"\r'.encode())  # Set recipient's phone number
        time.sleep(0.5)
        gsm_ser.write(f'{message}\x1A'.encode())  # Send the message with Ctrl+Z (0x1A)
        print(f"Message sent: {message}")
    except Exception as e:
        print(f"Error sending SMS: {e}")

# Function to read GPS data and parse latitude and longitude
def read_gps():
    global lat, lon
    try:
        while gps_ser.in_waiting > 0:
            line = gps_ser.readline().decode('utf-8').strip()  # Read a line from the GPS
            if line.startswith('$GPGGA'):
                fields = line.split(",")
                if fields[2] and fields[4]:  # Check if latitude and longitude are available
                    lat = float(fields[2]) / 100  # Convert latitude to float
                    lon = float(fields[4]) / 100  # Convert longitude to float
                    lat_deg = int(lat // 1)  # Degrees
                    lat_min = (lat % 1) * 60  # Minutes
                    lon_deg = int(lon // 1)  # Degrees
                    lon_min = (lon % 1) * 60  # Minutes
                    lat = f"{lat_deg}°{lat_min:.2f}' N"
                    lon = f"{lon_deg}°{lon_min:.2f}' E"
                    print(f"Latitude: {lat}, Longitude: {lon}")
                    # Update the label with the latest location
                    location_label.config(text=f"Lat: {lat}\nLon: {lon}")
                    # Send the GPS coordinates via SMS
                    send_sms(f"Location Update:\nLat: {lat}\nLon: {lon}", "<Recipient_Phone_Number>")
                    break  # Only process the first GPS fix
    except Exception as e:
        print("Error reading GPS data:", e)

# Function to handle speed pulse detection
def detect_pulse(channel):
    global count
    count += 1

# Add event detection for the IR sensor
GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=detect_pulse, bouncetime=20)

# Function to handle low fuel warning
def lowfuel(speed):
    speed_label["text"] = f"Speed: {round(speed)} Km/hr\nLOW FUEL! Return to pit!!"

# Update function to calculate speed and update UI
def update():
    global start_time, count
    current_time = time.time()
    elapsed_time = current_time - start_time
    if elapsed_time >= 1:
        rpm = count / elapsed_time * 60  # Calculate RPM
        speed = 0.001885 * rpm * 7.6433121  # Calculate speed in km/hr
        if GPIO.input(fuel):  # If fuel sensor detects low fuel
            lowfuel(speed)
        else:
            speed_label["text"] = f"Speed: {round(speed)} Km/hr"
        count = 0
        start_time = current_time
        # Send the speed data via GSM
        send_sms(f"Speed Update: {round(speed)} Km/hr", "<Recipient_Phone_Number>")
    root.after(100, update)

# Create a label for displaying location
location_label = tk.Label(root, text="Lat: N/A\nLon: N/A", font=("Helvetica", 20), bg="#cc8b6a", fg="#000000")
location_label.pack(fill="both", expand=True, padx=10, pady=10)

# Start the GPS reading and speed calculation loop
root.after(1000, update)
root.after(1000, read_gps)  # Start reading GPS every second

# Start the Tkinter main loop
root.mainloop()
