import time
import RPi.GPIO as GPIO
import Player

class Game:
  def __init__(self, rounds: int, pin: int):
    self.__rounds = rounds
    self.__button = pin
    self.__player = Player("Flo", False)
    self.__cpu = Player("CPU", True)

    self.__currentRound = 0
    self.__currentPlayer = self.__player

    self.__running = True

  def start(self):
    try:
      GPIO.setmode(GPIO.BCM)
      GPIO.setwarnings(False)
      GPIO.setup(self.__button, GPIO.IN)

      while self.__running:
        if self.__currentRound is self.__rounds:
          self.__running = False
          break

        self.__currentPlayer = self.__player
        self.__turn()

        if self.__player.getPoints() == 21:
          self.__player.incrementScore()
          self.__currentRound += 1
          continue

        if self.__player.getPoints() < 21:
          self.__cpu.incrementScore()
          self.__currentRound += 1
          continue

        self.__currentPlayer = self.__cpu
        self.__turn()

        if self.__cpu.getPoints() < 21:
          self.__player.incrementScore()
          self.__currentRound += 1
          continue

        if self.__player.getPoints() < self.__cpu.getPoints():
          self.__cpu.incrementScore()
          self.__currentRound += 1
          continue

        self.__player.incrementScore()
        self.__currentRound += 1
        continue

      self.__determineWinner()

    except KeyboardInterrupt:
      self.__running = False
    finally:
      GPIO.cleanup()

  def __turn(self):
    while True:
      print(self.__currentPlayer.getName(), " points: ", self.__currentPlayer.getPoints())

      if self.__currentPlayer.getPoints() >= 21:
        break

      if not self.__currentPlayer.isCpu():
        if self.__getClicks() >= 2:
          break

      if self.__currentPlayer.isCpu() and self.__cpu.getPoints() < self.__player.getPoints():
        break;

      self.__currentPlayer.roll()

  def __getClicks(self):
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
  
  def __determineWinner(self):
    playerScore = self.__player.getScore()
    cpuScore = self.__player.getScore()

    if playerScore > cpuScore:
      self.__player.won()
    
    if playerScore < cpuScore:
      self.__cpu.won()


  
