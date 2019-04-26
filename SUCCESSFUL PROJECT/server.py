#! /usr/bin/python
import os.path 
import tornado.httpserver 
import tornado.websocket 
import tornado.ioloop 
import tornado.web 
import RPi.GPIO as GPIO
import subprocess
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

print "mode: "
print GPIO.getmode()

#GPIO.setmode(GPIO.BOARD)

#print "mode: "
#print GPIO.getmode()

#software box configuration:
OUT1 = 24
LED1 = 23

#software SPI configuration:
CLK = 23
MISO = 21
MOSI = 19
CS = 24
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)
print "mode: "
print GPIO.getmode()

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Define Variables
delay = 0.5
ldr_channel = 0

def readadc(i):
   # read SPI data from the MCP3008, channel 1 is temp channel 0 is light
   if i == 1:
	millivolts = mcp.read_adc(i)*(3300/1024)
	temp_C = ((millivolts-500.0)/10.0)
	temp_F = (temp_C*9.0/5.0)+32
	temp_C = "%.1f" % temp_C
	temp_F = "%1.f" % temp_F
	return temp_F
   else:
	return (mcp.read_adc(i))/160

#Initialize Raspberry PI GPIO
GPIO.setup(LED1, GPIO.OUT) 
GPIO.setup(OUT1, GPIO.OUT)
GPIO.output(LED1, False)
GPIO.output(OUT1, True)

#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static")
	)
#Tonado server port
PORT = 8888 
class MainHandler(tornado.web.RequestHandler):
  def get(self):
     print "[HTTP](MainHandler) User Connected."
     self.render("index.html")
	
class WSHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self, origin):
    print origin
    return origin == "http://ec2-3-85-217-77.compute-1.amazonaws.com"

  def open(self):
    print '[WS] Connection was opened.'
 
  def on_message(self, message):
    print '[WS] Incoming message:', message
    #self.write_message(subprocess.check_output(["hostname", "-I"]));
    if message == "on_outlet1":
      GPIO.output(OUT1, False)
      GPIO.output(LED1, True)
    if message == "off_outlet1":
      GPIO.output(OUT1, True)
      GPIO.output(LED1, False)
    if message == "refresh_lum":
      self.write_message(str(readadc(0))+ " LUM")
    if message == "refresh_temp":
      self.write_message(str(readadc(1))+ " TEMP")
  def on_close(self):
    print '[WS] Connection was closed.' 



application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  ]) 
if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(PORT)
        main_loop = tornado.ioloop.IOLoop.instance()
        print "Tornado Server started"
        main_loop.start()
    except:
        print "Exception triggered - Tornado Server stopped."
        GPIO.cleanup()
#End of Program
