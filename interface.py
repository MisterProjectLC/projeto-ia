import pyautogui
import torch
from torchvision import transforms
from PIL import Image
import time
from intelligence import evaluate_action


def take_action(images):
    action_value = evaluate_action(images)
    match(action_value):
        case 1:
            pyautogui.press('up')
        case -1:
            pyautogui.press('down') 


action_interval = 1
image_count = 10

time.sleep(3)
while True:
    images = []
    for i in range(image_count):
        im = pyautogui.screenshot('my_screenshot' + str(i) + '.png',
                                  region=(350,325, 650, 105))
        convert_tensor = transforms.ToTensor()
        tensor_im = convert_tensor(im)
        time.sleep(action_interval/image_count)
        images.append(tensor_im)
        
    take_action(images)


