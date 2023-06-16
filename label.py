#!/usr/bin/env python3
## -*- coding: utf-8 -*-
#import sys
#import codecs
#sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

from PIL import Image, ImageDraw, ImageFont
import zipfile
import os
import json
import datetime

path = "/usr/local/etc/label/work_dir/"

def openDir (path):
    for dirs,folder,files in os.walk(path):
        print("Select dir: ", dirs)
        print("In dirs: ", folder)
        print("Files: ", files)
        print("\n")
        #перебераем все файлы в директории
        for file1 in files:
            ext_split = os.path.splitext(file1)
            if ext_split[1] == ".csv":     #если расширение CSV открываем файл и считываем GTIN
                f = open(path+file1, 'r')
                marka = f.read()
                print ("marka = ", marka)
                gtin = marka[2:16]
                print ("gtin : ", gtin)
                sub_name = ""
                for file2 in files:
                    ext_split2 = os.path.splitext(file2)
                    #print ("Extens: ",ext_split2)
                    if ext_split2[1] == ".zip":
                        z = zipfile.ZipFile(path+file2, "r")
                        for fi in z.namelist():
                            print("Файлы архива: ", fi)
                            if fi != "attributes.json":
                                eps_file = fi
                                print("EPS file: ", eps_file)
                        fileinzip = z.open("attributes.json", mode="r")
                        file_json = json.load(fileinzip)
                        for j in file_json["gtinProductAttributes"]:
                            print("gtin from json", j)
                            gtin_json = j
                        if gtin == gtin_json:
                            attr = []
                            attr.append(file_json["gtinProductAttributes"][gtin]["name"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["model"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["productTypeDesc"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["color"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["productSize"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["materialUpper"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["materialLining"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["materialDown"])
                            attr.append(file_json["gtinProductAttributes"][gtin]["brand"])
                            country_split = file_json["gtinProductAttributes"][gtin]["country"].split()
                            attr.append(country_split[0])
                            attr.append(file_json["gtinProductAttributes"][gtin]["ncCreateDate"])
                            epsinzip = z.open(eps_file, mode="r")
                            attr.append(epsinzip)
                            attr.append(gtin_json)
                            attr.append(marka)
                            createLabel_75120(attr)
                        z.close()


def createLabel_6040 (text_label):
    lineh1 = (5,80,475,80)
    print ("CREATE LABEL WITH gtin= ", text_label[12])
    img = Image.new("RGB", (480,320), "white") # для этикетки 58*40
    dm = Image.open(text_label[11])
    print (dm.size)
    dm.load(scale=3)
    img.paste(dm, (330,83))
    font = ImageFont.truetype("NotoMono-Regular.ttf", size=30)
    font_small = ImageFont.truetype("NotoMono-Regular.ttf", size=20)
    font_detail = ImageFont.truetype("NotoMono-Regular.ttf", size=10)
    idraw = ImageDraw.Draw(img)
    idraw.text((10, 5), text_label[0], font=font, fill="#000000")
    idraw.text((10, 35), text_label[1], font=font, fill="#000000")
    idraw.text((10, 85), "ПРОДУКЦИЯ", font=font_detail, fill="#000000")
    idraw.text((10, 100), text_label[2], font=font_small, fill="#000000")
    idraw.text((145, 85), "ЦВЕТ", font=font_detail, fill="#000000")
    idraw.text((145, 100), text_label[3], font=font_small, fill="#000000")
    idraw.text((250, 85), "РАЗМЕР", font=font_detail, fill="#000000")
    idraw.text((250, 100), text_label[4], font=font_small, fill="#000000")

    idraw.text((10, 130), "ВЕРХ", font=font_detail, fill="#000000")
    idraw.text((10, 145), text_label[5], font=font_small, fill="#000000")
    idraw.text((145, 130), "ПОДКЛАДКА", font=font_detail, fill="#000000")
    idraw.text((145, 145), text_label[6], font=font_small, fill="#000000")
    idraw.text((250, 130), "ПОДОШВА", font=font_detail, fill="#000000")
    idraw.text((250, 145), text_label[7], font=font_small, fill="#000000")

    idraw.text((10, 175), "ПРОИЗВОДИТЕЛЬ", font=font_detail, fill="#000000")
    idraw.text((10, 190), text_label[8], font=font_small, fill="#000000")
    idraw.text((145, 175), "СТРАНА", font=font_detail, fill="#000000")
    idraw.text((145, 190), text_label[9], font=font_small, fill="#000000")
    idraw.text((250, 175), "ДАТА", font=font_detail, fill="#000000")
    dt = datetime.datetime.fromtimestamp(text_label[10])
    dt.strfptint('%d-%m-%Y')
    idraw.text((250, 190), dt, font=font_small, fill="#000000")

    idraw.line(lineh1, fill="black", width=2)
    img.save(text_label[12]+".pdf", "PDF", append=False, resolution=203, quality=100)
    #dm.save("test_dm.jpg")
    #img = Image.open("test1.png")
    #img.show()

def createLabel_75120 (text_label):
    lineh1 = (7,175,953,175)
    lineh2 = (7,260,480,260)
    lineh3 = (663,175,663,593)
    lineh4 = (480,175,480,340)
    lineh5 = (480,340,663,340)
    print ("CREATE LABEL WITH gtin= ", text_label[12])
    img = Image.new("RGB", (960,600), "white") # для этикетки 75*120 при разрешении печати 8 dpi
    dm = Image.open(text_label[11])
    logo = Image.open("logo_bw_150.png")
    logo_eac = Image.open("logo_EAC_bw.png")
    logo_cz = Image.open("logo_CHZN_bw.png")
    print (dm.size)
    dm.load(scale=5)
    
    font = ImageFont.truetype("NotoMono-Regular.ttf", size=60)
    font_small = ImageFont.truetype("NotoMono-Regular.ttf", size=30)
    font_model = ImageFont.truetype("NotoMono-Regular.ttf", size=40)
    font_detail = ImageFont.truetype("NotoMono-Regular.ttf", size=20)
    font_size = ImageFont.truetype("NotoMono-Regular.ttf", size=120)
    font_marka = ImageFont.truetype("NotoMono-Regular.ttf", size=15)

    idraw = ImageDraw.Draw(img)
    idraw.rectangle((7, 7, 953, 593), fill="white", outline="black", width=3)
    idraw.text((180, 50), text_label[0], font=font, fill="#000000")
    idraw.line(lineh1, fill="black", width=3)
    idraw.text((30, 195), text_label[1], font=font_model, fill="#000000")
    idraw.line(lineh2, fill="black", width=3)
    idraw.line(lineh3, fill="black", width=3)
    idraw.line(lineh4, fill="black", width=3)
    idraw.line(lineh5, fill="black", width=3)
    y = 180
    idraw.text((20, 165+y), "ПРОДУКЦИЯ", font=font_detail, fill="#000000")
    idraw.text((20, 190+y), text_label[2], font=font_small, fill="#000000")
    idraw.text((280, 165+y), "ЦВЕТ", font=font_detail, fill="#000000")
    idraw.text((280, 190+y), text_label[3], font=font_small, fill="#000000")
    idraw.text((480, 165+y), "РАЗМЕР", font=font_detail, fill="#000000")
    idraw.text((480, 190+y), text_label[4], font=font_small, fill="#000000")
    idraw.text((495, 190), text_label[4], font=font_size, fill="#000000")

    idraw.text((20, 245+y), "ВЕРХ", font=font_detail, fill="#000000")
    idraw.text((20, 275+y), text_label[5], font=font_small, fill="#000000")
    idraw.text((280, 245+y), "ПОДКЛАДКА", font=font_detail, fill="#000000")
    idraw.text((280, 275+y), text_label[6], font=font_small, fill="#000000")
    idraw.text((480, 245+y), "ПОДОШВА", font=font_detail, fill="#000000")
    idraw.text((480, 275+y), text_label[7], font=font_small, fill="#000000")

    idraw.text((20, 325+y), "ПРОИЗВОДИТЕЛЬ", font=font_detail, fill="#000000")
    idraw.text((20, 355+y), text_label[8], font=font_small, fill="#000000")
    idraw.text((280, 325+y), "СТРАНА", font=font_detail, fill="#000000")
    idraw.text((280, 355+y), text_label[9], font=font_small, fill="#000000")
    idraw.text((480, 325+y), "ДАТА", font=font_detail, fill="#000000")
    dt = datetime.datetime.fromtimestamp(text_label[10]/1000)
    date_json = dt.strftime('%d.%m.%Y')
    idraw.text((480, 355+y), date_json, font=font_small, fill="#000000")
    idraw.text((667, 425), text_label[13], font=font_marka, fill="#000000")

    img.paste(dm, (690,180))
    img.paste(logo, (15,18))
    img.paste(logo_eac, (770,455))
    img.paste(logo_cz, (710,517))
    
    img.save(text_label[12]+".pdf", "PDF", append=False, resolution=203, quality=100)

def createLabel_75120_copy (text_label):
    lineh1 = (7,100,953,100)
    lineh2 = (7,160,680,160)
    lineh3 = (680,100,680,593)
    print ("CREATE LABEL WITH gtin= ", text_label[12])
    img = Image.new("RGB", (960,600), "white") # для этикетки 58*40
    dm = Image.open(text_label[11])
    logo = Image.open("logo_bw_150.png")
    print (dm.size)
    dm.load(scale=5)
    #img.paste(dm, (700,150))
    font = ImageFont.truetype("NotoMono-Regular.ttf", size=60)
    font_small = ImageFont.truetype("NotoMono-Regular.ttf", size=30)
    font_model = ImageFont.truetype("NotoMono-Regular.ttf", size=40)
    font_detail = ImageFont.truetype("NotoMono-Regular.ttf", size=20)
    idraw = ImageDraw.Draw(img)
    idraw.rectangle((7, 7, 953, 593), fill="white", outline="black", width=3)
    idraw.text((50, 15), text_label[0], font=font, fill="#000000")
    idraw.line(lineh1, fill="black", width=3)
    idraw.text((30, 105), text_label[1], font=font_model, fill="#000000")
    idraw.line(lineh2, fill="black", width=3)
    idraw.line(lineh3, fill="black", width=3)

    idraw.text((20, 165), "ПРОДУКЦИЯ", font=font_detail, fill="#000000")
    idraw.text((20, 190), text_label[2], font=font_small, fill="#000000")
    idraw.text((280, 165), "ЦВЕТ", font=font_detail, fill="#000000")
    idraw.text((280, 190), text_label[3], font=font_small, fill="#000000")
    idraw.text((500, 165), "РАЗМЕР", font=font_detail, fill="#000000")
    idraw.text((500, 190), text_label[4], font=font_small, fill="#000000")

    idraw.text((20, 245), "ВЕРХ", font=font_detail, fill="#000000")
    idraw.text((20, 275), text_label[5], font=font_small, fill="#000000")
    idraw.text((280, 245), "ПОДКЛАДКА", font=font_detail, fill="#000000")
    idraw.text((280, 275), text_label[6], font=font_small, fill="#000000")
    idraw.text((500, 245), "ПОДОШВА", font=font_detail, fill="#000000")
    idraw.text((500, 275), text_label[7], font=font_small, fill="#000000")

    idraw.text((20, 325), "ПРОИЗВОДИТЕЛЬ", font=font_detail, fill="#000000")
    idraw.text((20, 355), text_label[8], font=font_small, fill="#000000")
    idraw.text((280, 325), "СТРАНА", font=font_detail, fill="#000000")
    idraw.text((280, 355), text_label[9], font=font_small, fill="#000000")
    idraw.text((500, 325), "ДАТА", font=font_detail, fill="#000000")
    dt = datetime.datetime.fromtimestamp(text_label[10]/1000)
    date_json = dt.strftime('%d-%m-%Y')
    idraw.text((500, 355), date_json, font=font_small, fill="#000000")

    img.paste(dm, (700,110))
    img.paste(logo, (700,360))
    
    img.save(text_label[12]+".pdf", "PDF", append=False, resolution=203, quality=100)

def main():
    openDir(path)

if __name__ == "__main__":
    main()