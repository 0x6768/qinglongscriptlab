import requests
import concurrent.futures
import time
import json
from typing import Optional

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
        start_time = time.time()
        response = requests.post(
            url,
            headers=headers,
            json=data,
            timeout=10
        )
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        print(f"请求 {request_id}: 状态码 {response.status_code}, 耗时 {elapsed_time:.2f}秒, 响应长度 {len(response.text)}")
        return {
            "id": request_id,
            "status_code": response.status_code,
            "response_text": response.text[:100],
            "elapsed_time": elapsed_time
        }
        
    except requests.exceptions.Timeout:
        print(f"请求 {request_id}: 超时 (10秒)")
        return {"id": request_id, "error": "timeout"}
    except Exception as e:
        print(f"请求 {request_id}: 发生错误 - {str(e)[:50]}")
        return {"id": request_id, "error": str(e)}

def continuous_requests(num_threads=10, interval=1, max_requests: Optional[int] = None):
    """持续发送请求的主函数
    
    Args:
        num_threads: 线程数量，默认10个
        interval: 请求间隔时间（秒），避免过于频繁
        max_requests: 最大请求次数，None表示无限循环
    """
    request_count = 0
    success_count = 0
    fail_count = 0
    total_elapsed_time = 0
    
    print("=" * 50)
    if max_requests:
        print(f"计划发送最多 {max_requests} 个请求，使用 {num_threads} 个线程")
    else:
        print(f"将持续发送请求，使用 {num_threads} 个线程（按 Ctrl+C 停止）")
    print(f"请求间隔：{interval} 秒")
    print("=" * 50)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        try:
            while True:
                # 检查是否达到最大请求次数
                if max_requests and request_count >= max_requests:
                    print(f"\n已达到最大请求次数限制：{max_requests}")
                    break
                
                # 计算本轮要发送的请求数
                remaining_requests = max_requests - request_count if max_requests else num_threads
                current_batch_size = min(num_threads, remaining_requests) if max_requests else num_threads
                
                # 如果已经完成所有请求，退出循环
                if max_requests and current_batch_size <= 0:
                    break
                
                # 准备要执行的请求
                future_to_request = {
                    executor.submit(send_request, request_count + i): request_count + i 
                    for i in range(current_batch_size)
                }
                
                # 等待所有请求完成
                batch_results = []
                for future in concurrent.futures.as_completed(future_to_request):
                    request_id = future_to_request[future]
                    try:
                        result = future.result()
                        batch_results.append(result)
                        
                        # 统计结果
                        if "error" in result:
                            fail_count += 1
                        else:
                            success_count += 1
                            if "elapsed_time" in result:
                                total_elapsed_time += result["elapsed_time"]
                        
                    except Exception as e:
                        print(f"请求 {request_id} 处理异常: {e}")
                        fail_count += 1
                
                request_count += current_batch_size
                
                # 显示进度
                if max_requests:
                    progress = (request_count / max_requests) * 100
                    print(f"进度: {request_count}/{max_requests} ({progress:.1f}%) - "
                          f"成功: {success_count}, 失败: {fail_count}")
                else:
                    print(f"已发送 {request_count} 个请求 - 成功: {success_count}, 失败: {fail_count}")
                
                # 如果还有请求要发送，等待间隔时间
                if (max_requests and request_count < max_requests) or not max_requests:
                    print(f"等待 {interval} 秒后继续...")
                    time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n用户中断，停止请求")
    
    # 输出统计信息
    print("\n" + "=" * 50)
    print("测试完成！统计信息：")
    print(f"总请求次数: {request_count}")
    print(f"成功请求: {success_count}")
    print(f"失败请求: {fail_count}")
    if success_count > 0:
        avg_response_time = total_elapsed_time / success_count
        print(f"平均响应时间: {avg_response_time:.2f}秒")
    print(f"总耗时: {total_elapsed_time:.2f}秒")
    print("=" * 50)

if __name__ == "__main__":
    print("并发请求测试程序")
    print("-" * 50)
    
    # 配置参数（根据你的需求修改这些值）
    THREADS = 10           # 并发线程数
    INTERVAL = 0          # 请求间隔（秒）
    MAX_REQUESTS = 100000    # 最大请求次数，设为None表示无限循环
    
    # 重要：请根据实际情况调整参数
    continuous_requests(
        num_threads=THREADS,
        interval=INTERVAL,
        max_requests=MAX_REQUESTS
    )
