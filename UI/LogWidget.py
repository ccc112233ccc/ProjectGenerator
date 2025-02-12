from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPlainTextEdit
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QTextCursor, QColor, QTextCharFormat, QBrush
from datetime import datetime

class LogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建文本显示区域
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)  # 设置为只读
        self.log_text.setLineWrapMode(QPlainTextEdit.WidgetWidth)  # 自动换行
        
        # 设置样式
        
        layout.addWidget(self.log_text)
        self.setLayout(layout)
        
    def add_log(self, message, level="INFO"):
        """
        添加日志信息
        Args:
            message: 日志消息
            level: 日志级别 ("INFO", "WARNING", "ERROR", "SUCCESS")
        """
        # 获取当前时间
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 根据日志级别设置颜色
        color_map = {
            "INFO": "#000000",     # 黑色
            "WARNING": "#FFA500",  # 橙色
            "ERROR": "#FF0000",    # 红色
            "SUCCESS": "#00FF00"   # 绿色
        }
        
        # 创建带颜色的文本格式
        color = color_map.get(level, "#FFFFFF")
        
        # 构建日志文本
        log_text = f"[{current_time}] [{level}] {message}\n"
        
        # 添加日志文本
        self.log_text.appendHtml(f'<span style="color: {color}">{log_text}</span>')
        
        # 滚动到底部
        self.log_text.moveCursor(QTextCursor.End)
    
    def clear_logs(self):
        """清空日志"""
        self.log_text.clear()
    
    def save_logs(self, file_path):
        """
        保存日志到文件
        Args:
            file_path: 保存路径
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.log_text.toPlainText())
            return True
        except Exception as e:
            print(f"Error saving logs: {str(e)}")
            return False

# 使用示例
if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    
    log_widget = LogWidget()
    log_widget.resize(600, 400)
    log_widget.show()
    
    # 添加一些示例日志
    log_widget.add_log("这是一条普通信息")
    log_widget.add_log("这是一条警告信息", "WARNING")
    log_widget.add_log("这是一条错误信息", "ERROR")
    log_widget.add_log("这是一条成功信息", "SUCCESS")
    
    sys.exit(app.exec()) 