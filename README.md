# 高清图片下载

问题起因：拍卖行拍品高清图片显示的通用做法，是通过zoom功能可以显示，
网页屏蔽掉右键功能使得图片不能下载。

Bruun-Rasmussen拍卖行是同样的处理，分析页面代码，通过下载高清图不同区块，
最终合成一张高清图。

别家拍行的高清图下载可以参考这个代码


## 目录

- [安装](#安装)
- [使用方法](#使用方法)
- [功能](#功能)
- [贡献](#贡献)
- [许可证](#许可证)

## 安装

1. 克隆仓库：

   ```bash
   git clone https://github.com/wooexpand/HDImageDownload.git
   cd yourproject
   ```

2. 创建并激活虚拟环境：

   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   .\venv\Scripts\activate   # Windows
   ```

3. 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

python Bruun-Rasmussen.py 拍品链接

python Bruun-Rasmussen.py https://bruun-rasmussen.dk/m/lots/A7EA1EB4A145?category_id=462
