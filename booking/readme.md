# 说明

## python 依赖
```
pip install requests
pip install pytesseract
pip install retrying # 当发生异常或者失败时重试
```


## ocr 的驱动
安装 tesseract 驱动
https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe

把安装路径(默认是D:\Program Files\Tesseract-OCR\tesseract.exe)加到path环境变量

执行 tesseract -v 有输出即可