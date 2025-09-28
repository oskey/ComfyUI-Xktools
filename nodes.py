"""
ComfyUI 中文翻译节点
"""

from .baidu_translator import BaiduTranslator
from .config_manager import config_manager


class ChineseToEnglishTranslator:
    """中文到英文翻译节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        # 获取保存的配置
        api_config = config_manager.get_api_config()
        
        return {
            "required": {
                "chinese_text": ("STRING", {
                    "multiline": True,
                    "default": "请输入中文提示词",
                    "placeholder": "在这里输入中文提示词..."
                }),
                "app_id": ("STRING", {
                    "default": api_config.get('app_id', ''),
                    "placeholder": "请输入百度翻译API的APP ID"
                }),
                "app_key": ("STRING", {
                    "default": api_config.get('app_key', ''),
                    "placeholder": "请输入百度翻译API的密钥"
                }),
            },
            "optional": {
                "auto_translate": ("BOOLEAN", {
                    "default": True,
                    "label_on": "自动翻译",
                    "label_off": "手动翻译"
                }),
                "save_config": ("BOOLEAN", {
                    "default": False,
                    "label_on": "保存配置",
                    "label_off": "不保存"
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("english_text",)
    FUNCTION = "translate_text"
    CATEGORY = "Xktools/翻译"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False,)
    
    def translate_text(self, chinese_text, app_id, app_key, auto_translate=True, save_config=False):
        """
        翻译中文文本为英文
        
        Args:
            chinese_text (str): 中文输入文本
            app_id (str): 百度翻译API的APP ID
            app_key (str): 百度翻译API的密钥
            auto_translate (bool): 是否自动翻译
            save_config (bool): 是否保存配置
            
        Returns:
            tuple: 包含翻译结果的元组
        """
        # 保存配置（如果用户选择保存）
        if save_config and app_id.strip() and app_key.strip():
            config_manager.save_api_config(app_id.strip(), app_key.strip())
        
        # 如果不自动翻译，直接返回原文
        if not auto_translate:
            return (chinese_text,)
        
        # 检查输入参数
        if not chinese_text.strip():
            return ("请输入要翻译的中文文本",)
        
        if not app_id.strip() or not app_key.strip():
            return ("错误：请配置百度翻译API的APP ID和密钥\n\n请访问 https://fanyi-api.baidu.com/ 申请API",)
        
        # 创建翻译器实例
        translator = BaiduTranslator(app_id.strip(), app_key.strip())
        
        # 执行翻译
        try:
            result = translator.translate(chinese_text.strip())
            # 返回翻译结果，确保UI更新
            result_str = str(result)
            return {"ui": {"text": [result_str]}, "result": (result_str,)}
        except Exception as e:
            return (f"翻译过程中发生错误：{str(e)}",)


class BatchChineseToEnglishTranslator:
    """批量中文到英文翻译节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        # 获取保存的配置
        api_config = config_manager.get_api_config()
        
        return {
            "required": {
                "chinese_texts": ("STRING", {
                    "multiline": True,
                    "default": "美丽的风景\n可爱的小猫\n夕阳西下",
                    "placeholder": "每行一个中文提示词..."
                }),
                "app_id": ("STRING", {
                    "default": api_config.get('app_id', ''),
                    "placeholder": "请输入百度翻译API的APP ID"
                }),
                "app_key": ("STRING", {
                    "default": api_config.get('app_key', ''),
                    "placeholder": "请输入百度翻译API的密钥"
                }),
                "separator": ("STRING", {
                    "default": ", ",
                    "placeholder": "多个翻译结果之间的分隔符，如：逗号空格、换行符等"
                })
            },
            "optional": {
                "save_config": ("BOOLEAN", {
                    "default": False,
                    "label_on": "保存配置",
                    "label_off": "不保存"
                })
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("english_prompts",)
    FUNCTION = "batch_translate"
    CATEGORY = "Xktools/翻译"
    OUTPUT_NODE = True
    OUTPUT_IS_LIST = (False,)
    
    def batch_translate(self, chinese_texts, app_id, app_key, separator=", ", save_config=False):
        """
        批量翻译中文文本为英文
        
        Args:
            chinese_texts (str): 多行中文输入文本
            app_id (str): 百度翻译API的APP ID
            app_key (str): 百度翻译API的密钥
            separator (str): 结果分隔符
            save_config (bool): 是否保存配置
            
        Returns:
            tuple: 包含翻译结果的元组
        """
        # 保存配置（如果用户选择保存）
        if save_config and app_id.strip() and app_key.strip():
            config_manager.save_api_config(app_id.strip(), app_key.strip())
        
        # 检查输入参数
        if not chinese_texts.strip():
            return ("请输入要翻译的中文文本",)
        
        if not app_id.strip() or not app_key.strip():
            return ("错误：请配置百度翻译API的APP ID和密钥\n\n请访问 https://fanyi-api.baidu.com/ 申请API",)
        
        # 创建翻译器实例
        translator = BaiduTranslator(app_id.strip(), app_key.strip())
        
        # 分割文本行
        lines = [line.strip() for line in chinese_texts.strip().split('\n') if line.strip()]
        
        if not lines:
            return ("没有找到有效的文本行",)
        
        # 批量翻译
        translated_results = []
        for line in lines:
            try:
                result = translator.translate(line)
                if result.startswith("错误：") or result.startswith("翻译失败："):
                    return (str(result),)  # 如果有错误，直接返回错误信息
                translated_results.append(str(result))
            except Exception as e:
                return (f"翻译 '{line}' 时发生错误：{str(e)}",)
        
        # 合并结果，确保UI更新
        final_result = separator.join(translated_results)
        result_str = str(final_result)
        return {"ui": {"text": [result_str]}, "result": (result_str,)}


# 节点映射
NODE_CLASS_MAPPINGS = {
    "ChineseToEnglishTranslator": ChineseToEnglishTranslator,
    "BatchChineseToEnglishTranslator": BatchChineseToEnglishTranslator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChineseToEnglishTranslator": "中文转英文翻译器",
    "BatchChineseToEnglishTranslator": "批量中文转英文翻译器"
}