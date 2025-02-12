from PySide6.QtWidgets import (QMainWindow, QApplication, QMdiArea, QMdiSubWindow, 
                             QWidget, QVBoxLayout, QFileDialog, QToolBar, QColorDialog,
                             QSlider, QDialog, QLabel, QVBoxLayout, QHBoxLayout, QInputDialog)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QAction, QColor
from PySide6.QtWebEngineWidgets import QWebEngineView
import pyvista as pv
from pyvistaqt import QtInteractor
import sys

class OpacityDialog(QDialog):
    def __init__(self, current_opacity=1.0, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置透明度")
        layout = QVBoxLayout(self)
        
        # 添加滑块和标签
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(int(current_opacity * 100))
        
        self.label = QLabel(f"{int(current_opacity * 100)}%")
        self.slider.valueChanged.connect(
            lambda v: self.label.setText(f"{v}%")
        )
        
        layout.addWidget(QLabel("透明度:"))
        layout.addWidget(self.slider)
        layout.addWidget(self.label)
        
        # 添加确定和取消按钮
        button_layout = QHBoxLayout()
        from PySide6.QtWidgets import QPushButton
        ok_button = QPushButton("确定")
        cancel_button = QPushButton("取消")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

class StructureViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.meshes = {}  # 存储mesh对象的字典
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle('Structure Viewer')
        self.resize(1200, 800)
        
        # 创建 MDI 区域
        self.mdi_area = QMdiArea()
        self.setCentralWidget(self.mdi_area)
        
        # 创建菜单栏
        self.create_menu()
        
        
    def create_menu(self):
        menubar = self.menuBar()
        
        # 文件菜单
        file_menu = menubar.addMenu('文件')
        open_action = QAction('打开结构', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_structures)
        file_menu.addAction(open_action)
        
        # 视图菜单
        view_menu = menubar.addMenu('视图')
        
        # 级联排列
        cascade_action = QAction('级联排列', self)
        cascade_action.triggered.connect(self.mdi_area.cascadeSubWindows)
        
        # 平铺排列
        tile_action = QAction('平铺排列', self)
        tile_action.triggered.connect(self.mdi_area.tileSubWindows)
        
        view_menu.addAction(cascade_action)
        view_menu.addAction(tile_action)
        
        # 编辑菜单
        edit_menu = menubar.addMenu('编辑')
        
        color_action = QAction('更改颜色', self)
        color_action.triggered.connect(self.change_color)
        
        opacity_action = QAction('更改透明度', self)
        opacity_action.triggered.connect(self.change_opacity)
        
        edit_menu.addAction(color_action)
        edit_menu.addAction(opacity_action)

        # 在线模型菜单
        online_menu = menubar.addMenu('在线模型')
        open_url_action = QAction('打开在线模型', self)
        open_url_action.triggered.connect(self.open_online_model)
        online_menu.addAction(open_url_action)

    def open_online_model(self):
        url, ok = QInputDialog.getText(self, '输入URL', '请输入模型的URL:')
        if ok and url:
            self.add_online_model(url)

    def add_online_model(self, url):
        # 创建子窗口
        sub_window = QMdiSubWindow()
        
        # 创建容器
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建 QWebEngineView
        web_view = QWebEngineView(container)
        web_view.setUrl(url)
        layout.addWidget(web_view)
        
        # 设置子窗口的部件和标题
        sub_window.setWidget(container)
        sub_window.setWindowTitle(url)
        
        # 设置子窗口的最小尺寸
        sub_window.setMinimumSize(400, 300)
        
        # 将子窗口添加到MDI区域
        self.mdi_area.addSubWindow(sub_window)
        sub_window.show()

    def get_current_plotter_and_mesh(self):
        """获取当前活动窗口的plotter和mesh"""
        current_window = self.mdi_area.activeSubWindow()
        if current_window:
            container = current_window.widget()
            plotter = container.findChild(QtInteractor)
            if plotter and current_window in self.meshes:
                return plotter, self.meshes[current_window]
        return None, None

    def change_color(self):
        """更改当前选中模型的颜色"""
        plotter, mesh = self.get_current_plotter_and_mesh()
        if plotter and mesh:
            color = QColorDialog.getColor()
            if color.isValid():
                # 获取当前的不透明度
                current_opacity = mesh.opacity if hasattr(mesh, 'opacity') else 1.0
                # 清除当前显示
                plotter.clear()
                # 使用新颜色重新显示
                plotter.add_mesh(mesh, color=color.getRgbF()[:3], opacity=current_opacity, show_edges=True)
                plotter.reset_camera()

    def change_opacity(self):
        """更改当前选中模型的透明度"""
        plotter, mesh = self.get_current_plotter_and_mesh()
        if plotter and mesh:
            # 获取当前透明度
            current_opacity = getattr(mesh, 'opacity', 1.0)
            dialog = OpacityDialog(current_opacity, self)
            
            if dialog.exec_():
                opacity = dialog.slider.value() / 100.0
                # 获取当前的颜色
                current_color = getattr(mesh, 'color', None)
                # 清除当前显示
                plotter.clear()
                # 使用新的透明度重新显示
                plotter.add_mesh(mesh, opacity=opacity, color=current_color, show_edges=True)
                # 存储透明度值
                mesh.opacity = opacity
                # 强制更新显示
                plotter.render()

    def add_structures_from_paths(self, structure_paths):
        """通过文件路径列表添加多个结构"""
        if not structure_paths:
            return
            
        for path in structure_paths:
            # 创建子窗口
            sub_window = QMdiSubWindow()
            
            # 创建容器
            container = QWidget()
            layout = QVBoxLayout(container)
            layout.setContentsMargins(0, 0, 0, 0)
            
            # 创建 PyVista 渲染窗口
            plotter = QtInteractor(container)
            layout.addWidget(plotter)
            
            try:
                # 读取并显示结构
                mesh = pv.read(path)
                # 初始化透明度属性
                mesh.opacity = 1.0
                plotter.add_mesh(mesh, show_edges=True, opacity=1.0)
                plotter.reset_camera()
                
                # 存储mesh对象
                self.meshes[sub_window] = mesh
                
                # 设置子窗口的部件和标题
                sub_window.setWidget(container)
                sub_window.setWindowTitle(path.split('/')[-1])
                
                # 设置子窗口的最小尺寸
                sub_window.setMinimumSize(400, 300)
                
                # 将子窗口添加到MDI区域
                self.mdi_area.addSubWindow(sub_window)
                sub_window.show()
                
            except Exception as e:
                print(f"Error loading structure {path}: {str(e)}")
    
    def add_images_from_paths(self, image_paths):
        """通过图片路径列表添加多个图片"""
        if not image_paths:
            return
            
        for path in image_paths:
            # 创建子窗口
            sub_window = QMdiSubWindow()
            
            # 创建图片容器
            container = QWidget()
            container.setStyleSheet("""
                QWidget {
                    background: white;
                }
            """)
            
            # 创建图片标签
            image_label = QLabel()
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setStyleSheet("""
                QLabel {
                    padding: 10px;
                    background: transparent;
                }
            """)
            
            # 创建布局
            layout = QVBoxLayout(container)
            layout.setContentsMargins(5, 5, 5, 5)
            layout.addWidget(image_label)
            
            # 加载并显示图片
            pixmap = QPixmap(path)
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            
            # 设置子窗口的部件和标题
            sub_window.setWidget(container)
            sub_window.setWindowTitle(path.split('/')[-1])
            
            # 设置子窗口的最小尺寸
            sub_window.setMinimumSize(300, 200)
            
            # 将子窗口添加到MDI区域
            self.mdi_area.addSubWindow(sub_window)
            sub_window.show()
    def open_structures(self):
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "选择结构文件",
            "",
            "结构文件 (*.stl *.vtk *.vtm *.vtp *.obj *.ply *.wrl *.png *.jpg *.jpeg *.glb)"
        )

        # 如果选择了图片文件，则调用add_images_from_paths   
        for path in file_paths:
            if path.endswith('.png') or path.endswith('.jpg') or path.endswith('.jpeg'):
                self.add_images_from_paths([path])
            else:
                self.add_structures_from_paths([path])
    def add_structures(self, file_paths):
        """通过路径列表添加结构"""
        for path in file_paths:
            if path.endswith('.png') or path.endswith('.jpg') or path.endswith('.jpeg'):
                self.add_images_from_paths([path])
            else:
                self.add_structures_from_paths([path])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = StructureViewer()
    viewer.show()
    sys.exit(app.exec())