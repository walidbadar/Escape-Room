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
buttonDelay = 3000
deadTimer = ''

# Audio Varaibles
audioFormat = 'wav'
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

# GPIO Detection
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
    GPIO.setup(start, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(power, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(lifeSupport, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(engine, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(navigation, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def selectEnglishThread(thread=None):
    global language, deadTimer

    GPIO.remove_event_detect(selectEnglishLanguage)

    if GPIO.input(selectEnglishLanguage) == 1:
        language = 'English'
        GPIO.remove_event_detect(selectDutchLanguage)

    elif GPIO.input(selectEnglishLanguage) == 0:
        pygame.mixer.music.stop()
        if deadTimer != '':
            deadTimer.cancel()
        GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)

    GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)
    print(language)


def selectDutchThread(thread=None):
    global language, deadTimer

    GPIO.remove_event_detect(selectDutchLanguage)

    if GPIO.input(selectDutchLanguage) == 1:
        language = 'Dutch'
        GPIO.remove_event_detect(selectEnglishLanguage)

    elif GPIO.input(selectDutchLanguage) == 0:
        pygame.mixer.music.stop()
        if deadTimer != '':
            deadTimer.cancel()
        GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)

    GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)
    print(language)


def escapeRoomThread(thread=None):
    global startTime, endTime, timeFlag, deadTimer
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    def deadThread():
        if language == 'English':
            pygame.mixer.music.stop()
            deadAudioFormat = path + language + "/Escape room Nathan Dead (Engels) FINAL." + audioFormat
            deadAudioFile = AudioSegment.from_wav(deadAudioFormat)
            deadAudioLen = len(deadAudioFile)/1000.0
            deadAudio = play(deadAudioFile)
            time.sleep(deadAudioLen)

        elif language == 'Dutch':
            pygame.mixer.music.stop()
            deadAudioFormat = path + language + "/Escape room Nathan Dood (NL) FINAL." + audioFormat
            deadAudioFile = AudioSegment.from_wav(deadAudioFormat)
            deadAudioLen = len(deadAudioFile)/1000.0
            deadAudio = play(deadAudioFile)
            time.sleep(deadAudioLen)

    escapeRoomBtnPressed = escapeRoomBtnPressed + 1

    if escapeRoomBtnPressed == 1:
        print("Escape Room Started")
        deadTimer = threading.Timer(3600, deadThread)
        deadTimer.start()

        if language == 'English':
            pygame.mixer.music.load(path + language + "/Escape room Nathan (ENGELS) FINAL." + audioFormat)

        elif language == 'Dutch':
            pygame.mixer.music.load(path + language + "/Escape room Nathan (NL) FINAL." + audioFormat)

        pygame.mixer.music.play()


def startThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    startBtnPressed = startBtnPressed + 1

    if startBtnPressed == 1:
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
            startAudioFormat = path + language + "/All Systems Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            startAudioFormat = path + language + "/Alles gerepareerd (NL) FINAL." + audioFormat

        startAudioFile = AudioSegment.from_wav(startAudioFormat)
        startAudioLen = len(startAudioFile) / 1000.0
        startAudio = play(startAudioFile)
        print(startAudioLen)
        time.sleep(startAudioLen)
        startAudio = ''
        pygame.mixer.music.unpause()

    elif startBtnPressed > 1:
        time.sleep(0.1)

def powerThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    powerBtnPressed = powerBtnPressed + 1

    if powerBtnPressed == 1:
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
            powerAudioFormat = path + language + "/Power Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            powerAudioFormat = path + language + "/Stroom gerepareerd (NL) FINAL." + audioFormat

        powerAudioFile = AudioSegment.from_wav(powerAudioFormat)
        powerAudioLen = len(powerAudioFile) / 1000.0

        powerAudio = play(powerAudioFile)
        print(powerAudioLen)
        time.sleep(powerAudioLen)
        powerAudio = ''
        pygame.mixer.music.unpause()

    elif powerBtnPressed > 1:
        time.sleep(0.1)

def lifeSupportThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    lifeSupportBtnPressed = lifeSupportBtnPressed + 1

    if lifeSupportBtnPressed == 1:
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
            lifeSupportAudioFormat = path + language + "/Life Support Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            lifeSupportAudioFormat = path + language + "/Zuurstof gerepareerd (NL) FINAL." + audioFormat

        lifeSupportAudioFile = AudioSegment.from_wav(lifeSupportAudioFormat)
        lifeSupportAudioLen = len(lifeSupportAudioFile)/1000.0
        lifeSupportAudio = play(lifeSupportAudioFile)
        print(lifeSupportAudioLen)
        time.sleep(lifeSupportAudioLen)
        lifeSupportAudio = ''
        pygame.mixer.music.unpause()

    elif lifeSupportBtnPressed > 1:
        time.sleep(0.1)

def engineThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    engineBtnPressed = engineBtnPressed + 1
    print(engineBtnPressed)

    if engineBtnPressed == 1:
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
            engineAudioFormat = path + language + "/Engines Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            engineAudioFormat = path + language + "/Motoren gerepareerd (NL) FINAL." + audioFormat

        engineAudioFile = AudioSegment.from_wav(engineAudioFormat)
        engineAudioLen = len(engineAudioFile) / 1000.0

        engineAudio = play(engineAudioFile)
        print(engineAudioLen)
        time.sleep(engineAudioLen)
        engineAudio = ''
        pygame.mixer.music.unpause()

    elif engineBtnPressed > 1:
        time.sleep(0.1)

def navigationThread(thread=None):
    global startAudio, powerAudio, lifeSupportAudio, engineAudio, navigationAudio
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    navigationBtnPressed = navigationBtnPressed + 1

    if navigationBtnPressed == 1:
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
            navigationAudioFormat = path + language + "/Navigation Repaired (Engels) FINAL." + audioFormat

        elif language == 'Dutch':
            navigationAudioFormat = path + language + "/Navigatie gerepareerd (NL) FINAL." + audioFormat

        navigationAudioFile = AudioSegment.from_wav(navigationAudioFormat)
        navigationAudioLen = len(navigationAudioFile) / 1000.0
        navigationAudio = play(navigationAudioFile)
        print(navigationAudioLen)
        time.sleep(navigationAudioLen)
        navigationAudio = ''
        pygame.mixer.music.unpause()

    elif navigationBtnPressed > 1:
        time.sleep(0.1)

def loop():
    global escapeRoomBtnPressed, startBtnPressed, powerBtnPressed, lifeSupportBtnPressed, engineBtnPressed, navigationBtnPressed

    GPIO.add_event_detect(selectEnglishLanguage, GPIO.BOTH, callback=selectEnglishThread, bouncetime=buttonDelay)
    GPIO.add_event_detect(selectDutchLanguage, GPIO.BOTH, callback=selectDutchThread, bouncetime=buttonDelay)

    while True:
        if GPIO.input(escapeRoom) == 1:
            escapeRoomThread()
        else:
            escapeRoomBtnPressed = 0

        if GPIO.input(start) == 1:
            startThread()
        else:
            startBtnPressed = 0

        if GPIO.input(power) == 1:
            powerThread()
        else:
            powerBtnPressed = 0

        if GPIO.input(lifeSupport) == 1:
            lifeSupportThread()
        else:
            lifeSupportBtnPressed = 0

        if GPIO.input(engine) == 1:
            engineThread()
        else:
            engineBtnPressed = 0

        if GPIO.input(navigation) == 1:
            navigationThread()
        else:
            navigationBtnPressed = 0

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
