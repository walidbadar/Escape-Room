import os, subprocess, threading, time
import RPi.GPIO as GPIO
# import OPi.GPIO as GPIO
import pygame
import datetime as dt

pygame.init()
pygame.mixer.init()

data = ''
startTime = 0
endTime = 0
timeFlag = 0
path = "/home/pi/Desktop/"
language = "English"
languagePriority = 0

# Audio Varaibles
startAudio = ''
powerAudio = ''
lifeSupportAudio = ''
engineAudio = ''
navigationAudio = ''

# GPIO Varaibles
selectEnglishLanguage = 13
selectDutchLanguage = 16
escapeRoom = 19
start = 20
power = 21
lifeSupport = 12
engine = 5
navigation = 6


def setup():
    # Orange Pi Zero Board
    # GPIO.setboard(GPIO.ZERO)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setup(selectEnglishLanguage, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(selectDutchLanguage, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(power, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(lifeSupport, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(engine, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(navigation, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def selectEnglishThread():
    global language, languagePriority

    GPIO.remove_event_detect(selectDutchLanguage)

    if GPIO.input(selectEnglishLanguage) == 1 and languagePriority == 0:
        language = 'English'
        languagePriority = 1

    if GPIO.input(selectEnglishLanguage) == 0:
        languagePriority = 0
        GPIO.add_event_detect(selectDutchLanguage, GPIO.RISING, callback=selectDutchThread, bouncetime=1000)

    print(language)


def selectDutchThread():
    global language, languagePriority

    GPIO.remove_event_detect(selectEnglishLanguage)

    if GPIO.input(selectDutchLanguage) == 1 and languagePriority == 0:
        language = 'Dutch'
        languagePriority = 1

    if GPIO.input(selectDutchLanguage) == 0:
        languagePriority = 0
        GPIO.add_event_detect(selectEnglishLanguage, GPIO.RISING, callback=selectEnglishThread, bouncetime=1000)

    print(language)


def escapeRoomThread():
    global startTime, endTime, timeFlag

    if GPIO.input(escapeRoom) == 1:
        if timeFlag == 0:
            startTime = int(time.time())

        if timeFlag == 1:
            endTime = int(time.time())
            timeFlag = 0

        timeFlag = timeFlag + 1

        if language == 'English':
            pygame.mixer.music.load(path + language + "/Escape room Nathan (ENGELS) FINAL.mp3")

        elif language == 'Dutch':
            pygame.mixer.music.load(path + language + "/Escape room Nathan (NL) FINAL.mp3")

        pygame.mixer.music.play()


def startThread():
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if data == b'20':
        pygame.mixer.music.pause()

        if powerAudio != '':
            powerAudio.stop()

        if lifeSupportAudio != '':
            lifeSupportAudio.stop()

        if engineAudio != '':
            engineAudio.stop()

        if navigationAudio != '':
            navigationAudio.stop()

        if language == 'English':
            startAudio = pygame.mixer.Sound(path + language + "/All Systems Repaired (Engels) FINAL.mp3")

        elif language == 'Dutch':
            startAudio = pygame.mixer.Sound(path + language + "/Alles gerepareerd (NL) FINAL.mp3")

        startAudio.play()
        time.sleep(startAudio.get_length())
        pygame.mixer.music.unpause()


def powerThread():
    if GPIO.input(power) == 1:
        global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio
        pygame.mixer.music.pause()

        if startAudio != '':
            startAudio.stop()

        if lifeSupportAudio != '':
            lifeSupportAudio.stop()

        if engineAudio != '':
            engineAudio.stop()

        if navigationAudio != '':
            navigationAudio.stop()

        if language == 'English':
            powerAudio = pygame.mixer.Sound(path + language + "/Power Repaired (Engels) FINAL.mp3")

        elif language == 'Dutch':
            powerAudio = pygame.mixer.Sound(path + language + "/Stroom gerepareerd (NL) FINAL.mp3")

        powerAudio.play()
        time.sleep(powerAudio.get_length())
        pygame.mixer.music.unpause()


def lifeSupportThread():
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(lifeSupport) == 1:
        pygame.mixer.music.pause()

        if startAudio != '':
            startAudio.stop()

        if powerAudio != '':
            powerAudio.stop()

        if engineAudio != '':
            engineAudio.stop()

        if navigationAudio != '':
            navigationAudio.stop()

        if language == 'English':
            lifeSupportAudio = pygame.mixer.Sound(path + language + "/Life Support Repaired (Engels) FINAL.mp3")

        elif language == 'Dutch':
            lifeSupportAudio = pygame.mixer.Sound(path + language + "/Zuurstof gerepareerd (NL) FINAL.mp3")

        lifeSupportAudio.play()
        time.sleep(lifeSupportAudio.get_length())
        pygame.mixer.music.unpause()


def engineThread():
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(engine) == 1:
        pygame.mixer.music.pause()

        if startAudio != '':
            startAudio.stop()

        if powerAudio != '':
            powerAudio.stop()

        if lifeSupportAudio != '':
            lifeSupportAudio.stop()

        if navigationAudio != '':
            navigationAudio.stop()

        if language == 'English':
            engineAudio = pygame.mixer.Sound(path + language + "/Engines  Repaired (Engels) FINAL.mp3")

        elif language == 'Dutch':
            engineAudio = pygame.mixer.Sound(path + language + "/Motoren gerepareerd (NL) FINAL.mp3")

        engineAudio.play()
        time.sleep(engineAudio.get_length())
        pygame.mixer.music.unpause()


def naviagationThread():
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(navigation) == 1:
        pygame.mixer.music.pause()

        if startAudio != '':
            startAudio.stop()

        if powerAudio != '':
            powerAudio.stop()

        if lifeSupportAudio != '':
            lifeSupportAudio.stop()

        if engineAudio != '':
            engineAudio.stop()

        if language == 'English':
            navigationAudio = pygame.mixer.Sound(path + language + "/Navigation Repaired (Engels) FINAL.mp3")

        elif language == 'Dutch':
            navigationAudio = pygame.mixer.Sound(path + language + "/Navigatie gerepareerd (NL) FINAL.mp3")

        navigationAudio.play()
        time.sleep(navigationAudio.get_length())
        pygame.mixer.music.unpause()


def loop():
    GPIO.add_event_detect(selectEnglishLanguage, GPIO.RISING, callback=selectEnglishThread, bouncetime=1000)
    GPIO.add_event_detect(selectDutchLanguage, GPIO.RISING, callback=selectDutchThread, bouncetime=1000)
    GPIO.add_event_detect(start, GPIO.RISING, callback=startThread, bouncetime=1000)
    GPIO.add_event_detect(power, GPIO.RISING, callback=powerThread, bouncetime=1000)
    GPIO.add_event_detect(lifeSupport, GPIO.RISING, callback=lifeSupportThread, bouncetime=1000)
    GPIO.add_event_detect(engine, GPIO.RISING, callback=engineThread, bouncetime=1000)
    GPIO.add_event_detect(navigation, GPIO.RISING, callback=navigationThread, bouncetime=1000)

    while True:
        pass  # Don't do anything, sit forever


if __name__ == '__main__':
    setup()
    try:
        loop()
    except:
        GPIO.cleanup()
