import cv2
import numpy as np 
import pytesseract
import pyautogui
from time import sleep, time
from re import sub
import random

global supported_languages 
supported_languages = ['english', 'russian']

# Get text from screenshot
def getSceneText():
    # Logic taken from github user Misha91 repo called WoW-login-bot, big thanks for him!
    # Take screenshot
    image = np.array(pyautogui.screenshot())
    image = image[:, :, ::-1].copy()
    width, height = image.shape[:2]
    cntY, cntX = width//2, height//2
    minX, minY, maxY = int(cntX - 0.5*cntX), int(cntY - 0.75*cntY), int(cntY + 0.9*cntY)
    roi = image[minY:maxY, minX:]
    # Get only yellow text
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (15, 190, 190), (36, 255,255))
    imask = mask>0
    res = np.zeros_like(roi, np.uint8)
    res[imask] = roi[imask]
    # Convert image to grayscale and enhance
    img = cv2.cvtColor(np.array(res), cv2.COLOR_BGR2GRAY)
    kernel = np.ones((2, 2), np.uint8)
    roi = cv2.dilate(img, kernel, iterations=1)
    roi = cv2.erode(roi, kernel, iterations=1)
    # Get text from image 
    sceneText = (pytesseract.image_to_string(roi, lang='rus'))
    return sceneText

# Reconnect after kick from server
def reconnect(array, image):
    if array[0][0] and array[0][1] and array[0][2] and array[0][3] in image:
        pyautogui.press('enter')
        print('Re-login pressed!')
        sleep(5)
    else:
        relogin(array, image)

# Login from character selecting screen 
def relogin(array, image):
    if array[1][0] in image:
        pyautogui.press('enter')
        print('Connect pressed!')
    else:
        afk(array, image)

# Move you character to avoid AFK
def afk(array, image):
    keys = ['w', 'a', 's', 'd', 'space', '[', ']']
    startTime = time()
    if array[0][0] and array[0][1] and array[0][2] and array[0][3] not in image:
        keys_select = random.randint(0, 6) # Select random key from 'keys' list
        pressed_time = random.uniform(0, 2) # Chooses how long the key should be pressed (0-2 seconds)
        rand_wait = random.uniform(1, 20) # Chooses when the key will be pressed (between 1-245 seconds)
        pyautogui.keyDown(keys[keys_select]) # Press down key
        sleep(pressed_time) # Time used from press to release the button
        pyautogui.keyUp(keys[keys_select]) # Release key
        print(f"Script working for {(time()-startTime)/60:.1f} minutes.\nPressed key {keys[keys_select]} for {pressed_time:.1f} seconds.\nWaiting {rand_wait:.1f} seconds.\n")
        sleep(rand_wait) # How long script should wait before pressing down a new key

# Check if you WoW window's open and start defined functions, also check status and select func
def main(words):
    reconnect_array = words
    while True:
        wowTitle = "World of Warcraft"
        currentWindow = pyautogui.getActiveWindowTitle()
        if(currentWindow == wowTitle):
            screenText = getSceneText()
            if reconnect_array[0][0] or reconnect_array[0][1] or reconnect_array[0][2] or reconnect_array[0][3] in screenText:
                reconnect(reconnect_array, screenText)
                sleep(5)
            else:
                next

            if reconnect_array[1][0] in screenText:
                relogin(reconnect_array, screenText)
                sleep(20)
            else:
                next

            if reconnect_array[0][0] and reconnect_array[0][1] and reconnect_array[0][2] and reconnect_array[0][3] not in screenText:
                afk(reconnect_array, screenText)
            else:
                continue
        else:
            print('Wrong window')
            sleep(5)

# Simple language selector for you game (tested only on Russian, tell me if something wrong on eng version)  
def language_select(language):
    russian_words = [['Переподключение', 'Настройки', 'Создатели', 'Выйти'], ['Удалить персонажа']]
    english_words = [['Reconnect', 'System', 'Credits', 'Quit'], ['Delete Character']]
    reconnect_array = []

    if language in supported_languages:
        if language == 'russian':
            reconnect_array = russian_words
        elif language == 'english':
            reconnect_array = english_words
    else:
        print('Wrong selection! (English/Russian)')
        exit()
    
    print(f'You have selected {language} language, open your WoW window in next five seconds.')
    sleep(5)
    main(reconnect_array)

if __name__ == '__main__':
    print('Choose your language:')
    language_select(input().lower())