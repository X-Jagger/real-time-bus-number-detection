- docker Dockerfile的使用（多个image在一起使用）

- 安装cudnn出现error 

  > /usr/local/cuda-9.0/targets/x86_64-linux/lib/libcudnn.so.7 is not a symbolic link

  > 尝试解决1 ： 
  >
  > leij@leij:/usr/local/cuda-9.0/targets/x86_64-linux/lib$ sudo mv libcudnn.so.7 libcudnn.7.so
  >
  > leij@leij:/usr/local/cuda-9.0/targets/x86_64-linux/lib$ sudo ln -s libcudnn.7.so libcudnn.so.7 
  >
  >  

  ​

  > $ sudo cp include/cudnn.h /usr/local/cuda-9.1/include
  > $ sudo cp lib64/libcudnn* /usr/local/cuda-9.1/lib64
  > $ sudo chmod a+r /usr/local/cuda-9.1/lib64/libcudnn*
  >
  > ``` 
  > leij@leij:/usr/lib/x86_64-linux-gnu$ sudo ln ./libcudnn /usr/local/cuda-9.0/lib64/libcudnn
  > ```

   erro :chmod: cannot access '/usr/local/cuda-9.0/lib64/libcudnn': Too many levels of symbolic links

  >  用绝对路径来进行ln -s
  >
  >  ``` 
  >  /usr/lib/x86_64-linux-gnu$ sudo ln -s /usr/lib/x86_64-linux-gnu/libcudnn /usr/local/cuda-9.0/lib64/libcudnn
  >  ```
  >

  ​

  tensorflow 查找路径改为cuda-9.0 修改环境变量(这一步不要在虚拟环境下操作)

  >  ```
  >  export PATH=/usr/local/cuda-9.0/bin${PATH:+:${PATH}}
  >  export CUDA_HOME=/usr/local/cuda-9.0
  >  export LD_LIBRARY_PATH=/usr/local/cuda-9.0/lib64/${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
  >
  >  ```

  安装cuda-command-line-tools-9-0

  ``` 
  sudo apt install cuda-command-line-tools-9-0
  LD_LIBRARY_PATH=${LD_LIBRARY_PATH:+${LD_LIBRARY_PATH}:}/usr/local/cuda-9.0/extras/CUPTI/lib64
  ```

  ​

- uninstall cuda-9.1 completely :

  ```
  sudo apt-get --purge remove cuda-9.1
  sudo apt autoremove
  ```

  still during the installation of opencv, cuda-9.1 detected


