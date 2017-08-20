import os
import csv

os.getcwd()
os.chdir('C:\\Users\\k\\Desktop\\a')

import numpy as np
from PIL import Image
import pytesseract
import cv2
pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
####################################

def getString(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite("removed_noise.png", img)    
    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(Image.open("removed_noise.png"))
    return result

    
genderWords = ['boy', 'boys', 'girl', 'girls', 'kid', 'kids', 'bb', 'baby',
            'babies']
prodWords = ['knit', 'woven', 'sleep', 'cotton']
kstart = ['gender:', 'fabric:', 'Prod. Type:(T)', 'Description:',
          'Vendor:']
          
##############################################
def getKeys(txt):
    desc = ''
    fabric = ''
    vendor = ''
    txt = txt.lower()
    gender = []
    for word in genderWords:
        if word in txt:
            gender.append(word)
    prodtype = []
    for word in prodWords:
        if word in txt:
            prodtype.append(word)
    
    key = 'description: ' 
    if key in txt:
        indStart = txt.index(key) +13
        indEnd = txt.index('revise')
        desc = txt[indStart:indEnd]
    key = 'fabric: '
    if key in txt:
        indStart = txt.index(key) +8
        indEnd = txt.index('modified')
        fabric = txt[indStart:indEnd]
    key = 'vendor: '
    if key in txt:
        indStart = txt.index(key) +8
        indEnd = txt.index('store') -3
        vendor = txt[indStart:indEnd]
    return (gender, prodtype, desc, fabric, vendor)

    
def workflow(filename):
    txt = getString(filename).lower()
    if 'page 1' in txt:
        return getKeys(txt)
    else:
        return None

#### main ###########################################
if __name__ == '__main__':
    result = []
    resultHeader = ['techpackID', 'gender', 'productionType', 'description', 'fabric', 'vendor']
    result.append(resultHeader)
    counter = 0
    for i in range(1,100):
        print(i)
        if i < 10:
            filename = 'a-0' + str(i) + '.jpg'
        else:
            filename = 'a-' + str(i) + '.jpg'
        if os.path.isfile(filename): 
            output = workflow(filename)
            if output is not None:
                counter += 1
                out = [counter]
                out.append(', '.join(output[0]))
                out.append(', '.join(output[1]))
                out.append(output[2])
                out.append(output[3])
                out.append(output[4])
                result.append(out)
    
    ##### output to csv ############################
    with open('output.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(result)
    
    


