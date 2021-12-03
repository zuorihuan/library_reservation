from selenium import webdriver
from PIL import Image,ImageEnhance
import pytesseract
import time
import os

def infolist_spider(usernm, passwd, imgPath):    
    options = webdriver.ChromeOptions()
   #打开注释即后台模式
   #options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1200, 800)
    driver.implicitly_wait(5)


    url = "http://portal.ecnu.edu.cn/eapdomain/static/component/cms/cmp_cms_pim_show/showMoreInfoList.jsp?configId=5134"
    try:
        driver.get(url)

        assert "华东师范大学" in driver.title

        username =  driver.find_element_by_id("un")
        password = driver.find_element_by_id("pd")
        captcha = driver.find_element_by_id("code")

        username.send_keys(usernm)
        password.send_keys(passwd)

        codeImage = driver.find_element_by_id("codeImage")
        location = codeImage.location
        size = codeImage.size

        left = location['x']
        top =  location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        driver.get_screenshot_as_file(screenImg)
        img = Image.open(screenImg).crop((left,top,right,bottom))
        img = img.convert('L') 			#转换模式：L | RGB
        img = ImageEnhance.Contrast(img)#增强对比度
        img = img.enhance(2.0) 			#增加饱和度
        img.save(screenImg)

        code = pytesseract.image_to_string(img, lang='eng', config='--psm 6 --oem 3 -c '
                                                                        'tessedit_char_whitelist'
                                                                        '=0123456789')
        codeStr = ""

        for i in code:
            if i in "0123456789":
                codeStr = codeStr + i
                if len(codeStr)==4:
                    break

        captcha.send_keys(codeStr)

        driver.find_element_by_id("index_login_btn").click()


        infodiv = driver.find_element_by_id("ext-gen5")
        #print(infodiv.text)
        tbody_1 = infodiv.find_element_by_tag_name("tbody")

        tbodys = tbody_1.find_elements_by_tag_name("tbody")

        #第一个 table 里的 tdbody 是空行，从第二个开始是是通知列表
        trs = tbodys[3].find_elements_by_tag_name("tr")

        infolist = []
        index = 1
        for tr in trs:
            tds = tr.find_elements_by_tag_name("td")
            # 第一个 td 是箭头图标，无视
            a = tds[1].find_element_by_tag_name("a")
            title = tds[1].text
            date = tds[2].text

            info = {
                "index" : index,
                "href"  : a.get_attribute('href'),
                "title" : title,
                "date"  : date
            }
            index = index + 1
            infolist.append(info)

        res = {
            "update_time" : int(time.time()),
            "infolist" : infolist,
            "more":url 
        }
    except Exception as e:
        print(e)
        return None

    driver.quit()
    return res

if __name__ == '__main__':
    t_user = "username"
    t_pass = "password"
    pwd = os.getcwd()
    screenImg = pwd + "/ocr.png"

    print(infolist_spider(t_user,t_pass,screenImg))