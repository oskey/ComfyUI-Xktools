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
                })
            }
        }
    
    RETURN_TYPES = ("CONDITIONING", "STRING")
    RETURN_NAMES = ("条件", "翻译结果")
    FUNCTION = "encode_with_translation"
    CATEGORY = "Xktools/翻译"
    
    def encode_with_translation(self, clip, chinese_text, auto_translate, app_id, app_key, save_config=False, translation_result=None):
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
            tuple: 包含CLIP条件和翻译结果文本的元组
        """
        # 添加调试打印
        print(f"[XKT翻译] 开始处理: {chinese_text[:50]}...")
        print(f"[XKT翻译] 自动翻译: {auto_translate}")
        
        # 保存配置（如果用户选择保存）
        if save_config and app_id.strip() and app_key.strip():
            config_manager.save_api_config(app_id.strip(), app_key.strip())
            print(f"[XKT翻译] 已保存API配置")
        
        # 检查输入参数
        if not chinese_text.strip():
            error_msg = "请输入要翻译的中文文本"
            print(f"[XKT翻译] 错误: {error_msg}")
            # 返回空的conditioning和错误信息
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return {
                "ui": {"text": [error_msg]},
                "result": ([[cond, {"pooled_output": pooled}]], error_msg)
            }
        
        # 如果不自动翻译，直接使用原文进行编码
        if not auto_translate:
            tokens = clip.tokenize(chinese_text.strip())
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            result_text = chinese_text.strip()  # Show Text直接显示原文
            print(f"[XKT翻译] 使用原文: {chinese_text.strip()}")
            return {
                "ui": {"text": [result_text]},
                "result": ([[cond, {"pooled_output": pooled}]], result_text)
            }
        
        if not app_id.strip() or not app_key.strip():
            error_msg = "错误：请配置百度翻译API的APP ID和密钥\n\n请访问 https://fanyi-api.baidu.com/ 申请API"
            print(f"[XKT翻译] {error_msg}")
            # 返回空的conditioning和错误信息
            tokens = clip.tokenize("")
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return {
                "ui": {"text": [error_msg]},
                "result": ([[cond, {"pooled_output": pooled}]], error_msg)
            }
        
        # 创建翻译器实例并翻译
        translator = BaiduTranslator(app_id.strip(), app_key.strip())
        print(f"[XKT翻译] 开始调用百度翻译API...")
        
        try:
            english_text = translator.translate(chinese_text.strip())
            print(f"[XKT翻译] API返回结果: {english_text}")
            
            # 如果翻译失败，使用原文
            if english_text.startswith("错误：") or english_text.startswith("翻译失败："):
                english_text = chinese_text.strip()
                ui_text = english_text  # Show Text直接显示原文
                print(f"[XKT翻译] 翻译失败，使用原文: {english_text}")
            else:
                ui_text = english_text  # Show Text直接显示翻译结果
                print(f"[XKT翻译] 翻译成功: {chinese_text.strip()} -> {english_text}")
            
            # 使用翻译后的英文进行CLIP编码
            tokens = clip.tokenize(english_text)
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            
            # 返回conditioning和UI显示
            return {
                "ui": {"text": [ui_text]},
                "result": ([[cond, {"pooled_output": pooled}]], ui_text)
            }
            
        except Exception as e:
            error_msg = f"翻译过程中发生错误：{str(e)}"
            print(f"[XKT翻译] 异常: {error_msg}")
            # 返回使用原文的conditioning和错误信息
            tokens = clip.tokenize(chinese_text.strip())
            cond, pooled = clip.encode_from_tokens(tokens, return_pooled=True)
            return {
                "ui": {"text": [error_msg]},
                "result": ([[cond, {"pooled_output": pooled}]], error_msg)
            }


# 节点映射
NODE_CLASS_MAPPINGS = {
    "ChineseClipTextEncode": ChineseClipTextEncode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChineseClipTextEncode": "XKT 自动翻译英文CLIP文本编码器"
}