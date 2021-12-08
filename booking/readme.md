# 说明

## python 依赖
```
pip install requests
pip install pytesseract
pip install retrying
```

## ocr 的驱动
[安装 tesseract 驱动](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v4.1.0.20190314.exe)

把安装路径(我的是D:\Program Files\Tesseract-OCR\tesseract.exe)加到path环境变量
执行 tesseract -v 有输出即可

## 预约
执行reserve.py即可,(在代码中输入自己的学号和密码)

若需要换研讨室,相关研讨室的信息和id参数可以爬http://202.120.82.2:8081/ClientWeb/pro/ajax/device.aspx获取