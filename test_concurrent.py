#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

API_URL = "https://t2c.agentlab.click/api/translate"

results_lock = Lock()
success_count = 0
fail_count = 0
total_time = 0

test_data = [
    {"text": "བཀྲ་ཤིས་བདེ་ལེགས།", "direction": "tc", "name": "藏→中1"},
    {"text": "你好", "direction": "ct", "name": "中→藏1"},
    {"text": "བོད་ལྗོངས་སློབ་གྲྭ་ཆེན་མོ།", "direction": "tc", "name": "藏→中2"},
    {"text": "西藏大学", "direction": "ct", "name": "中→藏2"},
    {"text": "ཐུགས་རྗེ་ཆེ།", "direction": "tc", "name": "藏→中3"},
    {"text": "谢谢", "direction": "ct", "name": "中→藏3"},
    {"text": "བོད་ཀྱི་སྐད་ཡིག", "direction": "tc", "name": "藏→中4"},
    {"text": "藏语", "direction": "ct", "name": "中→藏4"},
    {"text": "སྐུ་ཁམས་བཟང་།", "direction": "tc", "name": "藏→中5"},
    {"text": "身体好", "direction": "ct", "name": "中→藏5"},
]

def call_api(data, index):
    global success_count, fail_count, total_time
    
    start_time = time.time()
    try:
        response = requests.post(
            API_URL,
            json={"text": data["text"], "direction": data["direction"]},
            timeout=30
        )
        elapsed = time.time() - start_time
        
        with results_lock:
            if response.status_code == 200:
                result = response.json()
                success_count += 1
                total_time += elapsed
                print(f"✓ [{index:2d}] {data['name']:8s} | {elapsed:.2f}s | {data['text'][:20]} → {result['translation'][:20]}")
            else:
                fail_count += 1
                print(f"✗ [{index:2d}] {data['name']:8s} | {elapsed:.2f}s | HTTP {response.status_code}")
        
        return True
        
    except Exception as e:
        elapsed = time.time() - start_time
        with results_lock:
            fail_count += 1
        print(f"✗ [{index:2d}] {data['name']:8s} | {elapsed:.2f}s | 异常: {str(e)[:30]}")
        return False

def test_concurrent(num_threads, num_requests):
    global success_count, fail_count, total_time
    success_count = 0
    fail_count = 0
    total_time = 0
    
    print(f"\n{'='*70}")
    print(f"并发测试: {num_threads} 线程 × {num_requests} 请求 = {num_threads * num_requests} 总请求")
    print(f"{'='*70}\n")
    
    tasks = []
    total_requests = num_threads * num_requests
    for i in range(total_requests):
        data = test_data[i % len(test_data)]
        tasks.append((data, i + 1))
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(call_api, data, idx) for data, idx in tasks]
        for future in as_completed(futures):
            future.result()
    
    total_elapsed = time.time() - start_time
    
    print(f"\n{'='*70}")
    print(f"测试完成")
    print(f"{'='*70}")
    print(f"总请求数: {success_count + fail_count}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"成功率: {success_count/(success_count+fail_count)*100:.1f}%")
    print(f"总耗时: {total_elapsed:.2f}s")
    print(f"平均响应时间: {total_time/success_count:.2f}s" if success_count > 0 else "N/A")
    print(f"QPS: {(success_count+fail_count)/total_elapsed:.2f} 请求/秒")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    print("AgentLab Tibetan Translation API 并发测试\n")
    
    test_concurrent(num_threads=50, num_requests=1)
