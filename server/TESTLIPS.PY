import time
from ohbot import ohbot

robot = ohbot.reset()


while 1:
    ohbot.move(ohbot.TOPLIP, 10, 10)
    ohbot.move(ohbot.BOTTOMLIP, 10,10)
    time.sleep(0.3)
    ohbot.move(ohbot.TOPLIP, 5, 10)
    ohbot.move(ohbot.BOTTOMLIP, 5,10)
    time.sleep(0.3)
    #time.sleep(2)  # Wait for the remaining time to complete 10 seconds