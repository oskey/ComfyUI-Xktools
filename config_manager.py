"""
配置文件管理模块
用于保存和加载百度翻译API配置
"""

import os
import json
from pathlib import Path


class ConfigManager:
    """配置管理器"""
    
    def __init__(self):
        # 获取插件目录
        self.plugin_dir = Path(__file__).parent
        self.config_file = self.plugin_dir / "config.json"
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置文件"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"[Xktools] 加载配置文件失败: {e}")
                return {}
        return {}
    
    def save_config(self, config):
        """保存配置文件"""
        try:
            # 确保目录存在
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            self.config = config
            print(f"[Xktools] 配置已保存到: {self.config_file}")
            return True
        except IOError as e:
            print(f"[Xktools] 保存配置文件失败: {e}")
            return False
    
    def get_api_config(self):
        """获取API配置"""
        return {
            'app_id': self.config.get('app_id', ''),
            'app_key': self.config.get('app_key', '')
        }
    
    def save_api_config(self, app_id, app_key):
        """保存API配置"""
        new_config = self.config.copy()
        new_config['app_id'] = app_id
        new_config['app_key'] = app_key
        return self.save_config(new_config)
    
    def has_valid_config(self):
        """检查是否有有效的配置"""
        api_config = self.get_api_config()
        return bool(api_config['app_id'].strip() and api_config['app_key'].strip())


# 全局配置管理器实例
config_manager = ConfigManager()