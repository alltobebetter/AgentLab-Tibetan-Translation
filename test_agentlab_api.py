#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json

API_URL = "https://t2c.agentlab.click/api/translate"

def test_translation(text, direction, desc):
    print(f"\n{'='*60}")
    print(f"测试: {desc}")
    print(f"{'='*60}")
    print(f"输入: {text}")
    print(f"方向: {direction}")
    
    try:
        response = requests.post(
            API_URL,
            json={"text": text, "direction": direction},
            timeout=30
        )
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"成功: {data['success']}")
            print(f"原文: {data['source']}")
            print(f"译文: {data['translation']}")
            print(f"方向: {data['directionName']}")
        else:
            print(f"错误: {response.text}")
            
    except Exception as e:
        print(f"异常: {e}")

if __name__ == "__main__":
    print("AgentLab Tibetan Translation API 测试")
    
    test_translation(
        "བཀྲ་ཤིས་བདེ་ལེགས།",
        "tc",
        "藏文→中文"
    )
    
    test_translation(
        "你好",
        "ct",
        "中文→藏文"
    )
    
    test_translation(
        "西藏大学信息科学技术学院",
        "ct",
        "中文→藏文（长文本）"
    )
    
    test_translation(
        "བོད་ལྗོངས་སློབ་གྲྭ་ཆེན་མོ།",
        "tc",
        "藏文→中文（长文本）"
    )
    
    print(f"\n{'='*60}")
    print("测试完成！")
    print(f"{'='*60}")
