"""
百度翻译API调用模块
"""

import hashlib
import random
import time
import requests
import json


class BaiduTranslator:
    """百度翻译API调用类"""
    
    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key
        self.api_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    
    def generate_sign(self, query, salt):
        """生成签名"""
        sign_str = self.app_id + query + str(salt) + self.app_key
        sign = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        return sign
    
    def translate(self, text, from_lang='zh', to_lang='en'):
        """
        翻译文本
        
        Args:
            text (str): 要翻译的文本
            from_lang (str): 源语言，默认为中文(zh)
            to_lang (str): 目标语言，默认为英文(en)
            
        Returns:
            str: 翻译结果，如果失败返回原文本
        """
        if not text.strip():
            return text
            
        if not self.app_id or not self.app_key:
            return f"错误：请配置百度翻译API的APP ID和密钥"
        
        # 生成随机数
        salt = random.randint(32768, 65536)
        
        # 生成签名
        sign = self.generate_sign(text, salt)
        
        # 构建请求参数
        params = {
            'q': text,
            'from': from_lang,
            'to': to_lang,
            'appid': self.app_id,
            'salt': salt,
            'sign': sign
        }
        
        try:
            # 发送请求
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            # 解析响应
            result = response.json()
            
            # 检查是否有错误
            if 'error_code' in result:
                error_messages = {
                    '52001': 'APP ID或密钥错误',
                    '52002': '系统错误',
                    '52003': '用户认证失败',
                    '54000': '必填参数为空',
                    '54001': '签名错误',
                    '54003': '访问频率受限',
                    '54004': '账户余额不足',
                    '54005': '长query请求频繁',
                    '58000': '客户端IP非法',
                    '58001': '译文语言方向不支持',
                    '58002': '服务当前已关闭',
                    '90107': '认证未通过或未生效'
                }
                error_code = result['error_code']
                error_msg = error_messages.get(error_code, f'未知错误: {error_code}')
                return f"翻译失败: {error_msg}"
            
            # 提取翻译结果
            if 'trans_result' in result and result['trans_result']:
                translated_text = result['trans_result'][0]['dst']
                return translated_text
            else:
                return "翻译失败：未获取到翻译结果"
                
        except requests.exceptions.Timeout:
            return "翻译失败：请求超时"
        except requests.exceptions.RequestException as e:
            return f"翻译失败：网络错误 - {str(e)}"
        except json.JSONDecodeError:
            return "翻译失败：响应格式错误"
        except Exception as e:
            return f"翻译失败：{str(e)}"