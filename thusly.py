#!/usr/bin/env python
# A simple GUI to show and log thrust test stand results.
# Needs an arduino running the sketch in this folder.

import pygtk
pygtk.require("2.0")
import gtk, gobject, serial, glob
import pololu

class ThuslyApp(object):
  sensor = {}
  
  def __init__(self):
      builder = gtk.Builder()
      builder.add_from_file("thusly.glade")
      
      self.current_throttle = 0
      
      self.throttle_val = builder.get_object("throttle_val")
      
      self.speed_text = builder.get_object("speed")
      self.current_text = builder.get_object("current")
      self.voltage_text = builder.get_object("voltage")
      self.throttle_text = builder.get_object("current_throttle")
      
      builder.connect_signals(
      { "on_window_destroy" : self.leave,
        "on_apply_clicked" : self.update_servo
      }
      )
      
      self.window = builder.get_object("window")
      self.window.show()
      
      ports = glob.glob('/dev/ttyUSB*')
	  	try:
      	self.ser = serial.Serial(ports[0], 9600, timeout=0.1)
      	print "Connected to Arduino on " + self.ser.port
	  	except RuntimeError:
				self.current_text.set_text("Can't connect to sensor")
		
			try:
      	self.throttle = pololu.Servo(0)
      	self.throttle.move(1000)
			except RuntimeError:
				self.current_text.set_text("Can't initialise servo")
  
  def update_servo(self, value):
      self.throttle.move(((self.throttle_val.get_value() + 1)*10)+990)
      self.throttle_text.set_text("Throttle: " + str(self.throttle_val.get_value()) + " %")
      self.current_throttle = self.throttle_val.get_value()
      
  def update(self):
      try:
        line = self.ser.readline()
        self.sensor = eval(line.strip())
        self.speed_text.set_text("Speed: " + str(self.sensor['rpm']) + " rev/min")
        self.current_text.set_text("Current: " + str(self.sensor['rpm']) + " A")
        self.voltage_text.set_text("Voltage: " + str(self.sensor['current']) + " Vdc")
        self.throttle_text.set_text("Throttle: " + str(self.current_throttle) + " %")
      except:
        #print "Connection lost"
        pass
      return True

  def leave(self, widget):
    self.throttle.move(((0 + 1)*10)+990)
    gtk.main_quit
    exit(0)
    
if __name__ == "__main__":
  app = ThuslyApp()
  gobject.idle_add(ThuslyApp.update, app)
  gtk.main()
