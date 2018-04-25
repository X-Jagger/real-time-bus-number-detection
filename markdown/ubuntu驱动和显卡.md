ubuntu解决分辨率

sudo ~./profile

最后空行添加
cvt 1920 1080
xrandr --newmode "1920x1080_60.00"  173.00  1920 2048 2248 2576  1080 1083 1088 1120 -hsync +vsync
xrandr --addmode eDP-1 "1920x1080_60.00"

ubuntu 解决显卡问题

1.开机启动界面,在ubuntu那里按e， 然后在linux开头的那一行末尾空一格输入 "nouveau.modeset=0" ,再按F10即可正常进入电脑
2.屏蔽开源驱动nouveau 
sudo gedit /etc/modprobe.d/blacklist.conf
最后一行添加以下内容病保存 

blacklist vga16fb 
blacklist nouveau 
blacklist rivafb 
blacklist rivatv 
blacklist nvidiafb
//最后这里有空行

//卸载其他驱动
sudo apt-get purge nvidia*
3.更新内核
sudo update-initramfs -u
4.安装nvidia.run 
alt+ctrl+f1 进入非图形界面
sudo service lightdm stop
sudo ./nivida.run --no-opengl-files,后续选择yes

检测是否安装成功
sudo nvidia-smi
sudo nvidia-settings
