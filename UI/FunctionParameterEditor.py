import inspect
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QPushButton, QLabel
)
from PySide6.QtCore import Qt


class FunctionParameterEditor(QWidget):
    def __init__(self, func=None, parent=None):
        super().__init__(parent)
        self.func = func
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"configurations")
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.layout.addLayout(self.form_layout)
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
            if param.annotation == int:
                input_widget = QSpinBox()
                input_widget.setMaximum(1e7)
                if param.default is not param.empty:
                    input_widget.setValue(param.default)
            elif param.annotation == float:
                input_widget = QDoubleSpinBox()
                input_widget.setMaximum(1e30)
                input_widget.setDecimals(6)
                if param.default is not param.empty:
                    input_widget.setValue(param.default)
            elif param.annotation == bool:
                input_widget = QCheckBox()
                if param.default is not param.empty:
                    input_widget.setChecked(param.default)
            else:
                input_widget = QLineEdit()
                if param.default is not param.empty:
                    input_widget.setText(param.default)

            self.inputs[name] = input_widget
            self.form_layout.addRow(QLabel(name), input_widget)

    def change_function(self, func):
        self.func = func
        self.set_ui()

    def __call__(self, *args, **kwds):
        kwargs = {}
        for name, widget in self.inputs.items():
            if isinstance(widget, QSpinBox):
                kwargs[name] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                kwargs[name] = widget.value()
            elif isinstance(widget, QCheckBox):
                kwargs[name] = widget.isChecked()
            else:
                kwargs[name] = widget.text()

        result = self.func(**kwargs)
        print("Task completed")
        return result


if __name__ == "__main__":
    import sys

    def sample_function(a: int, b: float, c: str, d: bool):
        return f"Received: a={a}, b={b}, c={c}, d={d}"

    app = QApplication(sys.argv)
    editor = FunctionParameterEditor(sample_function)
    editor.show()
    sys.exit(app.exec())
