import time
import RPi.GPIO as GPIO

class Clicks:
  def __init__(self, test: bool = False):
    self.__test = test

  def setup(self):
    if not self.__test:
      GPIO.setmode(GPIO.BOARD)
      GPIO.setwarnings(False)
      GPIO.setup(self.__button, GPIO.IN)

  def cleanup(self):
    if not self.__test:
      GPIO.cleanup()

  def getClicks(self):
    print("Press once to roll, press twice to end your turn!")

    while GPIO.input(self.__button) is not GPIO.LOW:
      time.sleep(0.05)
    state = True
    prev_state = True
    first_click = time.time()

    while time.time() < first_click + 0.3:
      prev_state = state

      state = GPIO.input(self.__button) is GPIO.LOW

      if state and not prev_state:
        return 2

      time.sleep(0.015)

    return 1