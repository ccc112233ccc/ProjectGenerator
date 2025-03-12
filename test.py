
import sys
from PySide6.QtWidgets import QApplication
from UI.FunctionParameterEditor import FunctionParameterEditor
from template.zhaolong_twinax_cable_oussama_1 import zhaolong_twinax_cable_oussama_1

app = QApplication(sys.argv)
editor = FunctionParameterEditor(zhaolong_twinax_cable_oussama_1)
editor.show()
sys.exit(app.exec())
