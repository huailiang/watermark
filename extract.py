#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: penghuailiang
# @Date  : 2/7/20


import cv2
import os
import sys
import numpy as np

rect = (120, 280)  # (H, W) 水印框大小
pos1 = (0, 10)  # 左上角位置
pos2 = (580, 1000)  # 右下角位置


# 提取水印, 生成存放在filter目录
def generate_filter(file):
    print(file)
    im = cv2.imread("hd/" + file)
    shape = im.shape
    nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)
    st_lt = 0
    for x in range(pos1[0], pos1[0] + rect[0]):
        for y in range(pos1[1], pos1[1] + rect[1]):
            px = im[x, y]
            if sum(px) > 640:
                nim[x, y] = 255
                st_lt = st_lt + 1  # 像素超过一定数量就判定为右下角， 否则水印在左上角
    if st_lt < 1000:
        nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)  # clear
        for x in range(pos2[0], pos2[0] + rect[0]):
            for y in range(pos2[1], pos2[1] + rect[1]):
                px = im[x, y]
                if sum(px) > 700:
                    nim[x, y] = 255
    # 这里提取的水印的灰度图
    if not os.path.exists("filter"):
        os.makedirs("filter")
    cv2.imwrite("filter/" + file, nim)
    return nim


# 卷积过滤水印， 保存在gen目录
def generate_file(file):
    print(file)
    mask = generate_filter(file)
    kernel = np.ones((3, 3), np.uint8)
    im = cv2.imread("hd/" + file)
    dilate = cv2.dilate(mask, kernel, iterations=3)
    sp = cv2.inpaint(im, dilate, 7, flags=cv2.INPAINT_TELEA)
    sp = cv2.bilateralFilter(sp, 5, 280, 50)
    cv2.imwrite("gen/" + file, sp)


def process_main(dir):
    for maindir, subdir, files in os.walk(dir):
        list = []
        for file in files:
            if file.endswith(".png"):
                list.append(file)
        list.sort()
        for i, it in enumerate(list):
            generate_file(it)


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) > 2:
        rect = (sys.argv[1], sys.argv[2])
    if len(sys.argv) > 4:
        pos1 = (sys.argv[3], sys.argv[4])
    if len(sys.argv) > 6:
        pos2 = (sys.argv[5], sys.argv[6])
    process_main("hd/")
