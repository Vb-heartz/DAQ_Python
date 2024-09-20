import serial
import time
from datetime import datetime

# Configure serial port
ser = serial.Serial('COM4', 9600) # Replace '/dev/ttyUSB0' with your FTDI device file
output_file = 'data_log.txt'

def read_from_fpga():
    while True:
        if ser.in_waiting >= 32:  # Each data packet is 32 bytes (8 channels, 4 bytes each)
            data = ser.read(32)  # Read 32 bytes
            ch1 = int.from_bytes(data[0:4], byteorder='big')
            ch2 = int.from_bytes(data[4:8], byteorder='big')
            ch3 = int.from_bytes(data[8:12], byteorder='big')
            ch4 = int.from_bytes(data[12:16], byteorder='big')
            ch5 = int.from_bytes(data[16:20], byteorder='big')
            ch6 = int.from_bytes(data[20:24], byteorder='big')
            ch7 = int.from_bytes(data[24:28], byteorder='big')
            ch8 = int.from_bytes(data[28:32], byteorder='big')
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_data(timestamp, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8)
            time.sleep(1)

def log_data(timestamp, ch1, ch2, ch3, ch4, ch5, ch6, ch7, ch8):
    with open(output_file, 'a') as file:
        file.write(f'{timestamp}, {ch1}, {ch2}, {ch3}, {ch4}, {ch5}, {ch6}, {ch7}, {ch8}\n')

if __name__ == "__main__":
    try:
        with open(output_file, 'w') as file:  # Initialize the file with headers
            file.write('Date, Time, Channel 1, Channel 2, Channel 3, Channel 4, Channel 5, Channel 6, Channel 7, Channel 8\n')
        read_from_fpga()
    except KeyboardInterrupt:
        ser.close()
        print("Program terminated")
