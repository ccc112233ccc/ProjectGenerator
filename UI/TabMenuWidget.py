from UI.UITabMenuWidget import Ui_TabMenuWidget
from PySide6.QtWidgets import QTabWidget, QWidget, QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem





class TabMenuWidget(QWidget):
    def __init__(self, parent=None):
        super(TabMenuWidget, self).__init__(parent)
        self.ui = Ui_TabMenuWidget()
        self.ui.setupUi(self)