#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import os.path
import re
import sys
import urllib
import urllib3
from tkinter import *
from excel_tool import *
import tkinter.filedialog
import threading
import hashlib
import requests

urllib3.disable_warnings()


def md5(message, salt=''):
    new_s = str(message) + salt
    m = hashlib.md5(new_s.encode())
    return m.hexdigest()

# 图片类


class Picture(object):

    def __init__(self, name, url, dir_path):
        # 图片名
        self.name = name
        # 图片链接
        self.url = url
        # 图片保存路径
        self.dir_path = dir_path
        # 图片下载失败原因
        self.error_reason = None

    # 开始下载
    def start_download_pic(self, download_pic_callback):
        pic_path = self.build_pic_name()

        # 已存在则不重复下载
        if os.path.exists(pic_path):
            print('pic has existed:' + self.url)
            self.error_reason = "pic has existed:"
            download_pic_callback(self)
            return

        # 图片链接前缀不包含http
        if not self.url.startswith("http"):
            print('pic has invalid url:' + self.url)
            self.error_reason = "pic has invalid url"
            download_pic_callback(self)
            return

        # 下载图片
        try:
            response = requests.get(
                self.url, proxies=None, verify=False)
        # 下载失败
        except Exception as error:
            print('pic cannot download:' + self.url)
            self.error_reason = str(error)
            download_pic_callback(self)
            return

        # 保存图片
        try:
            fp = open(pic_path, 'wb')
            fp.write(response.content)
            fp.close()
        # 保存失败
        except IOError as error:
            print(error)
            self.error_reason = str(error)
            download_pic_callback(self)
            return

        # 下载完成回调
        download_pic_callback(self)

    # 组装图片名字
    def build_pic_name(self):
        # 剪去图片链接后的参数
        pic_url = self.url.split("?")[0]

        # 获取图片格式后缀 如果没有 默认jpg
        urls = pic_url.split(".")
        if len(urls) > 1:
            pic_type = urls[-1]
        else:
            pic_type = "jpg"

        pic_name = self.name+'.'+pic_type

        pic_path = os.path.join(self.dir_path, pic_name)
        return pic_path


class XTImageDownloader(object):

    def __init__(self):
        # 数据
        self.download_error_list = []
        self.all_pic_count = 0
        self.current_pic_index = 0
        self.thread_lock = threading.Lock()
        self.search_button = None
        # 图形界面相关
        self.root = Tk()
        # 窗口不可调整大小
        self.root.title("XTImageDownloader")
        self.root.resizable(False, False)
        self.root.update()  # 必须
        self.path = StringVar()
        self.title = StringVar()
        self.title.set("请选择图片的Excel")
        self.list_box = None
        Label(self.root, textvariable=self.title).grid(row=0, column=1)
        Label(self.root, text="文件路径:").grid(row=1, column=0)
        Entry(self.root, textvariable=self.path).grid(row=1, column=1)
        Button(self.root, text="选择路径", command=self.select_path).grid(
            row=1, column=2)
        self.root.mainloop()

    # 选择文件夹
    def select_path(self):
        dir1 = tkinter.filedialog.askopenfilename(
            title=u'选择Excel文件')
        print(dir1)
        self.path.set(dir1)
        # 用户选中文件夹之后 显示下载按钮
        if self.path.get() != "":
            self.search_button = Button(
                self.root, text="开始下载", command=self.start_search_dir)
            self.search_button.grid(row=2, column=1)
            print(self.path)
            return self.path

    # 开始搜索文件夹 并且下载
    def start_search_dir(self):
        pass
        self.search_button['state'] = DISABLED
        self.search_button['text'] = "正在下载..."

        self.all_pic_count = 0
        self.current_pic_index = 0
        self.download_error_list = []

        r = ReadExcel(self.path.get(), "数据表1")
        pic_url_cells = r.read_data([1])
        self.all_pic_count = len(pic_url_cells)
        self.change_title(self.all_pic_count, self.current_pic_index)

        # 拼接文章图片下载后保存的路径
        self.result_pic_dir = self.path.get() + '_result'
        # 如果该文件夹不存在 则新建一个
        if not os.path.exists(self.result_pic_dir):
            os.mkdir(self.result_pic_dir)

        for pic_url_cell in pic_url_cells:
            url = pic_url_cell['img_url']
            name = md5(url)
            # 将图片加入到图片数组当中
            pic = Picture(name, url,
                          self.result_pic_dir)
            # 开启异步线程下载图片 并且传入下载完成的回调
            thread = threading.Thread(
                target=pic.start_download_pic, args=(self.download_pic_callback,))
            thread.start()

    # 下载图片完成后的回调函数
    def download_pic_callback(self, pic):
        # 获取线程锁
        self.thread_lock.acquire()
        # 如果下载失败 则保存到失败列表
        if pic.error_reason is not None and len(pic.error_reason) > 0:
            self.download_error_list.append(pic)

        self.current_pic_index += 1

        # 更新下载进度 刷新UI
        print('finish:' + str(self.current_pic_index) +
              '/' + str(self.all_pic_count))
        self.change_title(self.all_pic_count, self.current_pic_index)

        # 全部下载成功 刷新UI 生成失败报告
        if self.all_pic_count == self.current_pic_index:
            self.search_button['text'] = "下载完成"
            self.print_error(self.download_error_list)

        # 释放锁
        self.thread_lock.release()

    # 更新下载进度 刷新UI
    def change_title(self, total_num, current_num):
        self.title.set("已完成" + str(current_num) + "/" + str(total_num))

    # 生成失败列表
    def print_error(self, download_error_list):
        # python log
        print("-----------------------------------")
        print("some pic download failure:")
        for pic in download_error_list:
            print("")
            print("name:" + pic.name)
            print("url:" + pic.url)
            print("error_reason:" + pic.error_reason)

        Label(self.root, text="部分图片下载失败:").grid(row=4, column=1)

        # GUI
        # 新建listbox
        self.list_box = Listbox(self.root)
        for pic in download_error_list:
            self.list_box.insert(END, pic.url + " -> " + pic.error_reason)
        self.list_box.grid(row=5, column=0, columnspan=3, sticky=W+E+N+S)

        # 垂直 scrollbar
        scr1 = Scrollbar(self.root)
        self.list_box.configure(yscrollcommand=scr1.set)
        scr1['command'] = self.list_box.yview
        scr1.grid(row=5, column=4, sticky=W+E+N+S)
        # 水平 scrollbar
        scr2 = Scrollbar(self.root, orient='horizontal')
        self.list_box.configure(xscrollcommand=scr2.set)
        scr2['command'] = self.list_box.xview
        scr2.grid(row=6, column=0, columnspan=3, sticky=W+E+N+S)


dir_picker = XTImageDownloader()
