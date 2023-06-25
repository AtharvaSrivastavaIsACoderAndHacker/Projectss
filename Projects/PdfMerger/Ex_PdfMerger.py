from PyPDF2 import PdfMerger
from os import system

system('cls')


pdf1 = input("PDF 1 : ")
pdf2 = input("PDF 2 : ")
pname = input("Name To Be Set For The Processed PDF : ")

merger = PdfMerger()
merger.append(pdf1)
merger.append(pdf2)
merger.write(pname)
merger.close()