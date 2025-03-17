from PySide6.QtWidgets import (QMainWindow, QApplication, QDockWidget,
                               QMenu, QMenuBar, QDialog, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QLabel, QPushButton, QFileDialog, QSpinBox, QDoubleSpinBox, QCheckBox)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QProcess, QDir, QThread, Signal
import sys
import json
from template.CableSolver import CableSolver
import os
import io
import contextlib

# 假设 TreeEditor, StructureViewer, LogWidget 已经定义
# 这里简单定义它们的占位符类
from UI.TreeEditor import EditableTreeWidget
from UI.StructureViewer import StructureViewer
from UI.LogWidget import LogWidget
from UI.DataFramePlotterQt import DataFramePlotterQt
from UI.table_widget import TableWidget
from UI.FunctionParameterEditor import FunctionParameterEditor


class FunctionRunner(QThread):
    output_signal = Signal(str)

    def __init__(self, function_editor, working_directory=None):
        super().__init__()
        self.function_editor = function_editor
        self.working_directory = working_directory

    def run(self):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            original_directory = os.getcwd()
            os.chdir("codes")
            try:
                self.function_editor()
            finally:
                os.chdir(original_directory)
        output = buffer.getvalue()
        self.output_signal.emit(output)


class MainWindow(QMainWindow):
    def __init__(self, global_config_path='globalconfig.json'):
        super().__init__()
        # 从 globalconfig.json 加载配置
        self.global_config = json.load(
            open(global_config_path, 'r', encoding='utf-8'))
        self.name = self.global_config.get('name', '')

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

        # 创建并添加 FunctionParameterEditor DockWidget
        self.function_editor = FunctionParameterEditor(
            CableSolver.get_solver(1))
        self.function_dock = QDockWidget("Function Parameter Editor", self)
        self.function_dock.setFeatures(QDockWidget.DockWidgetClosable)  # 只允许关闭
        self.function_dock.setWidget(self.function_editor)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.function_dock)

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
        view_menu = menubar.addMenu('View')

        # TreeEditor 显示/隐藏
        self.toggle_tree_action = QAction(
            'Tree Editor', self, checkable=True)
        self.toggle_tree_action.setChecked(True)
        self.toggle_tree_action.triggered.connect(self.toggle_tree_dock)

        # StructureViewer 显示/隐藏
        self.toggle_structure_action = QAction(
            'Structure Viewer', self, checkable=True)
        self.toggle_structure_action.setChecked(True)
        self.toggle_structure_action.triggered.connect(
            self.toggle_structure_dock)

        # LogWidget 显示/隐藏
        self.toggle_log_action = QAction('Log', self, checkable=True)
        self.toggle_log_action.setChecked(True)
        self.toggle_log_action.triggered.connect(self.toggle_log_dock)

        # 添加复原布局动作
        restore_layout_action = QAction('Default Layout', self)
        restore_layout_action.setShortcut('Ctrl+R')  # 添加快捷键
        restore_layout_action.triggered.connect(self.restore_default_layout)

        view_menu.addAction(self.toggle_tree_action)
        view_menu.addAction(self.toggle_structure_action)
        view_menu.addAction(self.toggle_log_action)
        view_menu.addSeparator()  # 添加分隔线
        view_menu.addAction(restore_layout_action)

        # 执行菜单
        execute_menu = menubar.addMenu('Execute')

        # 运行按钮
        run_action = QAction('Run', self)
        run_action.setShortcut('F5')  # 添加快捷键
        run_action.triggered.connect(self.run_function_with_parameters)
        execute_menu.addAction(run_action)

        # 添加绘图菜单
        plot_menu = menubar.addMenu('Plot')

        # 添加 plot 动作
        plot_action = QAction('Plot', self)
        plot_action.setShortcut('Ctrl+P')  # 添加快捷键
        plot_action.triggered.connect(self.show_plot_window)
        plot_menu.addAction(plot_action)

        # 模型菜单
        model_menu = menubar.addMenu('Model')

        # 线缆模型库按钮
        cable_model_action = QAction('Open Cable Model Library', self)
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

    def handle_stdout(self):
        """处理标准输出"""
        data = self.process.readAllStandardOutput().data().decode()
        self.log_widget.add_log(data.strip())

    def handle_stderr(self):
        """处理标准错误"""
        data = self.process.readAllStandardError().data().decode()
        self.log_widget.add_log(data.strip(), "ERROR")

    def show_plot_window(self, file_path=None):
        """显示绘图窗口"""
        # 创建绘图窗口
        self.plot_window = DataFramePlotterQt(file_path)

        # 显示窗口
        self.plot_window.show()

    def open_cable_model_library(self):
        self.table_widget = TableWidget()
        self.table_widget.rowLoaded.connect(
            self.load_model)
        self.table_widget.show()

    def load_model(self, values):
        self.structure_viewer.add_structure(
            values.get('Model Path'))
        self.log_widget.add_log(f"Model {values.get('Model Name')} loaded")
        mode = values.get('ID')
        self.function_editor.change_function(CableSolver.get_solver(mode))

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

    def run_function_with_parameters(self):
        self.log_widget.add_log("Function started")
        self.function_runner = FunctionRunner(
            self.function_editor)
        self.function_runner.output_signal.connect(self.log_widget.add_log)
        self.function_runner.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
