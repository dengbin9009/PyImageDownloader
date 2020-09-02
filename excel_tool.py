#!/usr/bin/env python
# -*- coding: utf-8 -*-
import openpyxl


class Case:
    pass


class ReadExcel(object):
    def __init__(self, filename, sheetname):
        self.wb = openpyxl.load_workbook(filename)
        self.sheet = self.wb[sheetname]
        # list1 参数为一个列表，传入的是指定读取数据的列,比如[1,2,3]
        # 每一行[1,3,5]列的数据，读取出来就作为一条测试用例，放在字典中
        # 所有的用例放在列表中并且进行返回

    def read_data(self, list1):
        """
        :param list1:  list--->要读取列   list类型
        :return:    返回一个列表，每一个元素为一个用例（用例为dict类型）
        """
        # 获取最大的行数
        max_r = self.sheet.max_row
        cases = []  # 定义一个空列表，用来存放所有的用例数据
        titles = []  # 定义一个空列表，用来存放表头
        # 遍历所有的行数据
        for row in range(1, max_r+1):
            if row != 1:  # 判断是否是第一行
                case_data = []  # 定义一个空列表，用来存放该行的用例数据
                for column in list1:
                    info = self.sheet.cell(row, column).value
                    # print(info)
                    case_data.append(info)
                    # print(list(zip(titles,case_data)))
                # 将该条数据和表头进行打包组合,作用相当于dict(list(zip(titles,case_data)))
                case = dict(zip(titles, case_data))
                # print(case)
                cases.append(case)
                # print(cases)
            else:  # 获取表头数据
                for column in list1:
                    title = self.sheet.cell(row, column).value
                    titles.append(title)
                # print(titles)
        return cases


if __name__ == '__main__':
    r = ReadExcel("花呗.xlsx", "数据表1")
    res = r.read_data([1])
    for o in res:
        print(o['img_url'])
