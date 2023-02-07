import mss.tools
import time
import cv2
import numpy as np
import pyautogui
from PIL import Image
import intelligence
from intelligence import Intelligence

def take_action(action_value):
    if action_value == 1:    
        pyautogui.press('up')
    elif action_value == 0:
        pyautogui.press('down') 


def preprocess(image, width, height):
    cropped_img = image.crop((0, 80, 650, 205))
    return cropped_img.resize((width, height))


saved_action = 1
action_interval = 0.2

intel = Intelligence(80, 16, 5, 2)

time.sleep(3)

while True:
    images = []
    game_over = False
    first_img = None
    last_img = None

    saved_action = intel.evaluate_action(images)
    take_action(saved_action)

    for i in range(intel.image_count):
        # The screen part to capture
        monitor = {"top": 250, "left": 325, "width": 650, "height": 205}
        output = str(i) + "_sct-{top}x{left}_{width}x{height}.png".format(**monitor)

        # Grab the data
        sct_img = mss.mss().grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX").convert("L")
        if i == intel.image_count-2:
            first_img = img
        elif i == intel.image_count-1:
            last_img = img

        # image preprocessing
        processed_img = preprocess(img, intel.width, intel.height)
        data = np.asarray(processed_img, dtype="int32")
        #print(data.shape)

        # Debug: Save to png
        #img.save(output, "PNG")
        #processed_img.save("processed_" + output, "PNG")

        # each loop
        if saved_action == 0:
            take_action(saved_action)
        time.sleep(action_interval/intel.image_count)
        images.append(data)

    if np.all(np.equal(first_img, last_img)):
        game_over = True
    
    intel.receive_reward(game_over)

    if game_over:
        pyautogui.press('up')
    if cv2.waitKey(200) & 0xFF == ord('q'):
        break

intel.show_results()
print("Game over!")

