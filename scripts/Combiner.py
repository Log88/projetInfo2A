import cv2
import os
import re
import numpy as np
import random

def readLabel(string):
    numbers = re.findall(r'\d+', string)
    numbers = list(map(int, numbers))
    filename = re.search(r'\b[\w()-]+\.png\b', string).group()
    result = numbers + [filename]
    return result


def combine(obj_file, bg_file, label, dest_file):
    points = readLabel(label)[:-1]
    filename = readLabel(label)[-1]
    if filename != os.path.basename(bg_file):
        print("Error: label and background do not match")
        return
    topX = points[0]
    topY = points[1]
    botX = points[2]
    botY = points[3]

    # Read the images
    object_img = cv2.imread(obj_file, cv2.IMREAD_UNCHANGED)
    background_img = cv2.imread(bg_file, cv2.IMREAD_UNCHANGED)

    # Calculate the aspect ratio of the object
    aspect_ratio = object_img.shape[1] / object_img.shape[0]

    # Calculate the dimensions of the rectangle
    rect_width = botX - topX
    rect_height = botY - topY

    # Calculate the target dimensions of the object, preserving aspect ratio
    if rect_width / rect_height > aspect_ratio:
        # Rectangle is wider than the object, so height will be the limiting factor
        target_height = rect_height
        target_width = int(rect_height * aspect_ratio)
    else:
        # Rectangle is taller than the object, so width will be the limiting factor
        target_width = rect_width
        target_height = int(rect_width / aspect_ratio)

    # Resize object image to the target size
    object_img = cv2.resize(object_img, (target_width, target_height))

    # Calculate the position where the object should be placed
    posX1 = topX + (rect_width - target_width) // 2
    posY2 = topY + (rect_height - target_height) // 2
    posX2 = posX1 + target_width
    posY1 = posY2 + target_height

    alpha_s = object_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        background_img[posY2:posY1, posX1:posX2, c] = (alpha_s * object_img[:, :, c] + alpha_l * background_img[posY2:posY1, posX1:posX2, c])

    cv2.imwrite(dest_file, background_img)


def combine_folder(obj_folder, bg_folder, labels_file, dest_folder):
    with open(labels_file, 'r') as f:
        labels = f.readlines()
    random.shuffle(labels)
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    i = 1
    obj_file_name = os.path.join(obj_folder, f'img({i}).png')
    label = labels[(i-1)%len(labels)]
    bg_file_name = os.path.join(bg_folder, label.split(' ')[-1][:-1])
    dest_file_name = os.path.join(dest_folder, f'img({i}).png')
    while os.path.exists(obj_file_name):
        combine(obj_file_name, bg_file_name, label, dest_file_name)
        i += 1
        obj_file_name = os.path.join(obj_folder, f'img({i}).png')
        label = labels[(i-1)%len(labels)]
        bg_file_name = os.path.join(bg_folder, label.split(' ')[-1][:-1])
        dest_file_name = os.path.join(dest_folder, f'img({i}).png')