import RPi.GPIO as GPIO
import signal

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

clicks = 0

listeningForClicks = false
playerActive = true

try:
  def roll():
    # roll

  def nextRound():
    # nextRound

  def handleClick():
    global clicks, listeningForClicks

    if clicks == 1:
      clicks = 0
      listeningForClicks = false
      roll()

  def click():
    global clicks, playerActive, listeningForClicks

    if playerActive == false:
      return
    
    clicks = clicks + 1

    if listeningForClicks == false:
      listeningForClicks = true

      signal.signal(signal.SIGALRM, handleClick)

      signal.alarm(2)

    if clicks == 2:
      clicks = 0
      listeningForClicks = false
      nextRound()

  GPIO.setup(5, GPIO.IN, GPIO.PUD_UP)

  GPIO.add_event_detect(5, GPIO.FALLING, handleClick, bouncetime=300)

  signal.pause()
except KeyboardInterrupt:
  GPIO.cleanup()
  raise SystemExit

