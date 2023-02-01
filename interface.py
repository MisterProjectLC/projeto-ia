import mss.tools
import time
import cv2
import numpy as np
import pyautogui
from PIL import Image
from intelligence import evaluate_action

#wsh = comclt.Dispatch("WScript.Shell")


def take_action(images):
    action_value = evaluate_action(images)
    if action_value == 1:    
        pyautogui.press('up')
    elif action_value -1:
        pyautogui.press('down') 


action_interval = 1
image_count = 10
last_img = None

time.sleep(3)
game_over = False
pyautogui.press('up')
time.sleep(1)

while True:
    images = []
    game_over = False

    for i in range(10):
        # The screen part to capture
        monitor = {"top": 250, "left": 325, "width": 650, "height": 205}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = mss.mss().grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert("L")

        cropped_img = img.crop((0, 100, 650, 205))
        resized_img = cropped_img.resize((325, 52))
        data = np.asarray(resized_img, dtype="int32")

        # Save to the picture file
        img.save(output, "PNG")
        resized_img.save("resized_" + output, "PNG")
        
        images.append(data)
        print(output)

        time.sleep(action_interval/image_count)

        if i > 0 and np.all(np.equal(last_img, img)):
            game_over = True
            break
        last_img = img

    if game_over:
        break
        
    take_action(images)
    break

print("Game over!")

