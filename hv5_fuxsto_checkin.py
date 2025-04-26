import requests
import json
import logging
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

# 从环境变量获取PHPSESSID
phpsessid = os.getenv("FUXSTO_COOKIE")
if not phpsessid:
    logging.error("环境变量 FUXSTO_COOKIE 未设置")
    exit(1)

cookies = {
    'PHPSESSID': phpsessid,
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/jxl,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
}

try:
    # 替换为实际的签到URL
    response = requests.get('https://hv5.fuxsto.cn/Main/CheckIn/', cookies=cookies, headers=headers)
    response.raise_for_status()  # 检查请求是否成功

    json1 = json.loads(response.text)
    if "msg" in json1:
        if json1["msg"] in "失败":
            logging.error("签到失败")
        elif json1["msg"] in "已经签到过啦":
            logging.info("已经签到过啦")
        elif json1["msg"] in "签到成功":
            logging.info("签到成功")
        elif json1["msg"] in "未登录":
            logging.error("未登录")
        else:
            logging.error(f"未知响应: {json1['msg']}")
    else:
        logging.error("响应中没有msg字段")
except requests.RequestException as e:
    logging.error(f"请求失败: {e}")