import random
import time

class Player:
  def __init__(self, name: str, cpu: bool):
    self.__name = name
    self.__score = 0
    self.__points = 0
    self.__cpu = cpu

  def getName(self):
    return self.__name

  def isCpu(self):
    return self.__cpu
  
  def roll(self):
    print("Rolling...")
    time.sleep(0.5)
    number = random.randint(1, 6)
    print(self.__name, " rolled a ", number)
    self.addPoints(random.randint(1, 6))
    time.sleep(1)

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
    self.__score = self.__score + 1

  def getScore(self):
    return self.__score

  def win(self):
    print("Congratulations ", self.__name, "! You won!")

  def loose(self):
    if self.__cpu:
      self.__points = 22
