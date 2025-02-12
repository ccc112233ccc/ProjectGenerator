from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QLineEdit, QPushButton, QFileDialog)

class ExecutableSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置可执行文件")
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # 创建可执行程序路径输入区域
        exe_layout = QHBoxLayout()
        exe_label = QLabel("可执行程序路径:")
        self.executable_input = QLineEdit()
        self.executable_input.setPlaceholderText("输入可执行程序的路径")
        exe_browse = QPushButton("...")
        exe_browse.setMaximumWidth(30)
        exe_browse.clicked.connect(self.browse_executable)
        exe_layout.addWidget(exe_label)
        exe_layout.addWidget(self.executable_input)
        exe_layout.addWidget(exe_browse)
        layout.addLayout(exe_layout)
        
        # 创建工作目录输入区域
        work_dir_layout = QHBoxLayout()
        work_dir_label = QLabel("运行目录:")
        self.work_dir_input = QLineEdit()
        self.work_dir_input.setPlaceholderText("输入运行目录的路径")
        work_dir_browse = QPushButton("...")
        work_dir_browse.setMaximumWidth(30)
        work_dir_browse.clicked.connect(self.browse_work_dir)
        work_dir_layout.addWidget(work_dir_label)
        work_dir_layout.addWidget(self.work_dir_input)
        work_dir_layout.addWidget(work_dir_browse)
        layout.addLayout(work_dir_layout)
        
        # 创建参数输入框
        self.arguments_input = QLineEdit()
        self.arguments_input.setPlaceholderText("输入程序参数（可选）")
        layout.addWidget(QLabel("程序参数:"))
        layout.addWidget(self.arguments_input)
        
        # 添加确定和取消按钮
        button_layout = QHBoxLayout()
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

    def browse_executable(self):
        """浏览选择可执行文件"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择可执行文件",
            "",
            "可执行文件 (*.exe);;所有文件 (*.*)"
        )
        if file_name:
            self.executable_input.setText(file_name)

    def browse_work_dir(self):
        """浏览选择工作目录"""
        dir_name = QFileDialog.getExistingDirectory(
            self,
            "选择运行目录",
            ""
        )
        if dir_name:
            self.work_dir_input.setText(dir_name)
