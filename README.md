# 电脑接短信--实现短信验证码自动在PC端同步

## 效果展示

收到验证码后，自动拦截短信发送到电脑端，在电脑右下角有托盘消息提示，并自动复制到Windows剪贴板中，直接粘贴就可以。

![image-20240812233032541](README.assets/image-20240812233032541.png)

![image-20240812233253703](README.assets/image-20240812233253703.png)



## 实现步骤

### 1.安装短信转发器SmsForwarder

在安卓手机上安装短信转发器SmsForwarder
https://github.com/pppscn/SmsForwarder

### 2.SmsForwarder配置
注意！一般手机都默认开启了验证码安全保护，需要在设置里面搜索验证码进行关闭。

SmsForwarder基础配置参考官方wikihttps://gitee.com/pp/SmsForwarder/wikis/pages

**pushplus配置参考**

博客：https://www.amjun.com/485.html

视频：https://www.youtube.com/watch?v=Bkt6QpkoVfw&t=272s



### 3.Socket配置

需要手机与电脑在同一局域网下


**A.将代码clone到本地部署运行**

clone项目

```bash
git clone git@github.com:lzhdelife/SMS.git
cd SMS
```

安装依赖

```bash
pip install -r requirements.txt
```

运行`main.py`

```bash
python main.py
```



**B.发送通道配置如下**

端口写65432，程序中socket接收端口设置为了65432，可以在`config.json`文件中修改

<img src="README.assets/image-20240812230315063.png" alt="image-20240812230315063" style="zoom: 33%;" />

注：每次发送完消息后，有报错：
```
WNDPROC return value cannot be converted to LRESULT
TypeError: WPARAM is simple, so must be an int object (got NoneType)
```
这个问题不影响正常使用，只是看起来不太舒服。
参见<https://github.com/jithurjacob/Windows-10-Toast-Notifications/pull/115>，是由于win10toast里一个函数的返回值类型有误。由于win10toast在2018年之后已经不再接受pr，这个问题只能本地手动修复。
具体修复方法为：将win10toast的`__init__.py`中最后一行`on_destroy`函数的返回值从None换为0。
