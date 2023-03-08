import os, subprocess, threading, time
import RPi.GPIO as GPIO
# import OPi.GPIO as GPIO
import pygame
from pydub import AudioSegment
from pydub.playback import play

pygame.init()
pygame.mixer.init()

startTime = 0
endTime = 0
timeFlag = 0
path = "/home/nathan41/Desktop/"
language = "English"
buttonDelay = 100

# Audio Varaibles
audioFormat = 'wav'
escapeRoomAudio = ''
deadAudio = ''
startAudio = ''
powerAudio = ''
lifeSupportAudio = ''
engineAudio = ''
navigationAudio = ''

# GPIO Varaibles
selectEnglishLanguage = 13
selectDutchLanguage = 16
escapeRoom = 19
dead = 26
start = 20
power = 21
lifeSupport = 12
engine = 5
navigation = 6

# GPIO Detection
startFlag = 0
escapeRoomBtnPressed = 0
startBtnPressed = 0
powerBtnPressed = 0
lifeSupportBtnPressed = 0
engineBtnPressed = 0
navigationBtnPressed = 0


def setup():
    # Orange Pi Zero Board
    # GPIO.setboard(GPIO.ZERO)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(selectEnglishLanguage, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(selectDutchLanguage, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(escapeRoom, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dead, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(power, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(lifeSupport, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(engine, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(navigation, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def selectEnglishThread(thread=None):
    global startFlag, language

    if GPIO.input(selectEnglishLanguage) == 1:
        startFlag = 1
        language = 'English'
        GPIO.remove_event_detect(selectDutchLanguage)

    elif GPIO.input(selectEnglishLanguage) == 0:
        startFlag = 0
        pygame.mixer.music.stop()
        GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)

    print(language)


def selectDutchThread(thread=None):
    global startFlag, language

    if GPIO.input(selectDutchLanguage) == 1:
        startFlag = 1
        language = 'Dutch'
        GPIO.remove_event_detect(selectEnglishLanguage)

    elif GPIO.input(selectDutchLanguage) == 0:
        startFlag = 0
        pygame.mixer.music.stop()
        GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)

    print(language)


def escapeRoomThread(thread=None):
    global startTime, endTime, timeFlag

    print("Escape Room Started")

    if language == 'English':
        pygame.mixer.music.load(path + language + "/Escape room Nathan (ENGELS) FINAL.mp3")

    elif language == 'Dutch':
        pygame.mixer.music.load(path + language + "/Escape room Nathan (NL) FINAL.mp3")

    if startFlag == 1 and GPIO.input(escapeRoom) == 1:
        pygame.mixer.music.play()

    else:
        print("Audio Stopped")
        pygame.mixer.music.stop()


def deadThread(thread=None):
    global deadAudio, startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(dead) == 1:
        print("Playing Dead")
        GPIO.remove_event_detect(dead)

        if language == 'English':
            deadAudioFormat = path + language + "/Escape room Nathan Dead (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            deadAudioFormat = path + language + "/Escape room Nathan Dood (NL) FINAL." + audioFormat

        deadAudioFile = AudioSegment.from_wav(deadAudioFormat)
        pygame.mixer.music.stop()
        deadAudio = play(deadAudioFile)
        deadAudio = ''

        GPIO.add_event_detect(dead, GPIO.RISING, callback=deadThread, bouncetime=buttonDelay)

    else:
        deadAudio = ''


def startThread(thread=None):
    global deadAudio, startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(start) == 1:
        print("All Systems Repaired")
        GPIO.remove_event_detect(start)

        if language == 'English':
            startAudioFormat = path + language + "/All Systems Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            startAudioFormat = path + language + "/Alles gerepareerd (NL) FINAL." + audioFormat

        startAudioFile = AudioSegment.from_wav(startAudioFormat)
        pygame.mixer.music.pause()
        startAudio = play(startAudioFile)
        startAudio = ''
        pygame.mixer.music.unpause()

        GPIO.add_event_detect(start, GPIO.RISING, callback=startThread, bouncetime=buttonDelay)

    else:
        startAudio = ''


def powerThread(thread=None):
    global deadAudio, startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(power) == 1:
        print("Power Repaired")
        GPIO.remove_event_detect(power)

        if language == 'English':
            powerAudioFormat = path + language + "/Power Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            powerAudioFormat = path + language + "/Stroom gerepareerd (NL) FINAL." + audioFormat

        powerAudioFile = AudioSegment.from_wav(powerAudioFormat)
        pygame.mixer.music.pause()
        powerAudio = play(powerAudioFile)
        powerAudio = ''
        pygame.mixer.music.unpause()

        GPIO.add_event_detect(power, GPIO.RISING, callback=powerThread, bouncetime=buttonDelay)

    else:
        powerAudio = ''


def lifeSupportThread(thread=None):
    global deadAudio, startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(lifeSupport) == 1:
        print("Life Support Repaired")
        GPIO.remove_event_detect(lifeSupport)

        if language == 'English':
            lifeSupportAudioFormat = path + language + "/Life Support Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            lifeSupportAudioFormat = path + language + "/Zuurstof gerepareerd (NL) FINAL." + audioFormat

        lifeSupportAudioFile = AudioSegment.from_wav(lifeSupportAudioFormat)
        pygame.mixer.music.pause()
        lifeSupportAudio = play(lifeSupportAudioFile)
        lifeSupportAudio = ''
        pygame.mixer.music.unpause()

        GPIO.add_event_detect(lifeSupport, GPIO.RISING, callback=lifeSupportThread, bouncetime=buttonDelay)

    else:
        lifeSupportAudio = ''


def engineThread(thread=None):
    global deadAudio, startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(engine) == 1:
        print("Engine Repaired")
        GPIO.remove_event_detect(engine)

        if language == 'English':
            engineAudioFormat = path + language + "/Engines Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            engineAudioFormat = path + language + "/Motoren gerepareerd (NL) FINAL." + audioFormat

        engineAudioFile = AudioSegment.from_wav(engineAudioFormat)
        pygame.mixer.music.pause()
        engineAudio = play(engineAudioFile)
        engineAudio = ''
        pygame.mixer.music.unpause()

        GPIO.add_event_detect(engine, GPIO.RISING, callback=engineThread, bouncetime=buttonDelay)

    else:
        engineAudio = ''


def navigationThread(thread=None):
    global deadAudio, startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    if GPIO.input(navigation) == 1:
        print("Navigation Repaired")
        GPIO.remove_event_detect(navigation)

        if language == 'English':
            navigationAudioFormat = path + language + "/Navigation Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            navigationAudioFormat = path + language + "/Navigatie gerepareerd (NL) FINAL." + audioFormat

        navigationAudioFile = AudioSegment.from_wav(navigationAudioFormat)
        pygame.mixer.music.pause()
        navigationAudio = play(navigationAudioFile)
        navigationAudio = ''
        pygame.mixer.music.unpause()

        GPIO.add_event_detect(navigation, GPIO.RISING, callback=navigationThread, bouncetime=buttonDelay)

    else:
        navigationAudio = ''


def loop():
    GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(escapeRoom, GPIO.BOTH, callback=escapeRoomThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(dead, GPIO.RISING, callback=deadThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(start, GPIO.RISING, callback=startThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(power, GPIO.RISING, callback=powerThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(lifeSupport, GPIO.RISING, callback=lifeSupportThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(engine, GPIO.RISING, callback=engineThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(navigation, GPIO.RISING, callback=navigationThread, bouncetime=buttonDelay)

    while True:
        pass


if __name__ == '__main__':
    setup()
    try:
        print("Program Started")
        loop()
    except:
        print("Error")
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
