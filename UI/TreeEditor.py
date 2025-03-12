import sys
import json
from PySide6.QtWidgets import (
    QApplication, QTreeWidget, QTreeWidgetItem, QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QCheckBox, QWidget, QVBoxLayout, QPushButton, QHeaderView, QLabel
)
from PySide6.QtCore import Qt


class EditableTreeWidget(QTreeWidget):
    def __init__(self, json_file_path, parent=None):
        super().__init__(parent)
        self.json_file_path = json_file_path
        with open(json_file_path, "r", encoding="utf-8") as file:
            self.json_data = json.load(file)
        self.setColumnCount(2)  # 设置两列
        self.setHeaderHidden(True)  # 隐藏默认的表头
        self.header().setStretchLastSection(True)  # 最后一列自动填充剩余空间
        self.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 第一列根据内容调整
        self.populate_tree()  # 填充树形控件

        # 创建保存当前值按钮
        save_current_button = QPushButton("save", self)
        save_current_button.clicked.connect(self.save_current_values)
        self.setItemWidget(QTreeWidgetItem(self), 1, save_current_button)
        self.save_current_values()

    def populate_tree(self):
        """根据 JSON 数据填充树形控件"""
        for group_name, group_data in self.json_data.items():
            # 创建顶级节点（group）
            group_item = QTreeWidgetItem(self)
            group_item.setText(0, group_name)  # 设置顶级节点的名称
            group_item.setFlags(group_item.flags() |
                                Qt.ItemIsEnabled)  # 启用顶级节点
            self.addTopLevelItem(group_item)  # 将顶级节点添加到树形控件中

            # 填充子节点
            for item_data in group_data:
                child_item = QTreeWidgetItem(group_item)
                child_item.setText(0, item_data["name"])  # 设置子节点的名称
                child_item.setFlags(child_item.flags() |
                                    Qt.ItemIsEditable)  # 启用编辑标志
                self.setup_item_widget(child_item, item_data)  # 设置子节点的控件

    def setup_item_widget(self, item, item_data):
        """根据 JSON 数据的类型设置树形项的控件"""
        if item_data["type"] == "enum":
            # 如果是枚举类型，创建一个 QComboBox（下拉框）
            combo_box = QComboBox()
            combo_box.addItems(item_data["options"])  # 添加枚举选项
            # 设置默认选中的选项
            index = item_data["options"].index(item_data["default"])
            combo_box.setCurrentIndex(index)
            # 将下拉框绑定到树形项的第二列
            self.setItemWidget(item, 1, combo_box)
            # 绑定下拉框的选项改变事件
            combo_box.currentIndexChanged.connect(
                lambda index, item=item, combo_box=combo_box: self.on_enum_changed(item, combo_box))
        elif item_data["type"] == "string":
            # 如果是字符串类型，创建一个 QLineEdit（文本框）
            line_edit = QLineEdit(item_data["default"])
            line_edit.editingFinished.connect(
                lambda item=item, line_edit=line_edit: self.on_text_changed(item, line_edit))
            self.setItemWidget(item, 1, line_edit)
        elif item_data["type"] == "int":
            # 如果是整数类型，创建一个 QSpinBox（数字输入框）
            spin_box = QSpinBox()
            spin_box.setMaximum(1e7)
            spin_box.setValue(item_data["default"])
            spin_box.valueChanged.connect(
                lambda value, item=item: self.on_int_changed(item, value))
            self.setItemWidget(item, 1, spin_box)
        elif item_data["type"] == "float":
            # 如果是浮点数类型，创建一个 QDoubleSpinBox（浮点数输入框）
            double_spin_box = QDoubleSpinBox()
            double_spin_box.setMaximum(1e20)  # 设置最大值
            double_spin_box.setDecimals(6)  # 设置保留小数位数
            double_spin_box.setValue(item_data["default"])
            double_spin_box.valueChanged.connect(
                lambda value, item=item: self.on_float_changed(item, value))
            self.setItemWidget(item, 1, double_spin_box)
        elif item_data["type"] == "bool":
            # 如果是布尔类型，创建一个 QCheckBox（复选框）
            check_box = QCheckBox()
            check_box.setChecked(item_data["default"])
            check_box.stateChanged.connect(
                lambda state, item=item: self.on_bool_changed(item, state))
            self.setItemWidget(item, 1, check_box)
        elif item_data["type"] == "vector":
            # 如果是向量类型，创建一个 QLineEdit（文本框）
            line_edit = QLineEdit(",".join(map(str, item_data["default"])))
            line_edit.editingFinished.connect(
                lambda item=item, line_edit=line_edit: self.on_text_changed(item, line_edit))
            self.setItemWidget(item, 1, line_edit)

    def on_enum_changed(self, item, combo_box):
        """当下拉框选项改变时触发的槽函数"""
        selected_option = combo_box.currentText()  # 获取当前选中的选项
        print(f"树形项 '{item.text(0)}' 的选项已更改为: {selected_option}")

    def on_text_changed(self, item, line_edit):
        """当文本框内容改变时触发的槽函数"""
        new_value = line_edit.text()  # 获取当前文本
        print(f"树形项 '{item.text(0)}' 的文本已更改为: {new_value}")

    def on_int_changed(self, item, value):
        """当整数输入框值改变时触发的槽函数"""
        print(f"树形项 '{item.text(0)}' 的整数值已更改为: {value}")

    def on_float_changed(self, item, value):
        """当浮点数输入框值改变时触发的槽函数"""
        print(f"树形项 '{item.text(0)}' 的浮点数值已更改为: {value}")

    def on_bool_changed(self, item, state):
        """当复选框状态改变时触发的槽函数"""
        new_value = state == Qt.Checked  # 获取当前状态
        print(f"树形项 '{item.text(0)}' 的布尔值已更改为: {new_value}")

    def collect_current_values(self):
        """收集所有子节点的当前值"""
        def get_item_value(item):
            widget = self.itemWidget(item, 1)
            if isinstance(widget, QComboBox):
                return widget.currentText()
            elif isinstance(widget, QLineEdit):
                return widget.text()
            elif isinstance(widget, QSpinBox):
                return widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                return widget.value()
            elif isinstance(widget, QCheckBox):
                return widget.isChecked()
            return None

        def traverse_items(item):
            values = {}
            for i in range(item.childCount()):
                child = item.child(i)
                values[child.text(0)] = get_item_value(child)
            return values

        current_values = {}
        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            current_values.update(traverse_items(top_item))
        return current_values

    def save_current_values(self):
        """保存当前值到 current.json 文件"""
        self.current_values = self.collect_current_values()
        with open("template/current.json", "w", encoding="utf-8") as file:
            json.dump(self.current_values, file, indent=4, ensure_ascii=False)

    def load_current_values(self, values: dict):
        """加载当前值"""
        def set_item_value(item, value):
            widget = self.itemWidget(item, 1)
            if isinstance(widget, QComboBox):
                index = widget.findText(value)
                if index != -1:
                    widget.setCurrentIndex(index)
            elif isinstance(widget, QLineEdit):
                widget.setText(str(value))
            elif isinstance(widget, QSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QDoubleSpinBox):
                widget.setValue(value)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(value)

        def traverse_items(item, values):
            for i in range(item.childCount()):
                child = item.child(i)
                if child.text(0) in values:
                    set_item_value(child, values[child.text(0)])

        for i in range(self.topLevelItemCount()):
            top_item = self.topLevelItem(i)
            traverse_items(top_item, values)


class MainWindow(QWidget):
    def __init__(self, json_file_path):
        super().__init__()
        self.json_file_path = json_file_path
        self.setWindowTitle("JSON to UI")  # 设置窗口标题
        self.setGeometry(100, 100, 600, 400)  # 设置窗口大小和位置
        layout = QVBoxLayout()  # 创建一个垂直布局

        # 创建自定义标题
        title_label = QLabel("模型参数设置")
        title_label.setAlignment(Qt.AlignCenter)  # 标题居中对齐
        title_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # 创建树形控件
        self.tree_widget = EditableTreeWidget(json_file_path)
        layout.addWidget(self.tree_widget)

        # 设置窗口的主布局
        self.setLayout(layout)


if __name__ == "__main__":
    # 读取指定路径下的 JSON 文件
    json_file_path = "template/config.json"

    # 创建应用程序实例
    app = QApplication(sys.argv)

    # 创建主窗口实例
    window = MainWindow(json_file_path)
    window.show()  # 显示窗口

    # 运行应用程序
    sys.exit(app.exec())
