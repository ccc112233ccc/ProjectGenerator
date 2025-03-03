from PySide6.QtWidgets import (QMainWindow, QApplication, QDockWidget,
                               QMenu, QMenuBar, QDialog, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QLabel, QPushButton, QFileDialog)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QProcess, QDir
import sys
import json
import os

# 假设 TreeEditor, StructureViewer, LogWidget 已经定义
# 这里简单定义它们的占位符类
from UI.TreeEditor import EditableTreeWidget
from UI.StructureViewer import StructureViewer
from UI.LogWidget import LogWidget
from UI.ExecutableSettingsDialog import ExecutableSettingsDialog
from UI.DataFramePlotterQt import DataFramePlotterQt
from UI.table_widget import TableWidget


class MainWindow(QMainWindow):
    def __init__(self, global_config_path='globalconfig.json'):
        super().__init__()
        # 从 globalconfig.json 加载配置
        self.global_config = json.load(
            open(global_config_path, 'r', encoding='utf-8'))

        # 设置默认的求解器配置
        solver_config = self.global_config.get('solver', {})
        self.executable_path = solver_config.get('solver_path', '')
        self.work_dir = solver_config.get('pwd_dir', '')
        self.executable_args = solver_config.get('solver_args', '').split()
        self.name = self.global_config.get('name', '')

        # 初始化进程
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_stdout)
        self.process.readyReadStandardError.connect(self.handle_stderr)
        self.process.finished.connect(self.process_finished)

        # 加载结构图片
        self.structure_paths = self.global_config.get(
            'structure', {}).get('structure_path', [])

        self.init_ui()
        # 保存初始布局状态
        self.default_state = self.saveState()

    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle(self.name)
        self.resize(1200, 800)

        # 创建菜单栏
        self.create_menu()

        # 创建并添加 TreeEditor DockWidget
        self.tree_editor = EditableTreeWidget(
            self.global_config['config']['file_path'])
        self.tree_dock = QDockWidget("Tree Editor", self)
        self.tree_dock.setFeatures(QDockWidget.DockWidgetClosable)  # 只允许关闭
        self.tree_dock.setWidget(self.tree_editor)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.tree_dock)

        # 创建并添加 StructureViewer DockWidget
        self.structure_viewer = StructureViewer()
        self.structure_dock = QDockWidget("Structure Viewer", self)
        self.structure_dock.setFeatures(
            QDockWidget.DockWidgetClosable)  # 只允许关闭
        self.structure_dock.setWidget(self.structure_viewer)
        self.addDockWidget(Qt.RightDockWidgetArea, self.structure_dock)

        # 加载默认的结构图片
        self.structure_viewer.add_structures(self.structure_paths)

        # 创建并添加 LogWidget DockWidget
        self.log_widget = LogWidget()
        self.log_dock = QDockWidget("Log", self)
        self.log_dock.setFeatures(QDockWidget.DockWidgetClosable)  # 只允许关闭
        self.log_dock.setWidget(self.log_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.log_dock)

        # 连接可见性改变信号到槽函数
        self.tree_dock.visibilityChanged.connect(self.update_tree_action)
        self.structure_dock.visibilityChanged.connect(
            self.update_structure_action)
        self.log_dock.visibilityChanged.connect(self.update_log_action)

    def create_menu(self):
        menubar = self.menuBar()

        # 视图菜单
        view_menu = menubar.addMenu('视图')

        # TreeEditor 显示/隐藏
        self.toggle_tree_action = QAction(
            '显示/隐藏 Tree Editor', self, checkable=True)
        self.toggle_tree_action.setChecked(True)
        self.toggle_tree_action.triggered.connect(self.toggle_tree_dock)

        # StructureViewer 显示/隐藏
        self.toggle_structure_action = QAction(
            '显示/隐藏 Structure Viewer', self, checkable=True)
        self.toggle_structure_action.setChecked(True)
        self.toggle_structure_action.triggered.connect(
            self.toggle_structure_dock)

        # LogWidget 显示/隐藏
        self.toggle_log_action = QAction('显示/隐藏 Log', self, checkable=True)
        self.toggle_log_action.setChecked(True)
        self.toggle_log_action.triggered.connect(self.toggle_log_dock)

        # 添加复原布局动作
        restore_layout_action = QAction('复原布局', self)
        restore_layout_action.setShortcut('Ctrl+R')  # 添加快捷键
        restore_layout_action.triggered.connect(self.restore_default_layout)

        view_menu.addAction(self.toggle_tree_action)
        view_menu.addAction(self.toggle_structure_action)
        view_menu.addAction(self.toggle_log_action)
        view_menu.addSeparator()  # 添加分隔线
        view_menu.addAction(restore_layout_action)

        # 执行菜单
        execute_menu = menubar.addMenu('执行')

        # 设置可执行文件
        settings_action = QAction('设置可执行文件', self)
        settings_action.triggered.connect(self.show_executable_settings)
        execute_menu.addAction(settings_action)

        # 运行按钮
        run_action = QAction('运行', self)
        run_action.setShortcut('F5')  # 添加快捷键
        run_action.triggered.connect(self.run_executable)
        execute_menu.addAction(run_action)

        # 添加绘图菜单
        plot_menu = menubar.addMenu('绘图')

        # 添加 plot 动作
        plot_action = QAction('打开绘图窗口', self)
        plot_action.setShortcut('Ctrl+P')  # 添加快捷键
        plot_action.triggered.connect(self.show_plot_window)
        plot_menu.addAction(plot_action)

        # 模型菜单
        model_menu = menubar.addMenu('模型')

        # 线缆模型库按钮
        cable_model_action = QAction('线缆模型库', self)
        cable_model_action.triggered.connect(self.open_cable_model_library)
        model_menu.addAction(cable_model_action)

    def toggle_tree_dock(self):
        self.tree_dock.setVisible(not self.tree_dock.isVisible())

    def toggle_structure_dock(self):
        self.structure_dock.setVisible(not self.structure_dock.isVisible())

    def toggle_log_dock(self):
        self.log_dock.setVisible(not self.log_dock.isVisible())

    def update_tree_action(self, visible):
        self.toggle_tree_action.setChecked(visible)

    def update_structure_action(self, visible):
        self.toggle_structure_action.setChecked(visible)

    def update_log_action(self, visible):
        self.toggle_log_action.setChecked(visible)

    def show_executable_settings(self):
        """显示可执行文件设置对话框"""
        dialog = ExecutableSettingsDialog(self)
        dialog.executable_input.setText(self.executable_path)
        dialog.work_dir_input.setText(self.work_dir)
        dialog.arguments_input.setText(' '.join(self.executable_args))

        if dialog.exec_():
            self.executable_path = dialog.executable_input.text().strip()
            self.work_dir = dialog.work_dir_input.text().strip()
            self.executable_args = dialog.arguments_input.text().strip().split()

            self.log_widget.add_log(f"设置求解器路径: {self.executable_path}")
            self.log_widget.add_log(f"工作目录: {self.work_dir}")
            self.log_widget.add_log(f"参数: {' '.join(self.executable_args)}")

    def run_executable(self):
        """运行求解器"""
        if not self.executable_path:
            self.log_widget.add_log("请先设置求解器路径", "ERROR")
            return

        self.log_widget.add_log(
            f"开始执行: {self.executable_path} {' '.join(self.executable_args)}")

        # 设置工作目录
        work_dir = self.work_dir if self.work_dir else QDir.currentPath()
        self.process.setWorkingDirectory(work_dir)

        # 启动进程
        self.process.start(self.executable_path, self.executable_args)

        if not self.process.waitForStarted():
            self.log_widget.add_log("启动进程失败", "ERROR")

    def handle_stdout(self):
        """处理标准输出"""
        data = self.process.readAllStandardOutput().data().decode()
        self.log_widget.add_log(data.strip())

    def handle_stderr(self):
        """处理标准错误"""
        data = self.process.readAllStandardError().data().decode()
        self.log_widget.add_log(data.strip(), "ERROR")

    def process_finished(self, exit_code, exit_status):
        """处理进程结束"""
        status_text = "正常" if exit_status == QProcess.NormalExit else "异常"
        self.log_widget.add_log(f"进程结束，退出代码: {exit_code}，状态: {status_text}")

    def show_plot_window(self):
        """显示绘图窗口"""
        # 创建绘图窗口
        self.plot_window = DataFramePlotterQt()

        # 显示窗口
        self.plot_window.show()

    def open_cable_model_library(self):
        self.table_widget = TableWidget()
        self.table_widget.rowLoaded.connect(
            self.load_image_into_structure_viewer)
        self.table_widget.show()

    def load_image_into_structure_viewer(self, paths):
        self.structure_viewer.add_structures(paths)

    def restore_default_layout(self):
        """恢复默认的窗口布局"""
        # 确保所有 dock widgets 都可见
        self.tree_dock.setVisible(True)
        self.structure_dock.setVisible(True)
        self.log_dock.setVisible(True)

        # 恢复到初始布局状态
        self.restoreState(self.default_state)

        # 更新菜单项的选中状态
        self.toggle_tree_action.setChecked(True)
        self.toggle_structure_action.setChecked(True)
        self.toggle_log_action.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
