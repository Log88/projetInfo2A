import cv2
import os

class Labeler:
    def __init__(self, src_file, dest_file):
        self.src_file = src_file
        self.dest_file = dest_file
        self.points = []
        self.pointsList = []
        self.dragging = False
        self.image = cv2.imread(src_file)
        self.original = self.image.copy()
        self.clone = self.image.copy()

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.dragging = True
            self.points = [(x,y)]
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.dragging:
                self.image = self.clone.copy()
                cv2.rectangle(self.image, self.points[0], (x,y), (0,255,0), 2)
                cv2.imshow('image', self.image)
        elif event == cv2.EVENT_LBUTTONUP:
            self.dragging = False
            self.points.append((x,y))
            self.pointsList.append(self.points)
            self.clone = self.image.copy()
            cv2.rectangle(self.image, self.points[0], self.points[1], (0,255,0), 2)
            cv2.imshow('image', self.image)
    
    def label(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_rectangle)
        filename = os.path.basename(self.src_file)

        while True:
            cv2.imshow('image', self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):
                self.image = self.original.copy()
                self.clone = self.original.copy()
                self.pointsList = []
            elif key == ord('w'):
                # print(self.pointsList)ext
                if self.pointsList == []:
                    print("No points selected")
                else:
                    for points in self.pointsList:
                        print(points)
                        with open(self.dest_file, 'a') as f:
                            f.write(str(points) + f' {filename}' + '\n')
                    break
            elif key == ord("c"):
                break
        cv2.destroyAllWindows()

def label_folder(src_folder, dest_folder):
    # create destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_file = os.path.join(dest_folder, 'labels.txt')
    for filename in os.listdir(src_folder):
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q") : break
        if filename.endswith(".png"):
            src_file = os.path.join(src_folder, filename)
            # dest_file = os.path.join(dest_folder, filename[:-4] + '.txt')
            labeler = Labeler(src_file, dest_file)
            labeler.label()
            continue
        else:
            continue
        


