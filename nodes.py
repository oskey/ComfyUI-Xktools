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
                    "default": "一个美丽的女孩，长发飘逸，微笑着看向镜头",
                    "placeholder": "请输入中文提示词..."
                }),
                "app_id": ("STRING", {
                    "default": api_config.get('app_id', ''),
                    "placeholder": "请输入百度翻译API的APP ID"
                }),
                "app_key": ("STRING", {
                    "default": api_config.get('app_key', ''),
                    "placeholder": "请输入百度翻译API的密钥"
                }),
                "auto_translate": ("BOOLEAN", {
                    "default": True,
                    "label_on": "自动翻译",
                    "label_off": "手动翻译"
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
    RETURN_NAMES = ("english_text",)
    FUNCTION = "translate_text"
    CATEGORY = "Xktools/翻译"
    
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
        
        # 检查输入参数
        if not chinese_text.strip():
            return ("请输入要翻译的中文文本",)
        
        if not auto_translate:
            return (chinese_text,)  # 如果不自动翻译，直接返回原文
        
        if not app_id.strip() or not app_key.strip():
            return ("错误：请配置百度翻译API的APP ID和密钥\n\n请访问 https://fanyi-api.baidu.com/ 申请API",)
        
        # 创建翻译器实例并翻译
        translator = BaiduTranslator(app_id.strip(), app_key.strip())
        
        try:
            result = translator.translate(chinese_text.strip())
            # 返回翻译结果，确保CLIP兼容性
            result_str = str(result)
            return (result_str,)
        except Exception as e:
            return (f"翻译过程中发生错误：{str(e)}",)


class ChineseClipTextEncode:
    """集成中文翻译功能的CLIP文本编码器"""
    
    @classmethod
    def INPUT_TYPES(cls):
        # 获取保存的配置
        api_config = config_manager.get_api_config()
        
        return {
            "required": {
                "clip": ("CLIP",),
                "chinese_text": ("STRING", {
                    "multiline": True,
                    "default": "一个美丽的女孩，长发飘逸，微笑着看向镜头",
                    "placeholder": "请输入中文提示词..."
                }),
                "app_id": ("STRING", {
                    "default": api_config.get('app_id', ''),
                    "placeholder": "请输入百度翻译API的APP ID"
                }),
                "app_key": ("STRING", {
                    "default": api_config.get('app_key', ''),
                    "placeholder": "请输入百度翻译API的密钥"
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
    
    RETURN_TYPES = ("CONDITIONING", "STRING")
    RETURN_NAMES = ("conditioning", "english_preview")
    FUNCTION = "encode_with_translation"
    CATEGORY = "Xktools/翻译"
    OUTPUT_NODE = True
    
    def encode_with_translation(self, clip, chinese_text, app_id, app_key, save_config=False):
        """
        翻译中文并进行CLIP编码
        
        Args:
            clip: CLIP模型
            chinese_text (str): 中文输入文本
            app_id (str): 百度翻译API的APP ID
            app_key (str): 百度翻译API的密钥
            save_config (bool): 是否保存配置
            
        Returns:
            tuple: 包含CLIP条件和英文预览的元组
        """
        # 保存配置（如果用户选择保存）
        if save_config and app_id.strip() and app_key.strip():
            config_manager.save_api_config(app_id.strip(), app_key.strip())
        
        # 检查输入参数
        if not chinese_text.strip():
            error_msg = "请输入要翻译的中文文本"
            # 返回空的conditioning和错误信息
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return ([[cond, {"pooled_output": pooled}]], error_msg)
        
        if not app_id.strip() or not app_key.strip():
            error_msg = "错误：请配置百度翻译API的APP ID和密钥\n\n请访问 https://fanyi-api.baidu.com/ 申请API"
            # 返回空的conditioning和错误信息
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return ([[cond, {"pooled_output": pooled}]], error_msg)
        
        # 创建翻译器实例并翻译
        translator = BaiduTranslator(app_id.strip(), app_key.strip())
        
        try:
            english_text = translator.translate(chinese_text.strip())
            
            # 如果翻译失败，使用原文
            if english_text.startswith("错误：") or english_text.startswith("翻译失败："):
                english_text = chinese_text.strip()
            
            # 使用翻译后的英文进行CLIP编码
            tokens = clip.tokenize(english_text)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            
            # 返回conditioning和英文预览
            return ([[cond, {"pooled_output": pooled}]], str(english_text))
            
        except Exception as e:
            error_msg = f"翻译过程中发生错误：{str(e)}"
            # 返回使用原文的conditioning和错误信息
            tokens = clip.tokenize(chinese_text.strip())
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return ([[cond, {"pooled_output": pooled}]], error_msg)


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
        
        # 合并结果，确保CLIP兼容性
        final_result = separator.join(translated_results)
        result_str = str(final_result)
        return (result_str,)


# 节点映射
NODE_CLASS_MAPPINGS = {
    "ChineseToEnglishTranslator": ChineseToEnglishTranslator,
    "ChineseClipTextEncode": ChineseClipTextEncode,
    "BatchChineseToEnglishTranslator": BatchChineseToEnglishTranslator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChineseToEnglishTranslator": "中文转英文翻译器",
    "ChineseClipTextEncode": "中文CLIP文本编码器",
    "BatchChineseToEnglishTranslator": "批量中文转英文翻译器"
}