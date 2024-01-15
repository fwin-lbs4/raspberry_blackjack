import time
import RPi.GPIO as GPIO
from Player import *

class Game:
  def __init__(self, rounds: int, pin: int, player: str, test: bool = False):
    self.__rounds = rounds
    self.__button = pin
    self.__player = Player("Player" if player == "" else player, False, test)
    self.__cpu = Player("CPU", True, test)

    self.__currentRound = 1
    self.__currentPlayer = self.__player

    self.__running = True

    self.__test = test

  def start(self):
    try:
      GPIO.setmode(GPIO.BOARD)
      GPIO.setwarnings(False)
      GPIO.setup(self.__button, GPIO.IN)

      while self.__running:
        # if the last round has been played end the loop
        if self.__currentRound > self.__rounds:
          self.__running = False
          break

        print("Round", self.__currentRound, "start!" if not self.__test else "")

        # reset points of both players to 0
        self.__player.reset()
        self.__cpu.reset()

        # start as the player
        if not self.__test:
          self.__currentPlayer = self.__player
          self.__turn()

        # if the player has 21 points auto-win the player
        if self.__player.getPoints() == 21:
          if not self.__test:
            print("Reached 21 points! Player wins round!")
          self.__player.incrementScore()
          self.__currentRound += 1
          continue

        # if the player has more than 21 points auto-loose the player
        if self.__player.getPoints() > 21:
          if not self.__test:
            print("Went over 21 points! CPU wins round!")
          self.__cpu.incrementScore()
          self.__currentRound += 1

          if not self.__test:
            time.sleep(0.5)

          continue

        # if the player has less than 16 points also auto-loose the player, the cpu will always be able to win
        if self.__player.getPoints() < 16:
          if not self.__test:
            print("Under 16 points rolled! CPU wins round!")
          self.__cpu.incrementScore()
          self.__currentRound += 1

          if not self.__test:
            time.sleep(0.5)

          continue

        # start the cpu turn
        self.__currentPlayer = self.__cpu
        self.__turn()

        # if the cpu has over 21 points auto-loose the cpu
        if self.__cpu.getPoints() > 21:
          if not self.__test:
            print("CPU went over 21 points! Player wins round!")
          self.__player.incrementScore()
          self.__currentRound += 1

          if not self.__test:
            time.sleep(0.5)

          continue

        # if the cpu has more points than the player the cpu wins
        if self.__player.getPoints() < self.__cpu.getPoints():
          if not self.__test:
            print("CPU has more points than Player! CPU wins round!")
          self.__cpu.incrementScore()
          self.__currentRound += 1

          if not self.__test:
            time.sleep(0.5)

          continue

        # if none of the above statements happened then the player wins this round
        if not self.__test:
          print("Player has more points than CPU! Player wins round!")
        self.__player.incrementScore()
        self.__currentRound += 1

        if not self.__test:
          time.sleep(0.5)

      # after the loop check who is the winner
      self.__determineWinner()

    except KeyboardInterrupt:
      self.__running = False
    finally:
      GPIO.cleanup()

  def __turn(self):
    if not self.__test:
      print("Turn start: " + self.__currentPlayer.getName())

    while True:
      if not self.__test:
        print(self.__currentPlayer.getName() + " points: " + str(self.__currentPlayer.getPoints()))

      # if the currentPlayer is at 21 or more points end the turn
      if self.__currentPlayer.getPoints() >= 21:
        break

      # if the player clicks the button twice end the round
      if not self.__currentPlayer.isCpu() and self.__getClicks() >= 2:
        break

      # if it's the cpu turn and the cpu has more points than the player end the turn
      if self.__currentPlayer.isCpu() and self.__cpu.getPoints() > self.__player.getPoints():
        break;

      # roll for the currentPlayer
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
    cpuScore = self.__cpu.getScore()

    print("Player-score: " + str(playerScore))
    print("CPU-score:    " + str(cpuScore))

    winner = self.__player.getName() if playerScore > cpuScore else self.__cpu.getName()

    print(winner + " has won! Congratulations!")

    if self.__test:
      winnerScore = playerScore if playerScore > cpuScore else cpuScore
      percent = (float(winnerScore) / float(self.__rounds)) * 100
      print(winner, "has won", str(round(percent, 2)) + "%", "of rounds!")