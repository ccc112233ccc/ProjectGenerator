import random
import os
from PySide6 import QtWidgets, QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
import pyvista as pv
from pyvista.plotting.opts import ElementType
from pyvistaqt import QtInteractor
import numpy as np
from loguru import logger

from matplotlib.colors import PowerNorm
from pathlib import Path


# 定义一个enmu类，用于表示不同的文件类型
class FileType:
    BND = 0
    TIF = 1
    VTK = 2
    TDR = 3
    OTHER = 4


def get_file_type(file_name):
    if file_name.split('.')[-1] == 'bnd':
        return FileType.BND
    elif file_name.split('.')[-1] == 'vtk':
        return FileType.VTK
    elif file_name.split('.')[-1] == 'tif':
        return FileType.TIF
    elif file_name.split('.')[-1] == 'tdr':
        return FileType.TDR
    else:
        return FileType.OTHER


class VtkWindow(QtWidgets.QMainWindow):
    def __init__(self, file_name=None):
        super().__init__()

        # 为了兼容之前写的格式，防止报错，下面的字段先保留
        self.actor = None
        self.dargs = {'show_edges': True, 'lighting': True, 'opacity': 1, 'cmap': 'jet', 'show_scalar_bar': True,
                      'log_scale': False}

        self.file_name = file_name
        self.file_type = None
        if self.file_name is not None:
            self.file_type = get_file_type(self.file_name)
        self.initUI()  # 初始化UI界面, 包括self.plotter, self.centralwidget, self.frame等
        # self.draw3d()  # 根据文件类型，绘制3D图像

    def draw3d(self):
        if self.file_type is None:
            logger.info("file type is None")
            return
        if self.file_type == FileType.VTK:
            self.draw_vtk()
        elif self.file_type == FileType.OTHER:
            logger.info(f"file format not support now {self.file_name}")
            exit(0)
        else:
            self.draw_tdr()

    def draw_tdr(self):
        if self.widget.file_name is not None:
            mesh_actors = self.widget.mesh_actors
            actors = self.widget.actors
            for region, mesh in self.widget.meshes.items():
                mesh_actors[region] = self.plotter.add_mesh(mesh, **self.dargs)

            # self.actor = self.plotter.add_mesh(mesh, **self.dargs)
            actors['axes'] = self.plotter.add_axes()

            if self.widget.chk_title.isChecked():
                title = self.widget.ted_title.toPlainText()
                actors['title'] = self.plotter.add_text(title, font_size=12, position=(0.5, 10))

            if self.widget.chk_axes.isChecked():
                actors['grid'] = self.plotter.show_grid()

            self.plotter.set_background(color=self.widget.background_color)

            # self.plotter.aspect_ratio = (1,1,1)
            self.plotter.view_xy()
            #   self.plotter.camera_position = 'yx'
            self.plotter.camera.roll = -90

            for region, mesh in self.widget.meshes.items():
                self.widget.curr_scalar = mesh.active_scalars_name
            self.plotter.show()

    def draw_vtk(self):
        self.mesh = pv.read(self.file_name)
        scalar = None
        for name in self.mesh.point_data.keys():
            scalar = name
            break
        if scalar:
            self.mesh.set_active_scalars(scalar)
        self.actor = self.plotter.add_mesh(self.mesh, **self.dargs)
        self.plotter.show_axes()

    def initUI(self, off_screen=False):
        self.setWindowTitle('VTK Render Window')
        self.resize(1080, 800)

        self.frame = QFrame()
        self.plotter = QtInteractor(
            parent=self.frame,
            off_screen=off_screen,
            stereo=False, )

        self.centralwidget = QtWidgets.QWidget()
        # 将表格显示在窗口中
        layout = QVBoxLayout()
        layout.addWidget(self.plotter.interactor)
        self.centralwidget.setLayout(layout)
        self.setCentralWidget(self.centralwidget)
    def Open(self):
        open_dir = os.getcwd()

        file_filter = 'TDR Files (*.tdr);;VTK Files (*.vtk);;All files(*.*)'
        fileName_choose, file = QFileDialog.getOpenFileName(
            parent=self.centralwidget,
            caption='Open File',
            directory=open_dir,
            filter=file_filter,
            initialFilter='TDR Files (*.tdr)',

        )
        if fileName_choose == "":
            print("\n取消选择")
            return

        # print("\n你选择的文件为:")
        print(fileName_choose)
        self.file_name = fileName_choose

        if self.file_name is not None:
            # 得到文件的类型
            self.file_type = get_file_type(self.file_name)
        self.replace_dock_content()
        self.plotter.clear()
        # self.plotter.close()
        self.draw3d()

    def resetCamera(self):
        self.plotter.view_xy()
        #   self.plotter.camera_position = 'yx'
        self.plotter.camera.roll = -90

    def viewPlaneXY(self):
        self.plotter.view_xy()

    def viewPlaneYZ(self):
        self.plotter.view_yz()

    def viewPlaneXZ(self):
        self.plotter.view_xz()

    def cutX(self):
        plotter = pv.Plotter()
        plotter.add_mesh_clip_plane(self.widget.mesh, normal='x', normal_rotation=False, cmap='jet')
        plotter.show()

    def cutY(self):
        plotter = pv.Plotter()
        plotter.add_mesh_clip_plane(self.widget.mesh, normal='y', normal_rotation=False, cmap='jet')
        plotter.show()

    def cutZ(self):
        plotter = pv.Plotter()
        plotter.add_mesh_clip_plane(self.widget.mesh, normal='z', normal_rotation=False, cmap='jet')
        plotter.show()

    def probe(self, state):
        if not state:
            self.plotter._clear_picking_representations()
            self.plotter.disable_picking()
            self.switch_tab(self.widget.tabWidget_7,0)
        else:
            self.plotter.enable_surface_point_picking(callback=self.widget.on_click, use_picker=True, left_clicking=True,
                                              show_message=False)
            self.switch_tab(self.widget.tabWidget_7, 1)

    def test(self):
        logger.info("test")
        index = random.randint(0, 2)
        print(index)
        self.widget.cmb_levels_func.setCurrentIndex(index)

    def switch_tab(self,tab_widget, index):
        tab_widget.setCurrentIndex(index)



if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    # file = 'data/NLDMOS_des.tif'
    file = 'data/tdr/n2_des.tdr'
    # file = 'data/5V_NMOS_bnd.tdr'
    # file = 'data/n2_des.tdr'
    # file = 'data/aaa.bnd'
    # file = None
    ex = VtkWindow(file)
    ex.show()
    sys.exit(app.exec_())
