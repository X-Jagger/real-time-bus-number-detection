import cv2
import numpy as np
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import imutils
from imutils import contours
import time

option = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.5,
    'gpu': 0.8
}

tfnet = TFNet(option)

#judge Number map
judge_number_map = {}

bus_number = False
# number
ref = cv2.imread('/home/leij/Pictures/number.png')
# ref = imutils.resize(ref, width=300)
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]

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
    roi = ref[y-2:y + h+2, x-2:x + w+2]
    roi = cv2.resize(roi, (57, 88))
    # update the digits dictionary, mapping the digit name to the ROI
    digits[i] = roi


capture = cv2.VideoCapture('/home/leij/Videos/bus-test.mp4')
# capture = cv2.VideoCapture('/home/leij/Videos/video1.mp4')
# colors = [tuple(255 * np.random.rand(3)) for i in range(10)]

# capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH,640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('/home/leij/Videos/test.mp4',fourcc,20.0,(640,480))

while True:
    stime = time.time()
    ret, frame = capture.read()
    if ret:
        results = tfnet.return_predict(frame)
        for i in results:
            if i['label'] == 'bus':
                result = i
                break

        tl = (result['topleft']['x'], result['topleft']['y'])
        br = (result['bottomright']['x'], result['bottomright']['y'])
        label = result['label']
        confidence = result['confidence']
        #draw frame box
        frame = cv2.rectangle(frame, tl, br, (0, 0, 255), 7)
        frame = cv2.putText(frame, label, tl, cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
        
        busROI = frame[tl[1]:br[1],tl[0]:br[0]]
        gray = cv2.cvtColor(busROI,cv2.COLOR_RGB2GRAY)
        
        #store old shape and ratio
        oldShape = gray.shape
        ratio = float(oldShape[1]) / 600
        gray = imutils.resize(gray,width=600)

        rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
        sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, sqKernel)
        plt.imshow(cv2.cvtColor(tophat,cv2.COLOR_GRAY2BGR))

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
        plt.imshow(cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR))

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        locs = []
        for (i,c) in enumerate(cnts):
            (cX,cY,cW,cH) = cv2.boundingRect(c)
            ar = cW/float(cH)
            if ar > 1 and ar < 3.0:
                if (cX > 400 and cX < 600) and (cY > 10 and cY < 80):
                    if (cW > 10 and cW < 50) and (cH > 20 and cH < 30):
                        locs.append((cX, cY, cW, cH))
                        # print('only one is right',x,y,w,h)
        # locs = sorted(locs, key=lambda x:x[0])
        
        #最准确应该只有一个bus number
        for (i,(x,y,w,h)) in enumerate(locs):
            groupOutput = []
            print(i,x,y,w,h)
            group = gray[y:y+h,x:x+w]
            group = cv2.threshold(group, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            plt.imshow(group)
            digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
            digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
            
            #数字三位数以内才有效并且
            if len(digitCnts) <= 3:
                for c in digitCnts:
                    (gX,gY,gW,gH) = cv2.boundingRect(c)
                    roi = group[gY:gY+gH,gX:gX+gW]
                    
                    roi = cv2.resize(roi,(57,88))
                    
            #         plt.imshow(roi)
                    scores = []
                    
                    for (digit,digitROI) in digits.items():
                        result = cv2.matchTemplate(roi,digitROI,cv2.TM_CCOEFF)
                        
                        (_, score, _, _) = cv2.minMaxLoc(result)
                        scores.append(score)
                    # print(scores)
                    groupOutput.append(str(np.argmax(scores)))
                    print('groupOutput is',groupOutput)
                # draw number and box   
                tlX = int (tl[0] + (x-5) * ratio)
                tlY = int(tl[1] + (y-5) * ratio)
                brX = int(tl[0] + (x+w+5) * ratio)
                brY = int(tl[1] + (y+h+5) * ratio)
                bus_temp_number = "".join(groupOutput)
                if bus_temp_number in judge_number_map :
                    judge_number_map[bus_temp_number] += 1
                    count = judge_number_map[bus_temp_number]
                    if (int(count) > 30 ):
                        bus_number = bus_temp_number
                        break
                else :
                    judge_number_map[bus_temp_number] = 1

                cv2.rectangle(frame, (tlX, tlY),(brX, brY), (0, 255, 0), 2)
                cv2.putText(frame, bus_temp_number, (tlX, tlY-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
            print("Bus Number is #: {}".format("".join(groupOutput)))
                
        out.write(frame)
        # cv2.imshow("busROI", busROI)
        cv2.imshow('frame', frame)
        if(bus_number):
            print('The final result bus number is',bus_number)
            break
        # print('FPS {:.1f}'.format(1 / (time.time() - stime)))
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
capture.release()
out.release()
cv2.destroyAllWindows()
