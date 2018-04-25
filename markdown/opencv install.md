sudo apt-get install build-essential cmake pkg-config apt-get install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev -y

apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev -y

apt-get install libgtk-3-dev libatlas-base-dev gfortran -y

apt-get install python2.7-dev python3.5-dev -y


sudo apt-get install build-essential checkinstall cmake pkg-config yasm git gfortran libjpeg8-dev libjasper-dev libpng12-dev libtiff5-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine2-dev libv4l-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev qt5-default libgtk2.0-dev libtbb-dev libatlas-base-dev libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libopencore-amrnb-dev libopencore-amrwb-dev x264 v4l-utils -y



cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.1/modules \
    -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python \
    -D BUILD_EXAMPLES=ON ..

cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.3.1/modules \
      -D BUILD_EXAMPLES=ON ..



``` 
# find out number of CPU cores in your machine
nproc
# substitute 4 by output of nproc
make -j4
sudo make install
sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig
```



``` 
############ For Python 2 ############
## binary installed in dist-packages
/usr/local/lib/python2.6/dist-packages/cv2.so
/usr/local/lib/python2.7/dist-packages/cv2.so
## binary installed in site-packages
/usr/local/lib/python2.6/site-packages/cv2.so
/usr/local/lib/python2.7/site-packages/cv2.so
  

find /usr/local/lib/ -type f -name "cv2*.so"
############ For Python 3 ############
## binary installed in dist-packages
/usr/local/lib/python3.5/dist-packages/cv2.cpython-35m-x86_64-linux-gnu.so
/usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so
## binary installed in site-packages
/usr/local/lib/python3.5/site-packages/cv2.cpython-35m-x86_64-linux-gnu.so
/usr/local/lib/python3.6/site-packages/cv2.cpython-36m-x86_64-linux-gnu.so

############ For Python 2 ############
cd ~/.virtualenvs/facecourse-py2/lib/python2.7/site-packages
ln -s /usr/local/lib/python2.7/dist-packages/cv2.so cv2.so
  
############ For Python 3 ############
cd ~/.virtualenvs/facecourse-py3/lib/python3.6/site-packages
ln -s /usr/local/lib/python3.6/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so


#check
# open ipython (run this command on terminal)
ipython
# import cv2 and print version (run following commands in ipython)
import cv2
print cv2.__version__
# If OpenCV3 is installed correctly,
# above command should give output 3.3.1
# Press CTRL+D to exit ipython
```

