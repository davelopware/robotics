#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time
import getopt
import sys
from Tkinter import *

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
#pwm = PWM(0x40, debug=True)

servoMin = 150  # Min pulse length out of 4096
servoMax = 650  # Max pulse length out of 4096

sv_max = 420
sv_min = 150
sf_max = 650
sf_min = 150
sb_max = 650
sb_min = 150

servo_vertical = sv_min
servo_front = sf_min
servo_back = sb_max

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def handleKeypress(event):
  pressedKey = event.char
  print pressedKey

def yourFunction(event):
  if event.char == event.keysym:
    print('normal' + event.keysym)

  elif len(event.char) == 1 and event.keysym == 'KP_8':
    servoVerticalUp()
  elif len(event.char) == 1 and event.keysym == 'KP_2':
    servoVerticalDown()

  elif len(event.char) == 1 and event.keysym == 'KP_7':
    servoForwardIn()
  elif len(event.char) == 1 and event.keysym == 'KP_9':
    servoForwardOut()

  elif len(event.char) == 1 and event.keysym == 'KP_1':
    servoBackwardIn()
  elif len(event.char) == 1 and event.keysym == 'KP_3':
    servoBackwardOut()
    
  elif len(event.char) == 1:
    print('punctuation' + event.keysym)
#  elif event.keysym == 'Up':
#    print('going up')
#  elif event.keysym == 'Down':
#    print('going down')
  else:
    print('special' + event.keysym)
  
  positionServos()
  
def servoVerticalUp():
  global servo_vertical
  servo_vertical = servo_vertical + 50

def servoVerticalDown():
  global servo_vertical
  servo_vertical = servo_vertical - 50

def servoForwardOut():
  global servo_front
  servo_front = servo_front - 50

def servoForwardIn():
  global servo_front
  servo_front = servo_front + 50

def servoBackwardOut():
  global servo_back
  servo_back = servo_back + 50

def servoBackwardIn():
  global servo_back
  servo_back = servo_back - 50

def limitServoPositions():
  global servo_vertical
  global servo_front
  global servo_back

  if servo_vertical < sv_min:
    servo_vertical = sv_min
  if servo_vertical > sv_max:
    servo_vertical = sv_max
  if servo_front < sf_min:
    servo_front = sf_min
  if servo_front > sf_max:
    servo_front = sf_max
  if servo_back < sb_min:
    servo_back = sb_min
  if servo_back > sb_max:
    servo_back = sb_max
  
def positionServos():
  limitServoPositions()
  pwm.setPWM(0, 0, servo_vertical)
  pwm.setPWM(1, 0, servo_front)
  pwm.setPWM(2, 0, servo_back)

    
def main(argv):
  opts, args = getopt.getopt(argv, "s:p:f:", ["servo=", "pos=", "freq="])
  servoNumber = 0
  position = 0
  freq = 60

  for opt, arg in opts:
    if opt in ("-s", "--servo"):
      servoNumber = int(arg)
    if opt in ("-p", "--pos"):
      position = int(arg)
    if opt in ("-f", "--freq"):
      freq = int(arg)

  if (position < servoMin):
    position = servoMin
  if (position > servoMax):
    position = servoMax
    
  print "servo:" + str(servoNumber)
  print "position:" + str(position)
  print "freq:" + str(freq)

  pwm.setPWMFreq(freq)                        # Set frequency to 60 Hz
  pwm.setPWM(servoNumber, 0, position)


  root = Tk()
  frame = Frame(root, width=100, height=100)
  #frame.bind("<Left>",yourFunction)   #Binds the "left" key to the frame and exexutes yourFunction if "left" key was pressed
  root.bind_all("<Key>",yourFunction)
  l = Label(frame, text="Hello, world!\nTkinter on PocketPC!\nSee http://pythonce.sf.net.")
  b = Button(frame, text='Quit', command=root.destroy)
  l.pack()
  b.pack()
  frame.pack()

  root.mainloop()

  
  #while (True):
    # Change speed of continuous servo on channel O
    #pwm.setPWM(servoNumber, 0, position)
    #pwm.setPWM(1, 0, servoMin)
    #time.sleep(0.6)
    #pwm.setPWM(0, 0, servoMax)
    #pwm.setPWM(1, 0, servoMax)
    #time.sleep(0.6)

if __name__ == "__main__":
    main(sys.argv[1:])

