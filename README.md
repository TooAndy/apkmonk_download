# Usage
### 安装所需要的Python包
    pip install -r requirements.txt

### 安装redis
    apt-get install redis-server

### 运行redis
    redis-server

### 如果在CLI中运行,执行:
    1. python start_download.py
    2. scrapy crawl apkmonk

### 如果导入IDE运行,执行
    1. start_download.py
    2. start_scrapy.py

## NOTE
由于众所周知的原因,国内下载apkmonk中的软件经常出现速度慢如蜗牛的状况,因此使用了proxychains进行了加速(科学上网), 请事先配置好proxychains,
也可不使用proxychains, 只需更改start_download.py第35行, 将proxychains删除