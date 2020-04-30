#!/bin/bash

# ==============================================
# This tool is remove watermark in short-clips
# such as 抖音, 微视
# ----------------------------------------------
# Author: Huailiang.Peng
# Data:   2020.02.07
# ==============================================


if [ $# < 1 ] ; then
echo "请传入视频的路径"
exit 1;
fi


# ${1} 视频的地址 如douyin.mp4
ffmpeg -i ${1} -r 25 -f image2 image-%04d.png

mkdir -p hd/

mv image-*.png hd/

mkdir -p gen/

python extract.py

cd gen/

ffmpeg -i image-%04d.png generated.mp4

mv generated.mp4 ..
