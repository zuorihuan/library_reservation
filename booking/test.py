"""
    作者: ZRH
    日期: 2023年10月11日  15:48
"""
import requests
import json
import  random
import datetime
redirectLoginUrl = "https://portal1.ecnu.edu.cn/cas/login?service=https://api.ecnu.edu.cn/user/authorize"
codeUrl  = f"https://portal1.ecnu.edu.cn/cas/code?{random.random()}"
reserveUrl = 'https://studyroom.ecnu.edu.cn/ic-web/reserve'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Host': 'studyroom.ecnu.edu.cn',
    'Origin': 'https://studyroom.ecnu.edu.cn',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'lan': '1',
    'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
    'token': '7e4cb7855bf54f66b1359d3e156e138a'
}

cookies = {
    'Hm_lvt_f76f8c7e3ddd48018c54d9d37f42086a': '1678972916',
    'epjwrb9eGVNZO': '606EWXS7ryHjCsSGlL6M5dbT7jg9GrtNxX8awE6z0AmMppxDAOLEGB0YxoVLsRGRlb1r2_RGFdjHt_pqNAPMcjTa',
    'BIGipServerpool_172.20.5.195_80': '3271890092.20480.0000',
    'ic-cookie': '476a693d-405b-4a7a-907c-bc151d3a5956'
}

# 设置POST请求的参数
data = {
    "sysKind": 1,
    "appAccNo": 9919511,
    "memberKind": 1,
    "resvBeginTime": "2023-11-03 18:45:00",
    "resvEndTime": "2023-11-03 21:40:00",
    "testName": "test",
    "resvKind": 2,
    "resvProperty": 0,
    "appUrl": "",
    "resvMember": [9919511],
    "resvDev": [3676547],
    "memo": "tset",
    "captcha": "",
    "addServices": []
}



# 发送POST请求
while True:
    try:
        response = requests.post(reserveUrl, json=data, headers=headers, cookies=cookies, verify=False)
        print(response.text)
        json_resp = json.loads(response.text)
        code = json_resp.get("code")
        # 检查响应
        if code == 0:
            print('预约成功!')
            print('预约成功!')
            print('预约成功!')
            break
        else:
            print(f'预约失败: {json_resp.get("message")}')
    except Exception as e:
        print(f"请求出错：{e}")

