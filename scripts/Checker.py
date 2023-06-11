from tkinter import *
import cv2
import os

def checkFolder(folder):
    # Get list of images in the folder
    images = [filename for filename in os.listdir(folder) if filename.endswith(".png")]
    n = len(images)  # number of images
    i = 0  # counter for the current image

    while i < n:
        # Read and display the current image
        img = cv2.imread(os.path.join(folder, images[i]))
        cv2.imshow('image', img)

        key = cv2.waitKey(0) & 0xFF  # wait for a key press

        # if 'd' was pressed, delete the image
        if key == ord('d'):
            os.remove(os.path.join(folder, images[i]))
            print(f'{images[i]} was deleted.')

            # Remove image from the list and decrement the counter
            del images[i]
            n -= 1
            if i != 0:  # prevent index out of range
                i -= 1

        # if right arrow key was pressed, go to the next image
        elif key == ord('r'):
            if i < n-1:  # prevent index out of range
                i += 1

        # if left arrow key was pressed, go to the previous image
        elif key == ord('l'):
            if i > 0:  # prevent index out of range
                i -= 1

        else:
            cv2.destroyAllWindows()
            break

    renameFiles(folder)


def renameFiles(folder):
    i = 0
    for filename in os.listdir(folder):
        i += 1
        if filename.endswith(".png"):
            os.rename(os.path.join(folder, filename), os.path.join(folder,f"{i}.png"))
    i = 0
    for filename in os.listdir(folder):
        i += 1
        if filename.endswith(".png"):
            os.rename(os.path.join(folder, filename), os.path.join(folder,f"img({i}).png"))
