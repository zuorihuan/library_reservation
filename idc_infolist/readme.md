# 说明

## python 依赖
```
pip install pillow
pip install selenium
pip install pytesseract
```

## chrome 的驱动
准备 chrome 浏览器和对应的驱动，大版本要一致
https://sites.google.com/a/chromium.org/chromedriver/home

驱动的位置要加path环境变量

## ocr 的驱动
安装 tesseract 驱动
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe

把安装路径(默认是C:\Program Files\Tesseract-OCR)加到path环境变量

执行 tesseract -v 有输出即可