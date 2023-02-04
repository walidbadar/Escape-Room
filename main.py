import os, subprocess, threading, time
import RPi.GPIO as GPIO
# import OPi.GPIO as GPIO
import pygame
import datetime as dt
import vlc
from pydub import AudioSegment
from pydub.playback import play

pygame.init()
pygame.mixer.init()

data = ''
startTime = 0
endTime = 0
timeFlag = 0
path = "/home/nathan41/Desktop/"
language = "English"
languagePriority = 0
buttonDelay = 3000

# Audio Varaibles
audioFormat = "wav"
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
    GPIO.setup(selectEnglishLanguage, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(selectDutchLanguage, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(escapeRoom, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(power, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(lifeSupport, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(engine, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(navigation, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def selectEnglishThread(thread=None):
    global language, languagePriority

    GPIO.remove_event_detect(selectEnglishLanguage)

    if GPIO.input(selectEnglishLanguage) == 1 and languagePriority == 0:
        language = 'English'
        languagePriority = 1
        GPIO.remove_event_detect(selectDutchLanguage)

    elif GPIO.input(selectEnglishLanguage) == 0 and languagePriority == 1:
        pygame.mixer.music.stop()
        languagePriority = 0
        GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)

    GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)
    print(language)


def selectDutchThread(thread=None):
    global language, languagePriority

    GPIO.remove_event_detect(selectDutchLanguage)

    if GPIO.input(selectDutchLanguage) == 1 and languagePriority == 0:
        language = 'Dutch'
        languagePriority = 1
        GPIO.remove_event_detect(selectEnglishLanguage)

    elif GPIO.input(selectDutchLanguage) == 0 and languagePriority == 1:
        pygame.mixer.music.stop()
        languagePriority = 0
        GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)

    GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)
    print(language)


def escapeRoomThread(thread=None):
    global startTime, endTime, timeFlag

    GPIO.remove_event_detect(escapeRoom)

    def deadThread():
        if language == 'English':
            pygame.mixer.music.stop()
            deadAudioMP3 = path + language + "/Escape room Nathan Dead (Engels) FINAL." + audioFormat
            deadAudioFile = AudioSegment.from_file(deadAudioMP3, format=audioFormat)
            deadAudioLen = len(deadAudioFile)/1000
            deadAudio = play(deadAudioFile)
            time.sleep(deadAudioLen)

        elif language == 'Dutch':
            pygame.mixer.music.stop()
            deadAudioMP3 = path + language + "/Escape room Nathan Dood (NL) FINAL." + audioFormat
            deadAudioFile = AudioSegment.from_file(deadAudioMP3, format=audioFormat)
            deadAudioLen = len(deadAudioFile)/1000
            deadAudio = play(deadAudioFile)
            time.sleep(deadAudioLen)

    if GPIO.input(escapeRoom) == 1:
        print("Escape Room Started")
        threading.Timer(3600, deadThread).start()

        if language == 'English':
            pygame.mixer.music.load(path + language + "/Escape room Nathan (ENGELS) FINAL." + audioFormat)

        elif language == 'Dutch':
            pygame.mixer.music.load(path + language + "/Escape room Nathan (NL) FINAL." + audioFormat)

        pygame.mixer.music.play()

    GPIO.add_event_detect(escapeRoom, GPIO.RISING, callback=escapeRoomThread, bouncetime=buttonDelay)


def startThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    GPIO.remove_event_detect(start)

    if GPIO.input(start) == 1:
        print("All Systems Repaired")
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
            startAudioMP3 = path + language + "/All Systems Repaired (Engels) FINAL." + audioFormat
            startAudioFile = AudioSegment.from_file(startAudioMP3, format=audioFormat)
            startAudioLen = len(startAudioFile)/1000

        elif language == 'Dutch':
            startAudioMP3 = path + language + "/Alles gerepareerd (NL) FINAL." + audioFormat
            startAudioFile = AudioSegment.from_file(startAudioMP3, format=audioFormat)
            startAudioLen = len(startAudioFile)/1000

        startAudio = play(startAudioFile)
        print(startAudioLen)
        time.sleep(startAudioLen)
        startAudio = ''
        pygame.mixer.music.unpause()

    GPIO.add_event_detect(start, GPIO.RISING, callback=startThread, bouncetime=buttonDelay)


def powerThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    GPIO.remove_event_detect(power)

    if GPIO.input(power) == 1:
        print("Power Repaired")
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
            powerAudioMP3 = path + language + "/Power Repaired (Engels) FINAL." + audioFormat
            powerAudioFile = AudioSegment.from_file(powerAudioMP3, format=audioFormat)
            powerAudioLen = len(powerAudioFile)/1000

        elif language == 'Dutch':
            powerAudioMP3 = path + language + "/Stroom gerepareerd (NL) FINAL." + audioFormat
            powerAudioFile = AudioSegment.from_file(powerAudioMP3, format=audioFormat)
            powerAudioLen = len(powerAudioFile)/1000

        powerAudio = play(powerAudioFile)
        print(powerAudioLen)
        time.sleep(powerAudioLen)
        powerAudio = ''
        pygame.mixer.music.unpause()

    GPIO.add_event_detect(power, GPIO.RISING, callback=powerThread, bouncetime=buttonDelay)


def lifeSupportThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    GPIO.remove_event_detect(lifeSupport)

    if GPIO.input(lifeSupport) == 1:
        print("Life Support Repaired")
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
            lifeSupportAudioMP3 = path + language + "/Life Support Repaired (Engels) FINAL." + audioFormat
            lifeSupportAudioFile = AudioSegment.from_file(lifeSupportAudioMP3, format=audioFormat)
            lifeSupportAudioLen = len(lifeSupportAudioFile)/1000

        elif language == 'Dutch':
            lifeSupportAudioMP3 = path + language + "/Zuurstof gerepareerd (NL) FINAL." + audioFormat
            lifeSupportAudioFile = AudioSegment.from_file(lifeSupportAudioMP3, format=audioFormat)
            lifeSupportAudioLen = len(lifeSupportAudioFile)/1000

        lifeSupportAudio = play(lifeSupportAudioFile)
        print(lifeSupportAudioLen)
        time.sleep(lifeSupportAudioLen)
        lifeSupportAudio = ''
        pygame.mixer.music.unpause()

    GPIO.add_event_detect(lifeSupport, GPIO.RISING, callback=lifeSupportThread, bouncetime=buttonDelay)

def engineThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    GPIO.remove_event_detect(engine)

    if GPIO.input(engine) == 1:
        print("Engine Repaired")
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
            engineAudioMP3 = path + language + "/Engines Repaired (Engels) FINAL." + audioFormat
            engineAudioFile = AudioSegment.from_file(engineAudioMP3, format=audioFormat)
            engineAudioLen = len(engineAudioFile)/1000

        elif language == 'Dutch':
            engineAudioMP3 = path + language + "/Motoren gerepareerd (NL) FINAL." + audioFormat
            engineAudioFile = AudioSegment.from_file(engineAudioMP3, format=audioFormat)
            engineAudioLen = len(engineAudioFile)/1000

        engineAudio = play(engineAudioFile)
        print(engineAudioLen)
        time.sleep(engineAudioLen)
        engineAudio = ''
        pygame.mixer.music.unpause()

    GPIO.add_event_detect(engine, GPIO.RISING, callback=engineThread, bouncetime=buttonDelay)


def navigationThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio

    GPIO.remove_event_detect(navigation)

    if GPIO.input(navigation) == 1:
        print("Navigation Repaired")
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
            navigationAudioMP3 = path + language + "/Navigation Repaired (Engels) FINAL." + audioFormat
            navigationAudioFile = AudioSegment.from_file(navigationAudioMP3, format=audioFormat)
            navigationAudioLen = len(navigationAudioFile)/1000

        elif language == 'Dutch':
            navigationAudioMP3 = path + language + "/Navigatie gerepareerd (NL) FINAL." + audioFormat
            navigationAudioFile = AudioSegment.from_file(navigationAudioMP3, format=audioFormat)
            navigationAudioLen = len(navigationAudioFile)/1000

        navigationAudio = play(navigationAudioFile)
        print(navigationAudioLen)
        time.sleep(navigationAudioLen)
        navigationAudio = ''
        pygame.mixer.music.unpause()

    GPIO.add_event_detect(navigation, GPIO.RISING, callback=navigationThread, bouncetime=buttonDelay)


def loop():
    GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(escapeRoom, GPIO.RISING, callback=escapeRoomThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(start, GPIO.RISING, callback=startThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(power, GPIO.RISING, callback=powerThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(lifeSupport, GPIO.RISING, callback=lifeSupportThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(engine, GPIO.RISING, callback=engineThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(navigation, GPIO.RISING, callback=navigationThread, bouncetime=buttonDelay)

    while True:
        pass  # Don't do anything, sit forever


if __name__ == '__main__':
    setup()
    try:
        print("Program Started")
        loop()
    except:
        print("Error")
    finally:
        GPIO.cleanup()
