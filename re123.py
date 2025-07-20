import requests
import random
import string
import time

# ============ 配置项 ============
REGISTER_URL = "https://dev.voce.chat/api/user/register"
REGISTER_COUNT = 100000               # 注册用户数量
DELAY_SECONDS = 0              # 注册间隔（秒）
COMMON_EMAIL_DOMAINS = [
    "gmail.com", "yahoo.com", "outlook.com", "qq.com", "163.com", "hotmail.com"
]
DEVICE = "browser"

# ============ 工具函数 ============

def random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_email():
    local_part = random_string(random.randint(6, 12))
    domain = random.choice(COMMON_EMAIL_DOMAINS)
    return f"{local_part}@{domain}"

def generate_password():
    return random_string(random.randint(8, 16))

def generate_user_payload():
    return {
        "name": random_string(random.randint(6, 12)),
        "email": generate_email(),
        "password": generate_password(),
        "gender": random.randint(0, 1),
        "device": DEVICE
    }

# ============ 主注册函数 ============

def register_user(index: int):
    payload = generate_user_payload()
    try:
        response = requests.post(REGISTER_URL, json=payload, timeout=5)
        if response.status_code == 200:
            print(f"[{index:03}] 注册成功: {payload['email']}")
        else:
            print(f"[{index:03}] 注册失败: 状态码={response.status_code}, 响应={response.text}")
    except Exception as e:
        print(f"[{index:03}] 请求异常: {e}")

def main():
    for i in range(1, REGISTER_COUNT + 1):
        register_user(i)
        time.sleep(DELAY_SECONDS)

if __name__ == "__main__":
    main()
