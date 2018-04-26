import cv2
import numpy as np
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import imutils
from imutils import contours

img = cv2.imread('/home/leij/Pictures/bus-test.png')
options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.6,
    'gpu': 0.8
}
tfnet = TFNet(options)

# img = cv2.imread('/home/leij/obj-detection/darkflow-master/bus/bus-photos/IMG_20180421_155655.jpg', cv2.IMREAD_COLOR)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
results = tfnet.return_predict(img)
for i in results:
    if i['label'] == 'bus':
        result = i
        break

tl = (result['topleft']['x'], result['topleft']['y'])
br = (result['bottomright']['x'], result['bottomright']['y'])
label = result['label']
confidence = result['confidence']
busROI = img[tl[1]:br[1],tl[0]:br[0]]
gray = cv2.cvtColor(busROI,cv2.COLOR_RGB2GRAY)

rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, sqKernel)
# plt.imshow(cv2.cvtColor(tophat,cv2.COLOR_GRAY2BGR))

gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
gradX = gradX.astype("uint8")

# apply a closing operation using the rectangular kernel to help
# cloes gaps in between credit card number digits, then apply
# Otsu's thresholding method to binarize the image
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(gradX, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# apply a second closing operation to the binary image, again
# to help close gaps between credit card number regions
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

locs = []
for (i,c) in enumerate(cnts):
    (x,y,w,h) = cv2.boundingRect(c)
    ar = w/float(h)
    if ar > 1 and ar < 3.0:
        if (x > 400 and x < 600) and (y > 0 and y < 100):
            if (w > 10 and w < 60) and (h > 20 and h < 30):
                locs.append((x, y, w, h))
                print(x,y,w,h)

locs = sorted(locs, key=lambda x:x[0])

ref = cv2.imread('/home/leij/Pictures/number.png')
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]

# plt.imshow(cv2.cvtColor(ref,cv2.COLOR_GRAY2RGB))

refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}
# loop over the OCR-A reference contours
for (i, c) in enumerate(refCnts):
# compute the bounding box for the digit, extract it, and resize
# it to a fixed size
    (x, y, w, h) = cv2.boundingRect(c)
    print(i,x,y,w,h)
    roi = ref[y:y + h, x:x + w]
    roi = cv2.resize(roi, (57, 88))
    # update the digits dictionary, mapping the digit name to the ROI
    digits[i] = roi

groupOutput = []
for (i,(x,y,w,h)) in enumerate(locs):
    print(i,x,y,w,h)
    group = gray[y-5:y+h+5,x-5:x+w+5]
    group = cv2.threshold(group, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
#     plt.imshow(group)
    digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
    digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
    
    for c in digitCnts:
        (gX,gY,gW,gH) = cv2.boundingRect(c)
        roi = group[gY:gY+gH,gX:gX+gW]
        roi = cv2.resize(roi,(57,88))
        
        scores = []
        
        for (digit,digitROI) in digits.items():
            result = cv2.matchTemplate(roi,digitROI,cv2.TM_CCOEFF)
            (_,score,_,_) = cv2.minMaxLoc(result)
            scores.append(score)
    groupOutput.append(str(np.argmax(scores)))
cv2.rectangle(busROI, (gX - 5, gY - 5),(gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
cv2.putText(busROI, "".join(groupOutput), (gX, gY - 15),
cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

cv2.imshow("busROI", busROI)
cv2.waitKey(0)