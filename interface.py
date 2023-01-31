import mss.tools
import time
import cv2
import numpy
import pyautogui
from PIL import Image
from intelligence import evaluate_action

#wsh = comclt.Dispatch("WScript.Shell")


def take_action(images):
    action_value = evaluate_action(images)
    if action_value == 1:    
        pyautogui.press('a')
    elif action_value -1:
        pyautogui.press('b') 


action_interval = 1
image_count = 10

time.sleep(3)
game_over = False
while True:
    images = []
    game_over = False

    for i in range(10):
        with mss.mss() as sct:
            # The screen part to capture
            monitor = {"top": 160, "left": 160, "width": 160, "height": 135}
            output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

            # Grab the data
            sct_img = sct.grab(monitor)
            img = Image.new("RGB", sct_img.size)

            # Save to the picture file
            #mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
            images.append(img)
            print(output)

        if game_over:
            break
        
    take_action(images)
    break

print("Game over!")

