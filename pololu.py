# -*- coding: utf-8 -*-
from subprocess import call
class Servo:
  def __init__(self, servo = 0):
    self.servo = servo
    
  def move(self, pos):
    call("UscCmd " + "--servo " + str(self.servo) + "," + str(pos*4), shell=True)

if __name__ == "__main__":
  s = Servo()
  s.move(1000)
  s.move(2000)
