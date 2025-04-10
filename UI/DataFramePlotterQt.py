from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QComboBox, QFileDialog, QListWidget, QLabel,
                               QMdiArea, QMdiSubWindow)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QActionGroup
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import sys
import pandas as pd
import matplotlib.pyplot as plt
from ast import literal_eval
import matplotlib
import numpy as np
import os
matplotlib.use('QtAgg')


class DataFramePlotterQt(QMainWindow):
    def __init__(self, file_name=None):
        super().__init__()
        self.setWindowTitle("DataFrame Visualization Tool")
        self.setGeometry(100, 100, 1200, 800)

        # 初始化数据
        self.df = None
        self.current_plot_type = "Decibel"
        self.plot_mode = "Overlay"
        self.current_figure = None
        self.figure_count = 0

        self.init_ui()

        if file_name:
            self.load_csv_from_file(file_name)

    def init_ui(self):
        # 创建主窗口部件和布局
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)

        # 创建左侧变量列表面板
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setSpacing(10)  # 设置组件之间的间距
        left_layout.setContentsMargins(10, 10, 10, 10)  # 添加边距

        # 创建变量列表
        self.var_list = QListWidget()
        self.var_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 5px;
                background-color: #f8f9fa;
            }
            QListWidget::item {
                padding: 5px;
                margin: 2px 0;
            }
            QListWidget::item:selected {
                background-color: #007bff;
                color: white;
                border-radius: 3px;
            }
        """)
        self.var_list.setSelectionMode(QListWidget.SingleSelection)
        left_layout.addWidget(self.var_list, stretch=1)  # 添加stretch=1让列表扩展填充空间

        # 创建轴选择区域（使用组框）
        axes_widget = QWidget()
        axes_widget.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 10px;
            }
            QLabel {
                font-weight: bold;
            }
        """)
        axes_layout = QVBoxLayout(axes_widget)

        # X轴选择区域
        x_layout = QHBoxLayout()
        x_label_title = QLabel("X-axis:")
        self.x_label = QLabel("Not Selected")
        self.x_label.setStyleSheet("color: #666; padding: 3px;")
        x_layout.addWidget(x_label_title)
        x_layout.addWidget(self.x_label)
        axes_layout.addLayout(x_layout)

        # Y轴选择区域
        y_layout = QHBoxLayout()
        y_label_title = QLabel("Y-axis:")
        self.y_label = QLabel("Not Selected")
        self.y_label.setStyleSheet("color: #666; padding: 3px;")
        y_layout.addWidget(y_label_title)
        y_layout.addWidget(self.y_label)
        axes_layout.addLayout(y_layout)

        left_layout.addWidget(axes_widget)

        # 添加按钮
        button_style = """
            QPushButton {
                border: none;
                padding: 8px;
                border-radius: 4px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #004085;
            }
        """

        button_layout = QHBoxLayout()
        select_x_btn = QPushButton("Set as X-axis")
        select_y_btn = QPushButton("Set as Y-axis")
        select_x_btn.setStyleSheet(button_style)
        select_y_btn.setStyleSheet(button_style)
        select_x_btn.clicked.connect(self.set_x_variable)
        select_y_btn.clicked.connect(self.set_y_variable)
        button_layout.addWidget(select_x_btn)
        button_layout.addWidget(select_y_btn)
        left_layout.addLayout(button_layout)

        # 设置左侧面板的最小宽度
        left_panel.setMinimumWidth(200)

        # 修改右侧面板为MDI区域
        self.mdi_area = QMdiArea()
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # 添加左右面板到主布局
        layout.addWidget(left_panel, stretch=1)
        layout.addWidget(self.mdi_area, stretch=3)

        # 创建菜单栏
        self.create_menus()

    def create_menus(self):
        menubar = self.menuBar()

        # 文件菜单
        file_menu = menubar.addMenu('File')
        open_action = QAction('Open CSV', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.load_csv)
        file_menu.addAction(open_action)

        # 添加清空图表选项
        clear_action = QAction('Clear Plot', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.clear_current_plot)
        file_menu.addAction(clear_action)

        # 绘图类型菜单
        plot_menu = menubar.addMenu('Plot Type')
        plot_types = ["Original", "Absolute", "Decibel", "Phase Angle"]
        plot_group = QActionGroup(self)

        for plot_type in plot_types:
            action = QAction(plot_type, self, checkable=True)
            action.triggered.connect(
                lambda checked, t=plot_type: self.set_plot_type(t))
            plot_group.addAction(action)
            plot_menu.addAction(action)
            if plot_type == "Original":
                action.setChecked(True)

        # 新增：绘图模式菜单
        mode_menu = menubar.addMenu('Plot Mode')
        mode_group = QActionGroup(self)

        for mode in ["Overlay", "Append", "New Window"]:
            action = QAction(mode, self, checkable=True)
            action.triggered.connect(
                lambda checked, m=mode: self.set_plot_mode(m))
            mode_group.addAction(action)
            mode_menu.addAction(action)
            if mode == "Overlay":
                action.setChecked(True)

    def set_plot_type(self, plot_type):
        """设置绘图类型并更新图表"""
        self.current_plot_type = plot_type
        self.update_plot()

    def set_x_variable(self):
        """设置X轴变量"""
        current_item = self.var_list.currentItem()
        if current_item:
            self.x_label.setText(current_item.text())
            self.update_plot()

    def set_y_variable(self):
        """设置Y轴变量"""
        current_item = self.var_list.currentItem()
        if current_item:
            self.y_label.setText(current_item.text())
            self.update_plot()

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        if file_name:
            self.load_csv_from_file(file_name)

    def load_csv_from_file(self, file_name=None):
        """加载CSV文件"""
        if file_name:
            try:
                self.df = pd.read_csv(file_name)

                for col in self.df.columns:
                    try:
                        # 首先检查该列是否包含复数数据
                        self.df[col] = self.df[col].str.replace('im', 'j')
                        self.df[col] = self.df[col].apply(literal_eval)
                    except Exception:
                        # 如果转换失败，保持原始数据
                        print(col, "转换失败")
                        continue

                # 更新变量列表
                self.var_list.clear()  # 清除现有项目
                self.var_list.addItems(self.df.columns)  # 添加新的列名

            except Exception as e:
                print(f"Error: {str(e)}")

    def set_plot_mode(self, mode):
        """设置绘图模式"""
        self.plot_mode = mode

    def create_new_plot_window(self):
        """创建新的绘图子窗口"""
        self.figure_count += 1
        sub_window = QMdiSubWindow()
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # 创建matplotlib图形和工具栏
        figure = Figure(figsize=(8, 6))
        canvas = FigureCanvas(figure)
        toolbar = NavigationToolbar(canvas, widget)

        layout.addWidget(toolbar)
        layout.addWidget(canvas)

        sub_window.setWidget(widget)
        sub_window.setWindowTitle(f"图表 {self.figure_count}")
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

        return figure, canvas

    def update_plot(self):
        if self.df is None:
            return

        try:
            x_col = self.x_label.text()
            y_col = self.y_label.text()

            if x_col == "Not Selected" or y_col == "Not Selected":
                return

            # 根据绘图模式决定操作
            if self.plot_mode == "New Window" or self.current_figure is None:
                self.current_figure, current_canvas = self.create_new_plot_window()
            else:
                # 获取当前活动窗口的画布
                active_window = self.mdi_area.activeSubWindow()
                if active_window:
                    current_canvas = active_window.widget().findChild(FigureCanvas)
                    self.current_figure = current_canvas.figure
                else:
                    self.current_figure, current_canvas = self.create_new_plot_window()

            # 根据模式决定是否清除图形
            if self.plot_mode == "Overlay":
                self.current_figure.clear()
                ax = self.current_figure.add_subplot(111)
            elif self.plot_mode in ["Append", "New Window"]:
                # 获取现有的轴对象，如果没有则创建新的
                if len(self.current_figure.axes) == 0:
                    ax = self.current_figure.add_subplot(111)
                else:
                    ax = self.current_figure.axes[0]

            # 绘图代码
            y_data = self.df[y_col]
            if self.current_plot_type == "Absolute":
                y_plot = abs(y_data)
                ylabel = f"|{y_col}|"
            elif self.current_plot_type == "Decibel":
                y_plot = 20 * np.log10(abs(y_data))
                ylabel = f"{y_col} (dB)"
            elif self.current_plot_type == "Phase Angle":
                y_plot = np.angle(y_data, deg=True)
                ylabel = f"∠{y_col} (°)"
            else:  # 原始值
                y_plot = y_data
                ylabel = y_col

            # 绘制新的曲线
            ax.plot(self.df[x_col], y_plot, 'o-', label=ylabel)

            # 更新轴标签和标题
            ax.set_xlabel(x_col)
            ax.set_ylabel(ylabel)
            if self.plot_mode == "Overlay":
                ax.set_title(f'{y_col} vs {x_col}')
            else:
                # 追加模式下更新标题以反映多个变量
                current_title = ax.get_title()
                if not current_title:
                    ax.set_title(f'{y_col} vs {x_col}')
                elif y_col not in current_title:
                    ax.set_title(f'{current_title} & {y_col}')

            ax.grid(True)
            ax.legend()  # 添加图例

            # 添加x轴单位为hz
            ax.xaxis.set_major_formatter(
                plt.FuncFormatter(lambda x, _: f'{x:.2e} Hz'))

            # 刷新画布
            current_canvas.draw()

        except Exception as e:
            print(f"绘图错误: {str(e)}")

    def clear_current_plot(self):
        """清空当前活动窗口的图表"""
        active_window = self.mdi_area.activeSubWindow()
        if active_window:
            canvas = active_window.widget().findChild(FigureCanvas)
            if canvas:
                figure = canvas.figure
                figure.clear()
                canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = DataFramePlotterQt()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
