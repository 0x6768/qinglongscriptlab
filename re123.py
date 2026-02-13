import requests
import concurrent.futures
import time
import json

def send_request(request_id):
    """发送单个请求的函数"""
    url = "https://t.2x.nz/send"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:147.0) Gecko/20100101 Firefox/147.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8,zh-HK;q=0.7,en-US;q=0.6,en;q=0.5',
        'Content-Type': 'application/json',
        'Origin': 'https://2x.nz',
        'Referer': 'https://2x.nz/'
    }
    
    data = {
        "pathname": "/"
    }
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"请求 {request_id}: 状态码 {response.status_code}, 响应长度 {len(response.text)}")
        return response.status_code, response.text[:100]  # 只返回前100个字符
        
    except Exception as e:
        print(f"请求 {request_id}: 发生错误 - {str(e)}")
        return None, str(e)

def continuous_requests(num_threads=10, interval=1):
    """持续发送请求的主函数
    
    Args:
        num_threads: 线程数量，默认10个
        interval: 请求间隔时间（秒），避免过于频繁
    """
    request_count = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        while True:
            try:
                # 准备要执行的请求
                future_to_request = {
                    executor.submit(send_request, request_count + i): request_count + i 
                    for i in range(num_threads)
                }
                
                # 等待所有请求完成
                for future in concurrent.futures.as_completed(future_to_request):
                    request_id = future_to_request[future]
                    try:
                        status_code, response = future.result()
                        # 这里可以处理响应结果
                    except Exception as e:
                        print(f"请求 {request_id} 处理异常: {e}")
                
                request_count += num_threads
                print(f"已发送 {request_count} 个请求，等待 {interval} 秒...")
                time.sleep(interval)  # 添加延迟避免过于频繁
                
            except KeyboardInterrupt:
                print("\n用户中断，停止请求")
                break
            except Exception as e:
                print(f"主循环错误: {e}")
                time.sleep(5)

if __name__ == "__main__":
    print("开始并发请求测试...")
    print("按 Ctrl+C 停止程序")
    print("-" * 50)
    
    # 重要：请根据实际情况调整参数
    continuous_requests(
        num_threads=10,      # 线程数
        interval=2           # 请求间隔（秒），建议至少1秒以上
    )
