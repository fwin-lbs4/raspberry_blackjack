import random
import time

class Player:
  def __init__(self, name: str, cpu: bool, test: bool = False):
    self.__name = name
    self.__score = 0
    self.__points = 18 if test and not cpu else 0
    self.__cpu = cpu
    self.__test = test

  def getName(self):
    return self.__name

  def isCpu(self):
    return self.__cpu
  
  def reset(self):
    self.__points = 18 if self.__test and not self.__cpu else 0
  
  def roll(self):
    delay = 0.05 if self.__cpu else 0.125
    rolls = random.randint(16, 32)

    number = 0

    for roll in range(0, rolls):
      number = random.randint(1, 6)
      if not self.__test:
        print("Rolling...", str(number), end='\r' if roll < (rolls - 1) else '\n')

      if not self.__test:
        time.sleep(delay)

    if not self.__test:
      print(self.__name, "rolled a", str(number))
    self.addPoints(number)

  def addPoints(self, roll: int):
    if roll > 6:
      self.__points += 6
      return

    if roll < 1:
      self.__points += 1
      return

    self.__points += roll
    return

  def getPoints(self):
    return self.__points

  def incrementScore(self):
    self.__score += 1

  def getScore(self):
    return self.__score
