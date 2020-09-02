
# 改为从Excel中获取url，批量下载图片




##  Python 打包工具

![最终效果](http://upload-images.jianshu.io/upload_images/1319710-aa888cebfdb37e99.gif?imageMogr2/auto-orient/strip%7CimageView2/2/w/440)


这部分主要是讲如何把 Python 脚本打包打包成可以在 Mac 上运行的应用。



### [PyInstaller](http://www.pyinstaller.org/)

[图片上传失败...(image-fd72fe-1516382674300)]

PyInstaller 是一个打包工具，可以帮助你打包 Python 脚本，生成应用。

安装 PyInstaller

```
$ pip install pyinstaller
```

打包后在``dist``文件夹中可找到可执行文件
```
$ pyinstaller yourprogram.py
```
生成 app
```
$ pyinstaller --onedir -y  main.spec
```

### [py2app](https://pypi.python.org/pypi/py2app/)

py2app 也是打包工具，这里只是简单介绍一下，想要深入了解详细内容可以自行搜索。


切换到你的工程目录下

```
$ cd ~/Desktop/yourprogram
```

生成 setup.py 文件
```
$ py2applet --make-setup yourprogram.py
```

生成你的应用

```
$ python setup.py py2app
```

### [DMG Canvas](http://www.araelium.com/dmgcanvas)

![DMGCanvas](http://upload-images.jianshu.io/upload_images/1319710-a6044f67873d682a.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/140)

DMG Canvas 可以将 Mac 应用打包成 DMG 镜像文件，并且傻瓜式操作。

## 总结
刚开始只是写了很简单的一部分功能，后来慢慢完善，逐渐才有了现在的样子，在这个过程中学到了很多东西，包括 Python 中的 GUI 和多线程操作，如何生成应用程序。希望能对一部分人有所帮助。


**最后贴上[Demo](https://github.com/xietao3/PyImageDownloader)，本人 Python 2.7 环境下运行的， Python 3以上是无法运行的。**



