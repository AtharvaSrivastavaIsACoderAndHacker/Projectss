import qrcode
from os import system
import qrtools as QR
import cv2
system('cls')


def make (dataa,n):
      img = qrcode.make(str(dataa))
      namee = str(n)+'.png'
      img.save(namee)



system("cls")
data = input('Enter The Data/Link/Text To Make The QRcode Of : ')
name = input('Enter Name For The QRcode ( without .png ): ')
make(data,name)