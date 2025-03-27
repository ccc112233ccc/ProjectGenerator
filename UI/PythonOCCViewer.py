from OCC.Display.backend import get_qt_modules, load_backend
from OCC.Extend.DataExchange import read_step_file_with_names_colors
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from typing import Any, Callable, List, Optional, Tuple
from OCC.Display.SimpleGui import init_display

load_backend()
QtCore, QtGui, QtWidgets, QtOpenGL = get_qt_modules()

from OCC.Display.qtDisplay import qtViewer3d

class PythonOCCViewer(QtWidgets.QWidget):
    def __init__(self, *args: Any) -> None:
        QtWidgets.QWidget.__init__(self, *args)
        self.canva = qtViewer3d(self)
        self.setWindowTitle(
            f"pythonOCC"
        )
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().addWidget(self.canva)

    def load_step_file(self, filename: str) -> None:
        shapes_labels_colors = read_step_file_with_names_colors(filename)
        display = self.canva._display
        for shpt_lbl_color in shapes_labels_colors:
            label, c = shapes_labels_colors[shpt_lbl_color]
            display.DisplayColoredShape(
                shpt_lbl_color,
                color=Quantity_Color(c.Red(), c.Green(), c.Blue(), Quantity_TOC_RGB),
            )

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = PythonOCCViewer()

    filename = "models/JEPJ85.step"
    win.load_step_file(filename)
    win.show()
    app.exec_()
