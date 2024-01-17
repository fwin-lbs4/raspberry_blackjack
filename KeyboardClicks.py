import time
import keyboard

class Clicks:
  def __init__(self, test: bool = False):
    self.__test = test

  def setup(self):
    pass

  def cleanup(self):
    pass

  def getClicks(self):
    print("Press once to roll, press twice to end your turn!")

    while not keyboard.is_pressed("space"):
      time.sleep(0.05)
    state = True
    prev_state = True
    first_click = time.time()

    while time.time() < first_click + 0.3:
      prev_state = state

      state = keyboard.is_pressed("space")

      if state and not prev_state:
        return 2

      time.sleep(0.015)

    return 1