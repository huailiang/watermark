#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: penghuailiang
# @Date  : 2/7/20


import cv2
import os
import numpy as np


def generate_filter(file):
    print(file)
    im = cv2.imread("hd/" + file)
    shape = im.shape
    nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)

    st_lt = 0
    for x in range(0, 120):
        for y in range(10, 290):
            px = im[x, y]
            if sum(px) > 640:
                nim[x, y] = 255
                st_lt = st_lt + 1
    if st_lt < 1000:
        nim = np.zeros((shape[0], shape[1]), dtype=np.uint8)  # clear
        for x in range(1100, 1280):
            for y in range(410, 719):
                px = im[x, y]
                if sum(px) > 700:
                    nim[x, y] = 255
    # cv2.imwrite("filter/"+file, nim)
    return nim


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
    process_main("hd/")
