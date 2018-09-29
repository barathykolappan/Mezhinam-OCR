"""
@author: Barathy Kolappan A
Custom Tamil OCR
Synthetic Dataset - TDN Series
Uses advanced template matching and dictionary searching
"""
import glob, os
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
from difflib import SequenceMatcher
startTime = datetime.now()

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
'''
#Initialize O/P Window
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
cv2.resizeWindow("output", 200, 200)
'''
path = r'TDNMax\*jpg' #Applicable for TDNs,TDN,TDNMax
imgdict={}
finStr=""
#Association with TDN Dataset
dictlist={'ஃ':'ak','அ':'iaf','ஆ':'iaa','இ':'ie','ஈ':'iee','உ':'iu','ஊ':'iuu','எ':'iae','ஏ':'fea',
          'ஐ':'ai','ஒ':'io','ஓ':'ioo','க':'ka','கி':'ki','கீ':'kee','கு':'ku','கூ':'koo','ங':'nga',
          'ஙி':'ngi','ஙீ':'ngee','ஙு':'ngu','ஙூ':'ngoo','ச':'cha','சி':'chi','சீ':'chee','சு':'chu',
          'சூ':'choo','ஞ':'gya','ஞி':'gyi','ஞீ':'gyee','ஞு':'gyu','ஞூ':'gyoo','ட':'iad','டி':'idi',
          'டீ':'dee','டு':'du','டூ':'doo','ண':'nna','ணி':'nni','ணீ':'nnee','ணு':'nnu','ணூ':'nnoo',
          'த':'tha','தி':'thi','தீ':'thee','து':'thu','தூ':'thoo','ந':'ina','நி':'ini','நீ':'inee',
          'நு':'inu','நூ':'inoo','ப':'pa','பி':'pi','பீ':'pee','பு':'pu','பூ':'poo','ம':'ma','மி':'mi',
          'மீ':'mee','மு':'mu','மூ':'moo','ய':'ya','யி':'yi','யீ':'yee','யு':'yu','யூ':'yoo','ர':'ra',
          'ரி':'ri','ரீ':'ree','ரு':'ru','ரூ':'roo','ல':'ila','லி':'ili','லீ':'ilee','லு':'ilu',
          'லூ':'iloo','வ':'va','வி':'vi','வீ':'vee','வு':'vu','வூ':'voo','ழ':'sla','ழி':'sli',
          'ழீ':'slee','ழு':'slu','ழூ':'sloo','ள':'lla','ளி':'lli','ளீ':'llee','ளு':'llu','ளூ':'lloo',
          'ற':'bra','றி':'br','றீ':'bree','று':'bru','றூ':'broo','ன':'rna','னி':'rni','னீ':'rnee',
          'னு':'rnu','னூ':'rnoo','ா':'adda','ெ':'eadd','ே':'edd','ை':'id','்':'dot'}

images=glob.glob(path)
i=f=maximum=0

#file_path = "accind.txt"
#Source Image is read here
img = cv2.imread(r'nall.jpg')

#GrayScale Conversion
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#cv2.imwrite("Grayscale.jpg",gray)
#Thresholding by Binarizing
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
#cv2.imwrite("Binary.jpg",thresh)
#Initialize kernel for dilation
kernel = np.ones((1,1), np.uint8)
#Dilation is initiated for better reliability
img_dilation = cv2.dilate(thresh, kernel, iterations=1)
#cv2.imwrite("Dilation.jpg",img_dilation)
im2,ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#Contour mapping is performed, Sorted.
sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])

for i, ctr in enumerate(sorted_ctrs):
    x, y, w, h = cv2.boundingRect(ctr)
    #Region of Interest is abstracted 
    ro = img[y:y+h, x:x+w]
    #cv2.imwrite("roi"+str(i)+".jpg", ro)
    #cv2.imshow("roi"+str(i)+".jpg", ro)
    maximum=0
    roi = cv2.resize(ro,(200,200))

    for im in images:
        #Templates are read in bulk, one by one
        imgs = cv2.imread(im)
        template=cv2.resize(imgs,(200,200))
        #Matching is done by overlapping
        res = cv2.matchTemplate(roi,template,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #print(im,max_val)
        '''
        #Individual file accounting for iteration through templates
        with open(file_path, 'a') as file:
            dr=repr(max_val)
            st=im+" "+dr+"\n"
            file.write(st)
            '''
        imgdict[max_val]=im
        #Maximum similarity is kept track
        if(maximum<max_val):
            maximum=max_val
    #cv2.rectangle(img,(x,y),( x + w, y + h ),(0,255,0),2) 
    i=i+1
    #Letters from association are printed
    for key, value in dictlist.items():
        
        if("eadd" in imgdict[maximum]):
            f=1
        elif("edd" in imgdict[maximum]):
            f=2
        elif("id" in imgdict[maximum]):
            f=3
        elif(value in imgdict[maximum]):
            finStr=finStr+key
            if(f==1):
                finStr=finStr+'ெ'
                f=0
            elif(f==2):
                finStr=finStr+'ே'
                f=0   
            elif(f==3):
                finStr=finStr+'ை'
                f=0   
            #print(imgdict[maximum])  
print(finStr,end=' ')  
print (datetime.now() - startTime) 
#Enhancing Precision through Dictionary
xl_workbook = pd.ExcelFile('taIN.xlsx')  # Load the excel workbook
df = xl_workbook.parse("Sheet1")  # Parse the sheet into a dataframe
taWords = df['TamilCorpus'].tolist()  # Cast the desired column into a python list
nSim=mSim=mInd=nInd=0
for nInd,t in enumerate(taWords):
    nSim=similar(str(t),finStr)
    if(mSim<=nSim):
        mSim=nSim
        mInd=nInd
print(taWords[mInd])
print (datetime.now() - startTime) 
'''
#Bounding boxes are applied on original image and is displayed
cv2.imshow("output",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''