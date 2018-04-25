## Docker run 命令参数及使用

### Docker run ：创建一个新的容器并运行一个命令

## 语法

> nvidia-docker run -it tensorflow/tensorflow:latest-gpu bash



```
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]  
```

### OPTIONS说明：

```
01.[root@www ~]# docker run --help  
02.  
03.Usage:  docker run [OPTIONS] IMAGE [COMMAND] [ARG...]  
04.  
05.Run a command in a new container  
06.  
07.  -a, --attach=[]                 Attach to STDIN, STDOUT or STDERR  
08.  --add-host=[]                   Add a custom host-to-IP mapping (host:ip)  
09.  --blkio-weight=0                Block IO (relative weight), between 10 and 1000  
10.  --cpu-shares=0                  CPU shares (relative weight)  
11.  --cap-add=[]                    Add Linux capabilities  
12.  --cap-drop=[]                   Drop Linux capabilities  
13.  --cgroup-parent=                Optional parent cgroup for the container  
14.  --cidfile=                      Write the container ID to the file  
15.  --cpu-period=0                  Limit CPU CFS (Completely Fair Scheduler) period  
16.  --cpu-quota=0                   Limit CPU CFS (Completely Fair Scheduler) quota  
17.  --cpuset-cpus=                  CPUs in which to allow execution (0-3, 0,1)  
18.  --cpuset-mems=                  MEMs in which to allow execution (0-3, 0,1)  
19.  -d, --detach=false            Run container in background and print container ID(后台运行)  
20.  --device=[]                     Add a host device to the container  
21.  --disable-content-trust=true    Skip image verification  
22.  --dns=[]                        Set custom DNS servers  
23.  --dns-opt=[]                    Set DNS options  
24.  --dns-search=[]                 Set custom DNS search domains  
25.  -e, --env=[]                    Set environment variables(设置环境变量)  
26.  --entrypoint=                   Overwrite the default ENTRYPOINT of the image  
27.  --env-file=[]                   Read in a file of environment variables  
28.  --expose=[]                     Expose a port or a range of ports  
29.  --group-add=[]                  Add additional groups to join  
30.  -h, --hostname=                 Container host name  
31.  --help=false                    Print usage  
32. -i, --interactive=false         Keep STDIN open even if not attached(保持容器运行)  
33.  --ipc=                          IPC namespace to use  
34.  --kernel-memory=                Kernel memory limit  
35.  -l, --label=[]                  Set meta data on a container  
36.  --label-file=[]                 Read in a line delimited file of labels  
37. --link=[]                       Add link to another container(容器之间的通讯)  
38.  --log-driver=                   Logging driver for container  
39.  --log-opt=[]                    Log driver options  
40.  --lxc-conf=[]                   Add custom lxc options  
41.  -m, --memory=                   Memory limit  
42.  --mac-address=                  Container MAC address (e.g. 92:d0:c6:0a:29:33)  
43.  --memory-reservation=           Memory soft limit  
44.  --memory-swap=                  Total memory (memory + swap), '-1' to disable swap  
45.  --memory-swappiness=-1          Tuning container memory swappiness (0 to 100)  
46. --name=                         Assign a name to the container(指定容器名称)  
47.  --net=default                   Set the Network for the container  
48.  --oom-kill-disable=false        Disable OOM Killer  
49.  -P, --publish-all=false         Publish all exposed ports to random ports  
50. -p, --publish=[]                Publish a container's port(s) to the host(端口映射 80:8080)  
51.  --pid=                          PID namespace to use  
52.  --privileged=false              Give extended privileges to this container  
53.  --read-only=false               Mount the container's root filesystem as read only  
54.  --restart=no                    Restart policy to apply when a container exits  
55.  --rm=false                      Automatically remove the container when it exits  
56.  --security-opt=[]               Security Options  
57.  --shm-size=                     Size of /dev/shm, default value is 64MB  
58.  --sig-proxy=true                Proxy received signals to the process  
59.  --stop-signal=SIGTERM           Signal to stop a container, SIGTERM by default  
60.  -t, --tty=false                 Allocate a pseudo-TTY  
61.  -u, --user=                     Username or UID (format: <name|uid>[:<group|gid>])  
62.  --ulimit=[]                     Ulimit options  
63.  --uts=                          UTS namespace to use  
64. -v, --volume=[]                 Bind mount a volume(挂载目录 /root:/opt/temp)  
65.  --volume-driver=                Optional volume driver for the container  
66.  --volumes-from=[]               Mount volumes from the specified container(s)  
67.  -w, --workdir=                  Working directory inside the container  
```

