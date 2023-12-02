'''
预约研讨室  http://202.120.82.2:8081/ClientWeb/xcus/ic2/Default.aspx
'''
import requests
import time
import pytesseract
from PIL import Image
from retrying import retry
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)-s %(levelname)-s: %(message)s')

# 配置tesseract运行环境
# 需要安装tesseract，教程：https://blog.csdn.net/qq_31362767/article/details/107891185
pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'


def retry_on_result_fuc(result):
    return result[0] == False


class ReservePlatform(object):
    _session = requests.session()
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    _session.headers.update(headers)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()

    def clear_image(self, image, threshold):    # 图像降噪并进行灰度处理提高识别率
        image = image.convert('RGB')
        width = image.size[0]
        height = image.size[1]
        noise_color = self.get_noise_color(image)
        for x in range(width):
            for y in range(height):
                # 清除边框和干扰色
                if (x == 0 or y == 0 or x == width - 1 or y == height - 1
                        or image.getpixel((x, y)) == noise_color):
                    image.putpixel((x, y), (255, 255, 255))
        # 变为灰色，模式L为灰色模式，它的每个相似用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度
        image = image.convert('L')  # 灰色模式
        # image.show()
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        image = image.point(table, "1")
        image.save("verification_code_gray.jpg")
        return image

    def get_noise_color(self,image):
        for y in range(1, image.size[1] - 1):
            # 获取第2列非白的颜色
            (r, g, b) = image.getpixel((2, y))
            if r < 255 and g < 255 and b < 255:
                return (r, g, b)

    @retry(retry_on_result=retry_on_result_fuc,stop_max_attempt_number=5)
    def get_ocr(self):
        '''
        请求验证码图片，并进行验证码识别，当识别错误（识别出的数字长度不是4）时重试，最大重试次数5次
        :return:
        '''
        # 先请求图片资源
        codeUrl = f"https://portal1.ecnu.edu.cn/cas/code?{random.random()}"
        res1 = self._session.get(codeUrl)
        return
        res1.encoding = 'utf-8'
        with open("verification_code.jpg", 'wb') as file:  # 以byte形式将图片数据写入
            file.write(res1.content)
            file.flush()
        raw_image = Image.open("verification_code.jpg")
        image1 = self.clear_image(raw_image, 127)
        ocr = pytesseract.image_to_string(image1)
        logging.info(ocr)
        # 提取ocr中的数字
        number = "".join(list(filter(str.isdigit, ocr)))
        if len(number) == 4:
            logging.info(number)
            return True,number
        else:
            return False,number

    @retry(stop_max_attempt_number=5)
    def login(self,id,pwd):     # 当异常时重试，最大重试次数5次
        # res1 = self._session.get("http://202.120.82.2:8081/ClientWeb/xcus/ic2/Default.aspx")
        ocr = self.get_ocr()[1]
        # 开始验证登录
        r = self._session.post(
            url="http://202.120.82.2:8081/ClientWeb/pro/ajax/login.aspx",
            data={
                "id": id,
                "pwd": pwd,
                "number": int(ocr),
                "act": "dlogin"
            }
        )
        r_json = r.json()
        if (r_json.get('msg', None) == 'ok'):
            logging.info('登录成功')
            return True
        else:
            logging.error('登录失败,请检查账号、密码是否正确！')
            raise Exception("登录失败,请检查账号、密码是否正确！")

    def main(self):
        try:
            # 登录
            self.login("51215903102", "abc19990209.")
            #这里就可以写预约与取消操作了
            # 参数
            params = {
                'dev_id': '3676491',
                'lab_id': '3674920',
                'kind_id': '3675179',
                'type': 'dev',
                'min_user': 5,
                'max_user': 10,
                'mb_list': '20150073,51215903102,51201300094,51215903080,51215903087',
                'start': '2021-12-10 13:30',
                'end': '2021-12-10 16:30',
                'start_time': '1330',
                'end_time': '1630',
                'act': 'set_resv',
                '_': str(round(time.time()*1000))   # 当前时间戳
            }
            while True:
                re = self._session.get('http://202.120.82.2:8081/ClientWeb/pro/ajax/reserve.aspx', params=params)
                if re.json()['msg'] == "操作成功！":
                    print("预约成功！")
                    break
                else:
                    print(re.json()['msg'])
        except:
            logging.error("登录失败=-=")
            return False


if __name__ == '__main__':
    ReservePlatform().main()
