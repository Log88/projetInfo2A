import sys
import os
import shutil
from typing import Self


from Scrapper import scrape
from Cutter import del_white_bg_folder
from Labeler import label_folder
from Combiner import combine_folder
from Checker import checkFolder

data_folder = r".\data"


class DatabaseManager:
    def __init__(self, name, isBackground):
        self.name = name
        self.isBackground = isBackground
        self.main_folder = os.path.join(data_folder, f'Database_{name}')
        self.info_file = os.path.join(self.main_folder, 'info.txt')
        if not os.path.exists(self.main_folder):
            os.makedirs(self.main_folder)
        self.scraped = False
        self.CurNbImages = 0
        self.cut = False
        self.labeled = False
        self.inContext = False
        self.writeInfo()
        self.cur_folder = None
        self.updateCurFolder()



    def writeInfo(self):
        with open(self.info_file, 'w') as file:
            if self.isBackground:
                file.write('isBackground\n')
            else:
                file.write('isObject\n')
            if self.scraped:
                file.write('scraped\n')
            else:
                file.write('notScraped\n')
            file.write(f'CurNbImages {self.CurNbImages}\n')
    
    def updateCurFolder(self):
        print("updating cur folder")
        if self.isBackground:
            if not self.CurNbImages == 0:
                self.cur_folder = self.getScrapedFolder()
            else : 
                self.cur_folder = None
        else:
            if self.inContext:
                self.cur_folder = self.getInContextFolder()
            elif self.cut:
                self.cur_folder = self.getCutOutFolder()
            elif self.scraped:
                self.cur_folder = self.getScrapedFolder()
            else:
                self.cur_folder = None

    
    
    @classmethod
    def create(cls, name, isBackground=False):
        if os.path.exists(os.path.join(data_folder, f'Database_{name}')):
            print(f"Database named {name} already exists, do you want to load it ? (y/n)")
            if input() == 'y':
                return cls.load(name)
            else:
                print("Database not created")
                return
        db = cls(name, isBackground)
        return db
    
    @classmethod
    def load(cls, name):
        #check if database exists
        if not os.path.exists(os.path.join(data_folder, f'Database_{name}')):
            print("Database doesn't exists")
        
            return
        
        main_folder = os.path.join(data_folder, f'Database_{name}')
        with open(os.path.join(main_folder, 'info.txt'), 'r') as file:
            isBackground = file.readline().strip() == 'isBackground'
            scraped = file.readline().strip() == 'scraped'
            CurNbImages = int(file.readline().strip().split()[1])
        db = cls(name, isBackground)
        db.scraped = scraped
        db.CurNbImages = CurNbImages
        db.writeInfo()
        db.cut = os.path.exists(os.path.join(main_folder, f'CutOutData_{name}'))
        db.labeled = os.path.exists(os.path.join(main_folder, f'labels_{name}'))
        db.inContext = os.path.exists(os.path.join(main_folder, f'InContextData_{name}'))
        db.updateCurFolder()
        return db


    def setAsBackground(self):
        self.isBackground = True
        self.writeInfo()
        self.updateCurFolder()
    
    def setAsObject(self):
        self.isBackground = False
        self.writeInfo()
        self.updateCurFolder()



    def scrape(self, NUMBER_OF_IMAGES, RESEARCH):
        print("Scraping data...")
        dest_folder = os.path.join(self.main_folder, f'ScrapedData_{self.name}')
        scrape(RESEARCH, NUMBER_OF_IMAGES, dest_folder,self.CurNbImages)
        # self.scraped = True
        self.CurNbImages += NUMBER_OF_IMAGES
        self.writeInfo()
        self.updateCurFolder()
        print("done")
    
    def finishScraping(self):
        self.scraped = True
        self.writeInfo()
        self.updateCurFolder()

    def cutOut(self):
        if self.CurNbImages == 0:
            print("Data not scraped")
            return
        if self.cut:
            print("Data already cut out")
            return
        print("Cutting out data...")
        src_folder = self.getScrapedFolder()
        dest_folder = os.path.join(self.main_folder, f'CutOutData_{self.name}')
        del_white_bg_folder(src_folder, dest_folder)
        self.cut = True
        self.updateCurFolder()
        print("done")
    
    def label(self):
        if self.CurNbImages == 0:
            print("Data empty")
            return
        if self.labeled:
            print("Data already labeled, do you want to relabel it ? (y/n)")
            if input() == 'n':
                return
            if input() == 'y':
                self.cleanLabeled()
        if not self.isBackground:
            print("Data not background, do you want to set it as background ? (y/n)")
            if input() == 'y':
                self.setAsBackground()
            else:
                print("Data not labeled")
                return
        src_folder = self.getScrapedFolder()
        dest_folder = os.path.join(self.main_folder, f'labels_{self.name}')
        print("r to restart, w to write, c to continue")
        label_folder(src_folder, dest_folder)
        self.labeled = True
        self.updateCurFolder()
        print("done")
    
    def putInContext(self, background_db):
        if not background_db.isBackground:
            print("Background database needed")
            return
        if not background_db.labeled:
            print("Background database not labeled")
            return
        if not self.cut:
            print("Data not cut out")
            return
        print("Putting data in context...")
        obj_folder = self.getCutOutFolder()
        bg_folder = background_db.getScrapedFolder()
        dest_folder = os.path.join(self.main_folder, f'InContextData_{self.name}')
        labels_file = os.path.join(background_db.main_folder, f'labels_{background_db.name}', 'labels.txt')
        combine_folder(obj_folder, bg_folder, labels_file, dest_folder)
        self.inContext = True
        self.updateCurFolder()
        print("done")

    def checkFolder(self):
        folder = self.cur_folder
        print(folder)
        if folder is not None:
            print(f"Checking {folder}...")
            checkFolder(folder)
        

    def getScrapedFolder(self):
        if self.CurNbImages == 0:
            print("Data not scraped")
            return
        return os.path.join(self.main_folder, f'ScrapedData_{self.name}')

    def getCutOutFolder(self):
        if not self.cut:
            print("Data not cut out")
            return
        return os.path.join(self.main_folder, f'CutOutData_{self.name}')
    
    def getLabeledFolder(self):
        if not self.labeled:
            print("Data not labeled")
            return
        return os.path.join(self.main_folder, f'labels_{self.name}')
    
    def getInContextFolder(self):
        if not self.inContext:
            print("Data not in context")
            return
        return os.path.join(self.main_folder, f'InContextData_{self.name}')



    def cleanScraped(self):
        if self.CurNbImages == 0:
            print("Data not scraped")
            return
        print("Cleaning scraped data...")
        scraped_folder = self.getScrapedFolder()
        for file in os.listdir(scraped_folder):
            os.remove(os.path.join(scraped_folder, file))
        os.rmdir(scraped_folder)
        self.scraped = False
        self.CurNbImages = 0
        self.writeInfo()
        print("done")

    def cleanCutOut(self):
        if not self.cut:
            print("Data not cut out")
            return
        print("Cleaning cut out data...")
        cut_out_folder = self.getCutOutFolder()
        for file in os.listdir(cut_out_folder):
            os.remove(os.path.join(cut_out_folder, file))
        os.rmdir(cut_out_folder)
        self.cut = False
        print("done")

    def cleanLabeled(self):
        if not self.labeled:
            print("Data not labeled")
            return
        print("Cleaning labeled data...")
        labeled_folder = self.getLabeledFolder()
        for file in os.listdir(labeled_folder):
            os.remove(os.path.join(labeled_folder, file))
        os.rmdir(labeled_folder)
        self.labeled = False
        print("done")
    
    def cleanInContext(self):
        if not self.inContext:
            print("Data not in context")
            return
        print("Cleaning in context data...")
        inContext_folder = self.getInContextFolder()
        for file in os.listdir(inContext_folder):
            os.remove(os.path.join(inContext_folder, file))
        os.rmdir(inContext_folder)
        self.inContext = False
        print("done")

    def cleanAll(self):
        self.cleanScraped()
        self.cleanCutOut()
        self.cleanLabeled()
        self.cleanInContext()

    def delete(self):
            print("force deleting database...")
            shutil.rmtree(self.main_folder)
