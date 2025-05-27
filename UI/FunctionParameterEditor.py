import inspect
from enum import Enum
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QComboBox, QLabel, QSizePolicy, QScrollArea, QPushButton
)
from PySide6.QtCore import Qt
from UI.tools import Distance, Frequency, Conductivity, Permeability, Float, Int, FilePath
from UI.UnitInputWidget import DistanceInputWidget, FrequencyInputWidget, ConductivityInputWidget, PermeabilityInputWidget, FloatInputWidget, IntInputWidget,FileInputWidget

class FunctionParameterEditor(QWidget):
    def __init__(self, func=None, parent=None):
        super().__init__(parent)
        self.func = func
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Configurations")

        with open("UI/FunctionParameterEditor.qss", "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())

        # 创建一个QScrollArea并将表单布局嵌入其中
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.scroll_widget = QWidget()
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)

        # self.button = QPushButton("Run")
        # self.layout.addWidget(self.button)
        # self.button.clicked.connect(self.test_function)

        self.form_layout = QFormLayout(self.scroll_widget)
        self.scroll_widget.setLayout(self.form_layout)

        self.set_ui()

    def set_ui(self):
        # 清空布局中的所有控件
        for i in range(self.form_layout.rowCount()):
            self.form_layout.removeRow(0)
        if self.func is None:
            return
        self.inputs = {}
        # Inspect the function's parameters
        sig = inspect.signature(self.func)
        for name, param in sig.parameters.items():
            if param.annotation == Int or param.annotation == int:
                input_widget = IntInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            elif param.annotation == Float or param.annotation == float:
                input_widget = FloatInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            elif param.annotation == bool:
                input_widget = QCheckBox()
                if param.default is not param.empty:
                    input_widget.setChecked(param.default)
            elif issubclass(param.annotation, Enum):
                input_widget = QComboBox()
                input_widget.addItems([e.name for e in param.annotation])
                if param.default is not param.empty:
                    input_widget.setCurrentText(param.default.name)
            elif param.annotation == Distance:
                input_widget = DistanceInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            elif param.annotation == Frequency:
                input_widget = FrequencyInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            elif param.annotation == Conductivity:
                input_widget = ConductivityInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            elif param.annotation == Permeability:
                input_widget = PermeabilityInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            elif param.annotation == FilePath:
                input_widget = FileInputWidget()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            else:
                input_widget = QLineEdit()
                if param.default is not param.empty:
                    input_widget.setText(str(param.default))
            self.inputs[name] = input_widget
            self.form_layout.addRow(QLabel(name), input_widget)

    def change_function(self, func):
        self.func = func
        self.set_ui()

    def get_kargs(self):
        kwargs = {}
        for name, widget in self.inputs.items():
            if isinstance(widget, QCheckBox):
                kwargs[name] = widget.isChecked()
            elif isinstance(widget, QComboBox):
                enum_class = self.func.__annotations__[name]
                kwargs[name] = enum_class[widget.currentText()]
            elif isinstance(widget, QLineEdit) or isinstance(widget, FileInputWidget):
                kwargs[name] = widget.text()
            else:
                kwargs[name] = widget.value()
        return kwargs
    def __call__(self, *args, **kwds):
        
        kwargs = self.get_kargs()
        print("Solver Started")
        result = self.func(**kwargs)
        print("Solver Completed")
        return result
if __name__ == "__main__":
    import sys

    class SampleEnum(Enum):
        OPTION_A = "Option A"
        OPTION_B = "Option B"
        OPTION_C = "Option C"

    def sample_function(a: int, b: float, c: str, d: bool, e: SampleEnum):
        return f"Received: a={a}, b={b}, c={c}, d={d}, e={e}"

    app = QApplication(sys.argv)
    editor = FunctionParameterEditor(sample_function)
    editor.resize(400, 300)
    editor.show()

    sys.exit(app.exec())
