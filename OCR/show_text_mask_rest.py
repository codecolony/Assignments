import cv2
import numpy as np
#import skimage.morphology as smp

'''
prerequisite
* some hands on practice on manipulation of 2d spectrums will make things much easier to grasp
** http://www.jcrystal.com/ 'FTL - SE' can be used to easily try stuff out
** try the phase spectrum filtering there
* dct was used here because it's just simpler to manipulate. dft can also be used to get the same effect

outline
* the main 'aha' was to notice that even afer a very large portion of the orignal specturm was zero/ed out,
  the area of interest fails to completely disappear unlike the rest. so the solution trys to box that part
* also note that the text of interest is always horizontal,so throwing away more vertical components bring it out even more

'''
cv2.namedWindow('img',0)
cv2.namedWindow('dct before',0)
cv2.namedWindow('dct after',0)
cv2.namedWindow('low freq suppressed',0)
cv2.namedWindow('bring out black gaps',0)
cv2.namedWindow('connect them together',0)
cv2.namedWindow('auto thresh',0)
cv2.namedWindow('boxmask',0)
cv2.namedWindow('done',0)


img = cv2.imread('./out_hor.jpg')
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

orig=gray.copy()
gray = gray.astype('float32')
gray/=255
dct=cv2.dct(gray)

dctvis=cv2.normalize(np.log(dct.copy()),-1,0,1,cv2.NORM_MINMAX)
cv2.imshow('dct before',dctvis)

vr=1.#vertical ratio, how much percentage of vertical freq components should be thrown away
hr=.95#horizontal
dct[0:vr*dct.shape[0],0:hr*dct.shape[1]]=0

dctvis=cv2.normalize(np.sqrt(dct.copy()),-1,0,1,cv2.NORM_MINMAX)
cv2.imshow('dct after',dctvis)
gray=cv2.idct(dct)
gray=cv2.normalize(gray,-1,0,1,cv2.NORM_MINMAX)
gray*=255
gray=gray.astype('uint8')

cv2.imshow('low freq suppressed',gray)
gray=cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT,#smp.disk(7)
    cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15)),
    iterations=1)
cv2.imshow('bring out black gaps',gray)
gray=cv2.morphologyEx(gray, cv2.MORPH_DILATE,#smp.disk(5), 
    cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11)),
    iterations=1)
cv2.imshow('connect them together',gray)
gray=cv2.threshold(gray,0,255,cv2.THRESH_OTSU)[1]
cv2.imshow('auto thresh',gray)

contours,hierarchy = cv2.findContours(gray,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
boxmask=np.zeros(gray.shape,gray.dtype)
for i in xrange(len(contours)):
    x,y,w,h = cv2.boundingRect(contours[i])
    cv2.rectangle(boxmask,(x,y),(x+w,y+h),color=255,thickness=-1)
cv2.imshow('boxmask',boxmask)
cv2.imshow('done',img&cv2.cvtColor(boxmask,cv2.COLOR_GRAY2BGR))
cv2.imwrite("text_crop2.jpg", img&cv2.cvtColor(boxmask,cv2.COLOR_GRAY2BGR))
cv2.waitKey(0)