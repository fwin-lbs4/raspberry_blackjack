import signal
import RPi.GPIO as GPIO

class clickHandler:
  def __init__(self, singleClickFunc: Callable, doubleClickFunc: Callable, pin: int):
    self.__singleClickFunc = singleClickFunc
    self.__doubleClickFunc = doubleClickFunc
    self.__pin = pin
    self.__counter = 0
    self.__listenForClicks = False
    self.__firstClickDone = False

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(self.__pin, GPIO.IN, GPIO.PUD_UP)

    GPIO.add_event_detect(self.__pin, GPIO.FALLING, self.__click, bouncetime=300)

    

  def __reset(self):
    self.__counter = 0
    self.__firstClickDone = False

  def __handleSingleClick(self):
    if self.__listenForClicks == False:
      self.__reset()
      return

    if self.__counter == 1:
      self.__reset()
      self.__singleClickFunc()


  def __click(self):
    if self.__listenForClicks == False:
      self.__reset()
      return

    self.__counter = self.__counter + 1

    if self.__firstClickDone == False:
      self.__firstClickDone = True

      signal.signal(signal.SIGALRM, self.__handleSingleClick)

      signal.alarm(0.5)

    if self.__counter == 2:
      self.__reset()
      self.__doubleClickFunc()

  def start(self):
    self.__reset()
    self.__listenForClicks = True

  def stop(self):
    self.__reset()
    self.__listenForClicks = False

  def __del__(self):
    GPIO.cleanup()