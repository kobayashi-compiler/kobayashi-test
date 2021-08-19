# 一份很菜但能用的第三方评测机

这个软件在一台服务器和一块可信树莓派上运行评测服务，对所有测例多次运行取平均，并避免无意义的网络传输

服务器和树莓派通过 HTTP 通信，通过 HTTP 请求触发一轮评测，因此服务器和树莓派都需要有稳定的套接字

服务器暴露的 API：

1. `/hook`
    
    触发评测，拉取 master 分支内容，可以在开发时设置 gitlab webhook 自动触发

2. `/hook/<commit>`

    触发评测，拉取 \<commit\> 分支内容

3. `?f=<arg1>&f=<...>&p=<pass>`
    
    在触发评测时给定 `arg` 等命令行参数，并用 `pass` 作为密码鉴权

4. `/results/`

    按照顺序保存了评测结果文件夹，其中 `clang` 与 `gcc` 为对比，`best` 是本队的最佳提交记录

5. `/best`

    手动调整结果文件后刷新最佳记录

其中 `clang` 的编译指令为

```bash
clang -S -x c {basename}.sy -include kslib.h -std=gnu99 --target=armv7-unknown-linux-eabi -march=armv7a -mcpu=cortex-a72 -mfpu=neon -mfloat-abi=hard -O3 -Ofast -fvectorize -no-integrated-as
```

`gcc` 的编译指令为

```bash
arm-linux-gnueabihf-g++ -S -x c++ {basename}.sy -include kslib.h -mcpu=cortex-a72 -mfpu=neon -mfloat-abi=hard -O3 -Ofast
```

为了保证 `-x c++` 兼容性，改动 `kslib.h` 在 `master` 文件夹下

## 搭建概要

### 树莓派

你可能需要一些基础 Linux 和 nginx 知识以继续

先看树莓派侧，以下文件均指 `worker/` 下的文件

首先安装依赖，可能还需要自己根据报错调整

```bash
sudo apt install nginx python3-pip redis
pip3 install uwsgi flask redis
```

以及创建一个 `wsgi` 用户并添加到 `www-data` 组

```bash
sudo useradd wsgi -g www-data
```

然后创建文件夹 `/var/www/duck`，并将 `duck.py` `wsgi.py` `duck.ini` 复制到文件夹内，之后更改所有者

```bash
sudo chown wsgi:www-data -R /var/www/duck
```

新建服务，创建 `/etc/systemd/system/duck.service`，内容为 `duck.service`，然后启用服务

```bash
sudo systemctl enable duck
sudo systemctl start duck
```

之后配置 nginx，新建 `/etc/nginx/sites-available/duck.conf`，内容为 `duck.conf`，然后软链接启用，默认端口为 8987

```bash
sudo ln -s /etc/nginx/sites-available/duck.conf /etc/nginx/sites-enabled/
```

推荐使用 `acme.sh` 创建 SSL 证书，也可以跳过这步，配置文件在 `nyars.conf` 中

然后检查并开启 nginx 服务

```bash
sudo nginx -t
sudo nginx -s reload
```

之后访问树莓派的 IP:8987 应该可以看到文字提示

对于以上内容如果有问题可以参考 https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uswgi-and-nginx-on-ubuntu-18-04

需要拉取文件，具体来说，你需要拉取官方仓库，并把测例链接到 `/var/www/duck/testcases`

```bash
git clone git@gitlab.eduxiji.net:nscscc/compiler2021.git
ln -s /var/www/compiler2021/公开../ /var/www/testcases
ln -s /var/www/compiler2021/公开../20../h_functional /var/www/testcases/h_functional
```

你还需要把 `libsysy.a` 放在 `/var/www/duck` 下

### 服务器

然后看服务器配置，以下文件均指 `master/` 下的文件

继续配置网站直到上线，与树莓派无异

你需要把 `judge.sh` 放在 `/var/www/duck` 下，这是一份写的很糟糕的脚本，但至少能跑

同样地拉取官方仓库并链接，然后把 `judge.py` 放在 `/var/www/duck/testcases` 下，你需要更改其中的 `BASE` 变量为树莓派的访问地址，以及把 `kslib.h` 放在文件夹中

然后拉取你的编译器到 `/var/www/duck/thu-cs-compiler`，评测脚本会切换到指定 commit 并以如下方式编译测评，编译器位置为 `build/main`

```bash
cd build
cmake ..
make -j$(nproc)
```

可能会需要安装 `antlr` 等工具，建议先手动运行再批量测试

看着这篇简单的教程估计很大几率中途会有各种各样的问题，需要根据报错进一步处理
