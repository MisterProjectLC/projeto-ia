import mss.tools
import time
import cv2
import numpy as np
import pyautogui
from PIL import Image
from intelligence import evaluate_action


def decide_action(images, is_game_over):
    return evaluate_action(images, is_game_over)


def take_action(action_value):
    if action_value == 1:    
        pyautogui.press('up')
    elif action_value -1:
        pyautogui.press('down') 


saved_action = 1
action_interval = 0.25
image_count = 10
last_img = None

time.sleep(3)

while True:
    images = []
    game_over = False
    first_img = None
    last_img = None

    for i in range(image_count):
        # The screen part to capture
        monitor = {"top": 250, "left": 325, "width": 650, "height": 205}
        output = str(i) + "_sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = mss.mss().grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert("L")
        if i == image_count-2:
            first_img = img
        elif i == image_count-1:
            last_img = img

        cropped_img = img.crop((0, 80, 650, 205))
        resized_img = cropped_img.resize((160, 25))
        data = np.asarray(resized_img, dtype="int32")

        # Save to the picture file
        img.save(output, "PNG")
        resized_img.save("resized_" + output, "PNG")

        # each loop
        take_action(saved_action)
        time.sleep(action_interval/image_count)
        images.append(data)
        print(output)

    if np.all(np.equal(first_img, last_img)):
        game_over = True
        break
        
    saved_action = decide_action(images, game_over)
    if game_over:
        break

print("Game over!")

