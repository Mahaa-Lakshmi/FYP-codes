import random
import pyautogui as pg
import time

animal=('monkey','donkey','dog')
time.sleep(20)
for i in range(50):
    a=random.choice(animal)
    pg.write("u r a "+a)
    pg.press('enter')

