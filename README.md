# 简介
开始只是想用scrapy简单下载 [apkmonk](https://www.apkmonk.com/) 上的apk文件, 但是经过测试,发现通过scrapy自带的下载器或者通过自定义中间件的方法都不能获得满速下载(速度非常鸡肋),因此考虑使用系统自带的wget下载

scrapy在这里仅仅获取apk的真实url, 并把url放到redis队列中(使用redis并不是为了分布式), 然后单独写了一个python脚本从redis队列中获取apk链接, 并调用wget进行多进程下载.

最后, 由于时间有限(能力太渣), 发现scrapy经常爬取速度快了以后, wget跟不上, 导致出现了太多的wget进程, 因此最后又写了一个控制脚本control.py, 根据wget的进程数量对scrapy进行暂停(pause)和恢复(unpause)操作

# 用法
### 1. 安装所需要的Python包
    pip install -r requirements.txt

### 2. 安装redis
    apt-get install redis-server

### 3. 运行redis
    redis-server

### 4. 运行Scrapy
##### 如果在CLI中运行,执行:
    1. python start_download.py
    2. scrapy crawl apkmonk

##### 如果导入IDE运行,执行
    1. start_download.py
    2. start_scrapy.py

### 5. 运行control.py
    python control.py

## NOTE
由于众所周知的原因,国内下载apkmonk中的软件经常出现速度慢如蜗牛的状况,因此使用了proxychains进行了加速(科学上网), 请事先配置好proxychains,
也可不使用proxychains, 只需更改start_download.py第35行, 将proxychains删除