## 实例

##### 使用docker镜像nginx:latest以后台模式启动一个容器,并将容器命名为mynginx。

```
docker run --name mynginx -d nginx:latest  
```

##### 使用镜像nginx:latest以后台模式启动一个容器,并将容器的80端口映射到主机随机端口。

```
docker run -P -d nginx:latest  
```

##### 使用镜像nginx:latest以后台模式启动一个容器,将容器的80端口映射到主机的80端口,主机的目录/data映射到容器的/data。

```
docker run -p 80:80 -v /data:/data -d nginx:latest  
```

##### 使用镜像nginx:latest以交互模式启动一个容器,在容器内执行/bin/bash命令。

```
runoob@runoob:~$ docker run -it nginx:latest /bin/bash  
root@b8573233d675:/#   



Usage: docker run [OPTIONS] IMAGE [COMMAND] [ARG...]    
02.  
03.  -d, --detach=false         指定容器运行于前台还是后台，默认为false     
04.  -i, --interactive=false   打开STDIN，用于控制台交互    
05.  -t, --tty=false            分配tty设备，该可以支持终端登录，默认为false    
06.  -u, --user=""              指定容器的用户    
07.  -a, --attach=[]            登录容器（必须是以docker run -d启动的容器）  
08.  -w, --workdir=""           指定容器的工作目录   
09.  -c, --cpu-shares=0        设置容器CPU权重，在CPU共享场景使用    
10.  -e, --env=[]               指定环境变量，容器中可以使用该环境变量    
11.  -m, --memory=""            指定容器的内存上限    
12.  -P, --publish-all=false    指定容器暴露的端口    
13.  -p, --publish=[]           指定容器暴露的端口   
14.  -h, --hostname=""          指定容器的主机名    
15.  -v, --volume=[]            给容器挂载存储卷，挂载到容器的某个目录    
16.  --volumes-from=[]          给容器挂载其他容器上的卷，挂载到容器的某个目录  
17.  --cap-add=[]               添加权限，权限清单详见：http://linux.die.net/man/7/capabilities    
18.  --cap-drop=[]              删除权限，权限清单详见：http://linux.die.net/man/7/capabilities    
19.  --cidfile=""               运行容器后，在指定文件中写入容器PID值，一种典型的监控系统用法    
20.  --cpuset=""                设置容器可以使用哪些CPU，此参数可以用来容器独占CPU    
21.  --device=[]                添加主机设备给容器，相当于设备直通    
22.  --dns=[]                   指定容器的dns服务器    
23.  --dns-search=[]            指定容器的dns搜索域名，写入到容器的/etc/resolv.conf文件    
24.  --entrypoint=""            覆盖image的入口点    
25.  --env-file=[]              指定环境变量文件，文件格式为每行一个环境变量    
26.  --expose=[]                指定容器暴露的端口，即修改镜像的暴露端口    
27.  --link=[]                  指定容器间的关联，使用其他容器的IP、env等信息    
28.  --lxc-conf=[]              指定容器的配置文件，只有在指定--exec-driver=lxc时使用    
29.  --name=""                  指定容器名字，后续可以通过名字进行容器管理，links特性需要使用名字    
30.  --net="bridge"             容器网络设置:  
31.                                bridge 使用docker daemon指定的网桥       
32.                                host    //容器使用主机的网络    
33.                                container:NAME_or_ID  >//使用其他容器的网路，共享IP和PORT等网络资源    
34.                                none 容器使用自己的网络（类似--net=bridge），但是不进行配置   
35.  --privileged=false         指定容器是否为特权容器，特权容器拥有所有的capabilities    
36.  --restart="no"             指定容器停止后的重启策略:  
37.                                no：容器退出时不重启    
38.                                on-failure：容器故障退出（返回值非零）时重启   
39.                                always：容器退出时总是重启    
40.  --rm=false                 指定容器停止后自动删除容器(不支持以docker run -d启动的容器)    
41.  --sig-proxy=true           设置由代理接受并处理信号，但是SIGCHLD、SIGSTOP和SIGKILL不能被代理    
```