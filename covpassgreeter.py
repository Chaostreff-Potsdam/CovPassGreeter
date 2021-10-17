#!/usr/bin/python3

import cv2
from pyzbar import pyzbar
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

import zlib
import base45
import cbor2
import subprocess
import math

# initialize the cv2 QRCode detector
detector = cv2.QRCodeDetector()

camera = PiCamera()
#camera.resolution = (640, 480)
camera.resolution = (1296, 730)
camera.framerate = 15

#rawCapture = PiRGBArray(camera, size=(640,480))
rawCapture = PiRGBArray(camera, size=(1296, 730))
# allow the camera to warmup
time.sleep(0.1)
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    img = frame.array

    print('Image Dimensions :', img.shape)

    barcodes = pyzbar.decode(img)

    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
        (x, y, w, h) = barcode.rect
        print(x, y, w, h)
    
        # the barcode data is a bytes object so if we want to draw it
        # on our output image we need to convert it to a string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
    
        print(barcodeData)
        print(barcodeType)
        b45data = barcodeData.replace("HC1:", "")
        zlibdata = base45.b45decode(b45data)
        cbordata = zlib.decompress(zlibdata)
        decoded = cbor2.loads(cbordata)
        decoded_qrcode = cbor2.loads(decoded.value[2])
        print("")
        vorname = decoded_qrcode[-260][1]["nam"]["gn"]
        nachname = decoded_qrcode[-260][1]["nam"]["fn"]
        print(decoded_qrcode[-260][1]["nam"]["gn"]) 
        print(decoded_qrcode[-260][1]["nam"]["fn"]) 
        subprocess.run(["espeak", "-vde", vorname + " " + nachname + ", "+"ist ge impft, Glückwunsch!", "-v", "mb/mb-de2", "-s", "200"])
        subprocess.run(["mplayer", "newfile.mp3"])
        cv2.imwrite("success_"+str(math.floor(time.time()))+".png", img)        
                
                
    rawCapture.truncate(0)

