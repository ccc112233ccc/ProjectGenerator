from PySide6.QtWidgets import QApplication
from UI.MainWindow import MainWindow
import sys







if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow('template/globalconfig.json')
    main_window.show()
    sys.exit(app.exec()) 