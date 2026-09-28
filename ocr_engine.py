# ocr_engine.py
import os
from paddleocr import PaddleOCR

class OfflineOCR:
    def __init__(self):
        # 載入內建繁體中文與方向檢測模型 (離線模式)
        self.ocr = PaddleOCR(
            use_angle_cls=True, 
            lang='chinese_cht',
            show_log=False
        )

    def process_image(self, img_path):
        if not os.path.exists(img_path):
            raise FileNotFoundError("找不到指定的圖片檔案")
        
        # 執行辨識
        result = self.ocr.ocr(img_path, cls=True)
        extracted_text = []

        if result and result[0]:
            for line in result[0]:
                text = line[1][0]  # 取得辨識出的文字
                extracted_text.append(text)

        return "\n".join(extracted_text)
