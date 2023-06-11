import cv2
import os

def del_white_bg(src_file, dest_file):
    src = cv2.imread(src_file)[3:-3]
    tmp = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    _, alpha = cv2.threshold(tmp,225,255,cv2.THRESH_BINARY)
    alpha_inv = cv2.bitwise_not(alpha)
    b, g, r = cv2.split(src)
    rgba = [b,g,r, alpha_inv]
    img = cv2.merge(rgba,4)
    # cv2.imwrite(dest_file,img)

    # img = img[:-3]
    pts = cv2.findNonZero(alpha_inv)
    x, y, w, h = cv2.boundingRect(pts)
    img = img[y:y+h, x:x+w]
    cv2.imwrite(dest_file,img)

def del_white_bg_folder(src_folder, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    i = 1
    src_file_name = os.path.join(src_folder, f'img({i}).png')
    dest_file_name = os.path.join(dest_folder, f'img({i}).png')

    while os.path.exists(src_file_name):
        del_white_bg(src_file_name, dest_file_name)
        i+=1
        src_file_name = os.path.join(src_folder, f'img({i}).png')
        dest_file_name = os.path.join(dest_folder, f'img({i}).png')

    cv2.destroyAllWindows()
    print("done")
