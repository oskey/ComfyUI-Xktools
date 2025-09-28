"""
ComfyUI 中文翻译节点
"""

from .baidu_translator import BaiduTranslator
from .config_manager import config_manager


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
                "auto_translate": ("BOOLEAN", {
                    "default": True,
                    "label_on": "自动翻译",
                    "label_off": "不翻译"
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
                }),
                "translation_result": ("STRING", {
                    "default": "翻译结果将在这里显示...",
                    "multiline": True,
                    "readonly": True,
                    "placeholder": "翻译结果将在这里显示..."
                })
            }
        }
    
    RETURN_TYPES = ("CONDITIONING",)
    RETURN_NAMES = ("条件",)
    FUNCTION = "encode_with_translation"
    CATEGORY = "Xktools/翻译"
    
    def encode_with_translation(self, clip, chinese_text, auto_translate, app_id, app_key, save_config=False, translation_result="翻译结果将在这里显示..."):
        """
        翻译中文并进行CLIP编码
        
        Args:
            clip: CLIP模型
            chinese_text (str): 中文输入文本
            auto_translate (bool): 是否自动翻译
            app_id (str): 百度翻译API的APP ID
            app_key (str): 百度翻译API的密钥
            save_config (bool): 是否保存配置
            
        Returns:
            dict: 包含UI显示和CLIP条件的字典
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
            return {
                "ui": {"translation_result": [error_msg]},
                "result": ([[cond, {"pooled_output": pooled}]],)
            }
        
        # 如果不自动翻译，直接使用原文进行编码
        if not auto_translate:
            tokens = clip.tokenize(chinese_text.strip())
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            result_text = f"使用原文: {chinese_text.strip()}"
            return {
                "ui": {"translation_result": [result_text]},
                "result": ([[cond, {"pooled_output": pooled}]],)
            }
        
        if not app_id.strip() or not app_key.strip():
            error_msg = "错误：请配置百度翻译API的APP ID和密钥\n\n请访问 https://fanyi-api.baidu.com/ 申请API"
            # 返回空的conditioning和错误信息
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return {
                "ui": {"translation_result": [error_msg]},
                "result": ([[cond, {"pooled_output": pooled}]],)
            }
        
        # 创建翻译器实例并翻译
        translator = BaiduTranslator(app_id.strip(), app_key.strip())
        
        try:
            english_text = translator.translate(chinese_text.strip())
            
            # 如果翻译失败，使用原文
            if english_text.startswith("错误：") or english_text.startswith("翻译失败："):
                english_text = chinese_text.strip()
                ui_text = f"翻译失败，使用原文: {english_text}"
            else:
                ui_text = f"翻译结果: {english_text}"
            
            # 使用翻译后的英文进行CLIP编码
            tokens = clip.tokenize(english_text)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            
            # 返回conditioning和UI显示
            return {
                "ui": {"translation_result": [ui_text]},
                "result": ([[cond, {"pooled_output": pooled}]],)
            }
            
        except Exception as e:
            error_msg = f"翻译过程中发生错误：{str(e)}"
            # 返回使用原文的conditioning和错误信息
            tokens = clip.tokenize(chinese_text.strip())
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return {
                "ui": {"translation_result": [error_msg]},
                "result": ([[cond, {"pooled_output": pooled}]],)
            }


# 节点映射
NODE_CLASS_MAPPINGS = {
    "ChineseClipTextEncode": ChineseClipTextEncode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChineseClipTextEncode": "XKT 自动翻译英文CLIP文本编码器"
}