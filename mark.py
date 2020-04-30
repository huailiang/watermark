#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: penghuailiang
# @Date  : 4/30/20

import cv2
import os
import numpy as np


def generate_file(file, mark):
    im = cv2.imread("gen/" + file, cv2.IMREAD_UNCHANGED)
    shape = im.shape
    print(file, shape, mark.shape)
    nim = np.zeros(shape)
    pos = (580, 1120)
    for x in range(shape[0]):
        for y in range(shape[1]):
            if pos[0] < x < pos[0] + mark.shape[0] and pos[1] < y < pos[1] + mark.shape[1]:
                color = mark[x - pos[0], y - pos[1]][0:3]
                alpha = mark[x - pos[0], y - pos[1]][3:4]
                rate = alpha / 255.0
                # mark 和 背景图 融合Blend
                nim[x, y] = im[x, y] * (1 - rate) + color * rate
            else:
                nim[x, y] = im[x, y]

    if not os.path.exists("gen2"):
        os.makedirs("gen2")
    cv2.imwrite("gen2/" + file, nim)


def process_main(dir):
    mark = cv2.imread("mark.png", cv2.IMREAD_UNCHANGED)
    # mark 显示调整大小
    mark = cv2.resize(mark, (100, 100))
    for maindir, subdir, files in os.walk(dir):
        list = []
        for file in files:
            if file.endswith(".png"):
                list.append(file)
        list.sort()
        for i, it in enumerate(list):
            generate_file(it, mark)


if __name__ == '__main__':
    process_main("gen/")
