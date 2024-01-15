import time
# import RPi.GPIO as GPIO
from Player import *
import keyboard

class Game:
  def __init__(self, rounds: int, pin: int):
    self.__rounds = rounds
    self.__button = pin
    self.__player = Player("Flo", False)
    self.__cpu = Player("CPU", True)

    self.__currentRound = 1
    self.__currentPlayer = self.__player

    self.__running = True

  def start(self):
    try:
      # GPIO.setmode(GPIO.BCM)
      # GPIO.setwarnings(False)
      # GPIO.setup(self.__button, GPIO.IN)

      while self.__running:
        if self.__currentRound > self.__rounds:
          self.__running = False
          break

        self.__player.reset()
        self.__cpu.reset()

        self.__currentPlayer = self.__player
        self.__turn()

        if self.__player.getPoints() == 21:
          print("Reached 21 points! Player wins round!")
          self.__player.incrementScore()
          self.__currentRound += 1
          continue

        if self.__player.getPoints() > 21:
          print("Went over 21 points! CPU wins round!")
          self.__cpu.incrementScore()
          self.__currentRound += 1
          time.sleep(0.5)
          continue

        if self.__player.getPoints() < 16:
          print("Under 16 points rolled! CPU wins round!")
          self.__cpu.incrementScore()
          self.__currentRound += 1
          time.sleep(0.5)
          continue

        self.__currentPlayer = self.__cpu
        self.__turn()

        if self.__cpu.getPoints() > 21:
          print("CPU went over 21 points! Player wins round!")
          self.__player.incrementScore()
          self.__currentRound += 1
          continue

        if self.__player.getPoints() < self.__cpu.getPoints():
          print("CPU has more points than Player! CPU wins round!")
          self.__cpu.incrementScore()
          self.__currentRound += 1
          continue

        print("Player has more points than CPU! Player wins round!")
        self.__player.incrementScore()
        self.__currentRound += 1
        continue

      self.__determineWinner()

    except KeyboardInterrupt:
      self.__running = False
    finally:
      pass
      # GPIO.cleanup()

  def __turn(self):
    print("Turn start: " + self.__currentPlayer.getName())

    while True:
      print(self.__currentPlayer.getName() + " points: " + str(self.__currentPlayer.getPoints()))

      if self.__currentPlayer.getPoints() >= 21:
        break

      if not self.__currentPlayer.isCpu():
        if self.__getClicks() >= 2:
          break

      if self.__currentPlayer.isCpu() and self.__cpu.getPoints() > self.__player.getPoints():
        break;

      self.__currentPlayer.roll()

  def __getClicks(self):
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
  
  def __determineWinner(self):
    playerScore = self.__player.getScore()
    cpuScore = self.__cpu.getScore()

    print("Player-score: " + str(playerScore))
    print("CPU-score:    " + str(cpuScore))

    if playerScore > cpuScore:
      self.__player.win()
    
    if playerScore < cpuScore:
      self.__cpu.win()


  
