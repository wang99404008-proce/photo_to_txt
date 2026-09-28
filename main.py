# main.py
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, 
                             QTextEdit, QFileDialog, QVBoxLayout, QWidget, QMessageBox)
from ocr_engine import OfflineOCR

class OCRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("離線圖片轉 TXT 工具")
        self.setGeometry(100, 100, 700, 500)
        
        self.ocr = OfflineOCR()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.btn_select = QPushButton("選擇圖片並辨識")
        self.btn_select.clicked.connect(self.select_and_process)
        layout.addWidget(self.btn_select)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.btn_save = QPushButton("匯出為 .txt 檔案")
        self.btn_save.clicked.connect(self.save_to_txt)
        layout.addWidget(self.btn_save)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_and_process(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇圖片", "", "圖片檔案 (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            try:
                text = self.ocr.process_image(file_path)
                self.text_edit.setText(text)
            except Exception as e:
                QMessageBox.critical(self, "錯誤", f"辨識失敗: {str(e)}")

    def save_to_txt(self):
        content = self.text_edit.toPlainText()
        if not content.strip():
            QMessageBox.warning(self, "提示", "沒有可匯出的文字！")
            return

        save_path, _ = QFileDialog.getSaveFileName(self, "儲存 TXT 檔", "output.txt", "文字檔 (*.txt)")
        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(content)
            QMessageBox.information(self, "成功", "檔案已成功儲存！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec())
