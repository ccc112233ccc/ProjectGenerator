import sys
import csv
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QMenuBar, QFileDialog, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import Signal


class TableWidget(QWidget):
    rowLoaded = Signal(dict)  # Define a signal to emit row data

    def __init__(self, file_path="models/models.xlsx"):
        super().__init__()
        self.initUI()
        self.sheets = []
        self.currentFile = None
        if file_path:
            self.loadFileFromPath(file_path)
        self.setWindowTitle("models")
        self.resize(800, 600)  # 设置窗口默认大小

    def initUI(self):
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)

        self.menuBar = QMenuBar(self)
        self.fileMenu = self.menuBar.addMenu("File")
        self.openAction = QAction("Import", self)
        self.openAction.triggered.connect(self.loadFile)
        self.fileMenu.addAction(self.openAction)

        self.sheetMenu = self.menuBar.addMenu("Type")

        self.loadAction = QAction("Export", self)
        self.loadAction.triggered.connect(self.loadSelectedRow)
        self.fileMenu.addAction(self.loadAction)

        self.layout.setMenuBar(self.menuBar)

        self.setLayout(self.layout)
        self.setWindowTitle("Solver Models")

    def loadFile(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Open CSV/Excel File", "", "Excel Files (*.xlsx);;CSV Files (*.csv);;All Files (*)", options=options)
        if fileName:
            self.currentFile = fileName
            if fileName.endswith('.csv'):
                self.loadCsv(fileName)
            elif fileName.endswith('.xlsx'):
                self.loadExcel(fileName)

    def loadFileFromPath(self, file_path):
        self.currentFile = file_path
        if file_path.endswith('.csv'):
            self.loadCsv(file_path)
        elif file_path.endswith('.xlsx'):
            self.loadExcel(file_path)

    def loadCsv(self, fileName):
        with open(fileName, newline='') as csvfile:
            reader = csv.reader(csvfile)
            self.table.setRowCount(0)
            self.table.setColumnCount(0)
            for rowIndex, row in enumerate(reader):
                self.table.insertRow(rowIndex)
                self.table.setColumnCount(len(row))
                for columnIndex, item in enumerate(row):
                    self.table.setItem(
                        rowIndex, columnIndex, QTableWidgetItem(item))

    def loadExcel(self, fileName):
        import pandas as pd
        self.sheets = pd.ExcelFile(fileName).sheet_names
        self.sheetMenu.clear()
        for sheet in self.sheets:
            action = QAction(sheet, self)
            action.triggered.connect(
                lambda checked, s=sheet: self.loadSheet(s))
            self.sheetMenu.addAction(action)
        self.loadSheet(self.sheets[0])

    def loadSheet(self, sheetName):
        import pandas as pd
        self.df = pd.read_excel(self.currentFile, sheet_name=sheetName)
        self.table.setRowCount(0)
        self.table.setColumnCount(len(self.df.columns))
        self.table.setHorizontalHeaderLabels(self.df.columns)
        for rowIndex, row in self.df.iterrows():
            self.table.insertRow(rowIndex)
            for columnIndex, item in enumerate(row):
                self.table.setItem(
                    rowIndex, columnIndex, QTableWidgetItem(str(item)))

    def loadSelectedRow(self):
        selected_row = self.table.currentRow()
        # 得到当前行的数据，对应表头，返回字典
        row_data = {}
        for column in range(self.table.columnCount()):
            row_data[self.table.horizontalHeaderItem(
                column).text()] = self.df.iloc[selected_row, column]

        self.rowLoaded.emit(row_data)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    file_path = "models/models.xlsx"
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    window = TableWidget(file_path)
    window.show()
    sys.exit(app.exec())
