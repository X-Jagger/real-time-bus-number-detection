
import cv2
from darkflow.net.build import TFNet
import matplotlib.pyplot as plt
import numpy as np
import imutils
# %config InlineBackend.figure_format = 'svg'


# define the model options and run
options = {
    'model': 'cfg/yolo.cfg',
    'load': 'bin/yolov2.weights',
    'threshold': 0.6,
    'gpu': 0.8
}

tfnet = TFNet(options)


# # read the color image and covert to RGB

img = cv2.imread('/home/leij/obj-detection/darkflow-master/bus/bus-photos/IMG_20180421_155655.jpg', cv2.IMREAD_COLOR)

img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# use YOLO to predict the image
result = tfnet.return_predict(img)

img.shape


# pull out some info from the results

colors = [tuple(255 * np.random.rand(3)) for i in range(10)]
results = tfnet.return_predict(img)
for color, result in zip(colors, results):
    tl = (result['topleft']['x'], result['topleft']['y'])
    br = (result['bottomright']['x'], result['bottomright']['y'])
    label = result['label']
    confidence = result['confidence']
    text = '{}:{:.0f}%'.format(label,confidence*100)
    if (label == 'bus'):
        img = cv2.rectangle(img, tl, br, color, 7)
        img = cv2.putText(img, text, tl, cv2.FONT_HERSHEY_COMPLEX, 10, (0, 0, 0), 22)
img = imutils.resize(img, width=600)
cv2.imshow('img', img)
cv2.waitKey()
# plt.imshow(img)
# plt.show()
# tl = (result[0]['topleft']['x'], result[0]['topleft']['y'])
# br = (result[0]['bottomright']['x'], result[0]['bottomright']['y'])
# label = result[0]['label']


# # add the box and label and display it
# img = cv2.rectangle(img, tl, br, (0, 255, 0), 7)
# img = cv2.putText(img, label, tl, cv2.FONT_HERSHEY_COMPLEX, 10, (0, 0, 0), 13)
# plt.imshow(img)
# plt.show()

# plt.figure(figsize=IMAGE_SIZE)
# plt.imshow(img)
#     cv.imshow('TensorFlow MobileNet-SSD', img)
#     cv.waitKey()