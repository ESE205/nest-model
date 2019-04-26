# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008


# Software SPI configuration:
CLK  = 23
MISO = 21
MOSI = 19
CS   = 24
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>4} | {1:>4} |'.format(*range(8)))
print('-' * 57)
# Main program loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0]*2
    for i in range(2):
        # The read_adc function will get the value of the specified channel (0-7).
        if i==1:
            millivolts = mcp.read_adc(i)*(3300/1024)
            temp_C = ((millivolts-500.0)/10.0)
            temp_F = (temp_C*9.0/5.0)+32
            temp_C = "%.1f" % temp_C
            temp_F = "%1.f" % temp_F
            values[i] = temp_F
        else:
            values[i] = mcp.read_adc(i)
    # Print the ADC values.
    print('| {0:>4} | {1:>4} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)
