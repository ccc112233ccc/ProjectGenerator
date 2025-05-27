from PySide6.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QComboBox, QPushButton, QFileDialog
from PySide6.QtCore import Qt


class UnitInputWidget(QWidget):
    def __init__(self, units=None, parent=None):
        super().__init__(parent)
        self.units = units or {}
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter value")
        layout.addWidget(self.input_field)

        # 单位选择框
        self.unit_selector = QComboBox(self)
        self.unit_selector.addItems(self.units.keys())
        layout.addWidget(self.unit_selector)

    def value(self):
        """获取实际值，基于当前单位的换算"""
        try:
            input_value = float(self.input_field.text())
            selected_unit = self.unit_selector.currentText()
            conversion_factor = self.units.get(selected_unit, 1)
            return input_value * conversion_factor
        except ValueError:
            return None  # 如果输入无效，返回 None

    def text(self):
        """获取控件中的字面值"""
        return self.input_field.text()
    
    def setText(self, text):
        """设置控件中的字面值"""
        self.input_field.setText(text)


# 文件输入控件
# 左侧为文件路径输入框，右侧为浏览按钮
class FileInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # 输入框
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter file path")
        layout.addWidget(self.input_field)

        # 浏览按钮
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

    def browse_file(self):
        # 打开文件对话框
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_path:
            self.input_field.setText(file_path)

    def setText(self, text):
        """设置控件中的文件路径"""
        self.input_field.setText(text)

    def text(self):
        """获取控件中的文件路径"""
        return self.input_field.text()

    


# 距离输入控件
# 继承自 UnitInputWidget
class DistanceInputWidget(UnitInputWidget):
    def __init__(self, parent=None):
        units = {
            "m": 1,
            "cm": 0.01,
            "mm": 0.001,
            "km": 1000,
        }
        super().__init__(units, parent)

# 频率输入控件
# 继承自 UnitInputWidget
class FrequencyInputWidget(UnitInputWidget):
    def __init__(self, parent=None):
        units = {
            "Hz": 1,
            "kHz": 1000,
            "MHz": 1e6,
            "GHz": 1e9,
        }
        super().__init__(units, parent)


# 电导率输入控件
# 继承自 UnitInputWidget
class ConductivityInputWidget(UnitInputWidget):
    def __init__(self, parent=None):
        units = {
            "S/m": 1,
            "mS/m": 0.001,
            "μS/m": 1e-6,
        }
        super().__init__(units, parent)

# 磁导率输入控件
# 继承自 UnitInputWidget
class PermeabilityInputWidget(UnitInputWidget):
    def __init__(self, parent=None):
        units = {
            "H/m": 1,
            "mH/m": 0.001,
            "μH/m": 1e-6,
        }
        super().__init__(units, parent)

# 无单位浮点数输入控件
# 继承自 UnitInputWidget
class FloatInputWidget(UnitInputWidget):
    def __init__(self, parent=None):
        units = {
            "": 1,  # 无单位
        }
        super().__init__(units, parent)

# 无单位整数输入控件
# 继承自 UnitInputWidget
class IntInputWidget(UnitInputWidget):
    def __init__(self, parent=None):
        units = {
            "": 1,  # 无单位
        }
        super().__init__(units, parent)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication, QVBoxLayout, QMainWindow

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Unit Input Widget Example")

            # 示例单位及其换算因子
            units = {
                "meters": 1,
                "kilometers": 1000,
                "centimeters": 0.01,
                "millimeters": 0.001,
            }

            self.unit_input = UnitInputWidget(units)

            layout = QVBoxLayout()
            layout.addWidget(self.unit_input)

            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)

            # 打印值测试
            self.unit_input.input_field.textChanged.connect(self.print_value)
            self.unit_input.unit_selector.currentIndexChanged.connect(self.print_value)

        def print_value(self):
            print(f"Text: {self.unit_input.text()}, Value: {self.unit_input.value()}")

    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 100)
    window.show()
    sys.exit(app.exec())