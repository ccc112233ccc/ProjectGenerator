import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QPushButton, QFileDialog, QLabel,
                              QComboBox, QMenu, QMdiArea, QMdiSubWindow)
from PySide6.QtGui import QAction, QActionGroup
from PySide6.QtCore import Qt
import scipy.io as sio

class LinePlotWindow(QMdiSubWindow):
    def __init__(self, data, title):
        super().__init__()
        self.data = data
        
        # 创建主部件
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # 创建matplotlib图形
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, main_widget)
        
        # 添加组件到布局
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.setWidget(main_widget)
        self.setWindowTitle(title)
        
        # 绘制曲线
        self.plot_line()
        
    def plot_line(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.data)
        ax.grid(True)
        ax.set_title('Line Plot')
        ax.set_xlabel('Index')
        ax.set_ylabel('Value')
        self.canvas.draw()

class MatrixWindow(QMdiSubWindow):
    def __init__(self, matrix, title, parent=None):
        super().__init__()
        self.matrix = matrix
        self.show_colorbar = True
        self.parent = parent  # 保存父窗口引用
        self.selected_row = None  # 存储选中的行
        self.selected_col = None  # 存储选中的列
        
        # 创建主部件
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # 创建matplotlib图形
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, main_widget)
        
        # 添加组件到布局
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        
        self.setWidget(main_widget)
        self.setWindowTitle(title)
        
        # 绘制矩阵
        self.plot_matrix()
        
        # 连接鼠标点击事件
        self.canvas.mpl_connect('button_press_event', self.on_click)
    
    def on_click(self, event):
        if event.inaxes:
            if event.button == 1:  # 左键点击选择行
                self.selected_row = int(event.ydata + 0.5)
                self.plot_line_data(self.matrix[self.selected_row, :], f'Row {self.selected_row}')
            elif event.button == 3:  # 右键点击选择列
                self.selected_col = int(event.xdata + 0.5)
                self.plot_line_data(self.matrix[:, self.selected_col], f'Column {self.selected_col}')
    
    def plot_line_data(self, data, title):
        if self.parent:
            self.parent.create_line_plot(data, title)

    def plot_matrix(self, cmap='viridis'):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        im = ax.imshow(self.matrix, cmap=cmap, aspect='auto')
        if self.show_colorbar:  # 根据标志决定是否显示 colorbar
            self.figure.colorbar(im)
        ax.set_title(f'shape: {self.matrix.shape}')
        self.canvas.draw()

class MatrixVisualizerQt(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("matrix visual")
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建 MDI 区域
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        
        # 初始化数据
        self.current_cmap = 'viridis'
        self.create_menus()
        
    def create_menus(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        
        # 打开.mat文件
        open_mat_action = QAction('打开.mat文件', self)
        open_mat_action.setShortcut('Ctrl+M')
        open_mat_action.triggered.connect(self.load_mat)
        
        # 打开.npy文件
        open_npy_action = QAction('打开.npy文件', self)
        open_npy_action.setShortcut('Ctrl+N')
        open_npy_action.triggered.connect(self.load_npy)
        
        # 添加打开.csv文件的动作
        open_csv_action = QAction('打开.csv文件', self)
        open_csv_action.setShortcut('Ctrl+C')
        open_csv_action.triggered.connect(self.load_csv)
        
        file_menu.addAction(open_mat_action)
        file_menu.addAction(open_npy_action)
        file_menu.addAction(open_csv_action)  # 添加到菜单

        # 添加视图菜单
        view_menu = menubar.addMenu('视图')
        
        # 添加颜色映射子菜单
        cmap_menu = view_menu.addMenu('颜色映射')
        
        # 创建动作组使选项互斥
        self.cmap_group = QActionGroup(self)
        
        # 添加不同的颜色映射选项
        cmap_options = ['viridis', 'jet', 'hot', 'coolwarm', 'gray']
        for cmap in cmap_options:
            action = QAction(cmap, self)
            action.setCheckable(True)
            if cmap == self.current_cmap:
                action.setChecked(True)
            self.cmap_group.addAction(action)
            cmap_menu.addAction(action)
        
        # 连接动作组的信号
        self.cmap_group.triggered.connect(self.change_cmap)

        # 添加 colorbar 显示控制动作
        self.show_colorbar_action = QAction('显示 Colorbar', self)
        self.show_colorbar_action.setCheckable(True)
        self.show_colorbar_action.setChecked(True)
        self.show_colorbar_action.triggered.connect(self.toggle_colorbar)
        view_menu.addAction(self.show_colorbar_action)

    def change_cmap(self, action):
        self.current_cmap = action.text()
        # 只更新当前活跃窗口的颜色映射
        active_window = self.mdi.activeSubWindow()
        if isinstance(active_window, MatrixWindow):
            active_window.plot_matrix(self.current_cmap)

    def load_mat(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择MAT文件", "", "MAT Files (*.mat);;All Files (*)"
        )
        
        if file_name:
            try:
                mat_data = sio.loadmat(file_name)
                # 获取第一个非特殊变量（不以__开头的变量）
                for key in mat_data.keys():
                    if not key.startswith('__'):
                        matrix = mat_data[key]
                        self.create_matrix_window(matrix, f"MAT: {key}")
                        break
            except Exception as e:
                print(f"加载MAT文件错误: {str(e)}")
    
    def load_npy(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择NPY文件", "", "NPY Files (*.npy);;All Files (*)"
        )
        
        if file_name:
            try:
                matrix = np.load(file_name)
                self.create_matrix_window(matrix, f"NPY: {file_name.split('/')[-1]}")
            except Exception as e:
                print(f"加载NPY文件错误: {str(e)}")

    def load_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "选择CSV文件", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_name:
            try:
                # 先读取第一行来确定列数
                with open(file_name) as f:
                    first_line = f.readline()
                    num_cols = len(first_line.strip().split(','))
                
                # skiprows=1 跳过表头，usecols跳过第一列
                matrix = np.loadtxt(file_name, delimiter=',', skiprows=1, usecols=range(1, num_cols))
                self.create_matrix_window(matrix, f"CSV: {file_name.split('/')[-1]}")
            except Exception as e:
                print(f"加载CSV文件错误: {str(e)}")

    def create_matrix_window(self, matrix, title):
        sub_window = MatrixWindow(matrix, title, self)  # 传入self作为父窗口
        self.mdi.addSubWindow(sub_window)
        sub_window.show()
    
    def create_line_plot(self, data, title):
        sub_window = LinePlotWindow(data, title)
        self.mdi.addSubWindow(sub_window)
        sub_window.show()

    def toggle_colorbar(self):
        # 获取当前活跃窗口
        active_window = self.mdi.activeSubWindow()
        if isinstance(active_window, MatrixWindow):
            active_window.show_colorbar = self.show_colorbar_action.isChecked()
            active_window.plot_matrix(self.current_cmap)

def main():
    app = QApplication(sys.argv)
    window = MatrixVisualizerQt()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 