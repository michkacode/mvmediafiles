#!/usr/bin/env python 

import os
import shutil
from os import path
import glob
import time
import re

import plum.exceptions
from icecream import ic
from exif import Image
import PIL
from tkinter import Tk, filedialog

spath = "./"
files = []
paths = []


# gibt alle Pfade zu Bilddateien aus einem Ordner und dessen Unterordner zurück
def findindirrec(spath):
    extensions = ('*.jpg', '*.jpeg', '*.png', '*.tif')
    ext: str
    for ext in extensions:
        files.extend(glob.glob(spath + '/**/' + ext, recursive=True))
    return files

def getfiledate(image):
     with open(image, "rb") as image_file:
        try:
            my_image = Image(image_file)

        except plum.exceptions.UnpackError:
            ic("Datei" + os.path.basename(image) + "lässt sich nicht in die Karten schauen")
            filedate = time.gmtime(os.stat(image).st_mtime)
            fileprefix = str(filedate.tm_year).zfill(4) + str(filedate.tm_mon).zfill(2) + str(filedate.tm_mday).zfill(
                2)
        else:
            if my_image.has_exif:
                # ic(Image.open(image)._getexif()[36867])
                # ic(my_image.get_all())
                try:
                    ic(my_image.datetime)
                    fileprefix = (re.sub("\\:", "", str(my_image.datetime)))[0:8]

                except KeyError:
                    ic("KeyError occured")
                except AttributeError:
                    ic("Es gibt kein datetime Attribut in dieser Datei.")
                    filedate = time.gmtime(os.stat(image).st_mtime)
                    fileprefix = str(filedate.tm_year).zfill(4) + str(filedate.tm_mon).zfill(2) + str(
                        filedate.tm_mday).zfill(
                        2)
            else:
                filedate = time.gmtime(os.stat(image).st_mtime)
                ic("\n" + image)
                fileprefix = str(filedate.tm_year).zfill(4) + str(filedate.tm_mon).zfill(2) + str(filedate.tm_mday).zfill(2)

        return fileprefix

def main():
    # spath = "/Volumes/Extreme SSD/iPhoto Library/Masters"
    root = Tk()  # pointing root to Tk() to use it as Tk() in program.
    root.withdraw()  # Hides small tkinter window.
    root.attributes('-topmost', True)  # Opened windows will be active. above all windows despite of selection.

    spath = filedialog.askdirectory(initialdir="/",title='Bitte wähle das Quellverzeichnis')  # Returns opened path as str
    #spath = "/Volumes/GoogleDrive/Meine Ablage/Fotos"

    dpath = filedialog.askdirectory(initialdir="/",title='Bitte wähle das Zielverzeichnis')
    dpathchoosed = dpath
    #dpath = "/Volumes/GoogleDrive/Meine Ablage/Fotos"

    #Finde alle Bilder
    findindirrec(spath)

    for image in findindirrec(spath):
        filedate = (getfiledate(image))

        # Das Erstellungs-YYYYMMDDD als Präfix an die Datei schreiben
        if re.match(r"^\d{8}_", os.path.basename(image)):
            filename = os.path.basename(image)
        else:
            filename = filedate + "_" + os.path.basename(image)

        # Checken, ob die Ordner angelegt sind
        dpath = dpathchoosed
        dpath = dpath + "/" + filedate[0:4]
        if not os.path.exists(dpath):
            os.mkdir(dpath)
        dpath = dpath + "/" + filedate[4:6]
        if not os.path.exists(dpath):
            os.mkdir(dpath)


        try:
            shutil.copy2(image,dpath + "/" + filename)
            os.remove(image)
            print("File copied successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")

print(os.listdir(spath))
main()
