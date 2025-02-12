from PySide6 import QtWidgets, QtGui, QtCore
from UI.tree_style import TreeStyle
import json


class EditableTreeWidget(QtWidgets.QWidget):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.data = json.load(open(self.path, 'r', encoding='utf-8'))
        self.init_ui()
        self.populate_tree(self.data)

    def init_ui(self):
        # Create main layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Create Tree Widget
        self.tree = QtWidgets.QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderHidden(True)
        
        # 设置列宽比例
        self.tree.header().setStretchLastSection(True)  # 最后一列自动填充剩余空间
        self.tree.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # 第一列根据内容调整
        
        # 应用样式
        TreeStyle.apply_tree_style(self.tree)
        
        layout.addWidget(self.tree)

        # Create Save Button
        save_button = QtWidgets.QPushButton('保存')
        save_button.setFixedWidth(120)
        save_button.setFixedHeight(35)
        save_button.setStyleSheet(TreeStyle.get_style()["save_button"])
        layout.addWidget(save_button, alignment=QtCore.Qt.AlignRight)
        save_button.clicked.connect(self.save_data)

        # Set layout to the main widget
        self.setLayout(layout)
        self.setWindowTitle('配置编辑器')
        self.resize(600, 500)

    def populate_tree(self, data, parent_item=None):
        for key, value in data.items():
            if isinstance(value, dict):
                item = QtWidgets.QTreeWidgetItem([key])
                if parent_item is None:
                    self.tree.addTopLevelItem(item)
                else:
                    parent_item.addChild(item)
                self.populate_tree(value, item)
            elif isinstance(value, list):
                item = QtWidgets.QTreeWidgetItem([key])
                if parent_item is None:
                    self.tree.addTopLevelItem(item)
                else:
                    parent_item.addChild(item)
                line_edit = QtWidgets.QLineEdit()
                line_edit.setText(json.dumps(value))
                line_edit.editingFinished.connect(
                    lambda item=item, line_edit=line_edit: self.update_data(item, line_edit))
                self.tree.setItemWidget(item, 1, line_edit)
            else:
                item = QtWidgets.QTreeWidgetItem([key])
                if parent_item is None:
                    self.tree.addTopLevelItem(item)
                else:
                    parent_item.addChild(item)
                line_edit = QtWidgets.QLineEdit()
                line_edit.setText(str(value))
                # line_edit.setStyleSheet(TreeStyle.get_style()["line_edit"])
                line_edit.editingFinished.connect(
                    lambda item=item, line_edit=line_edit: self.update_data(item, line_edit))
                self.tree.setItemWidget(item, 1, line_edit)
        
        # 展开所有节点
        self.tree.expandAll()

    def update_data(self, item, line_edit):
        keys = []
        while item is not None:
            keys.insert(0, item.text(0))
            item = item.parent()

        # 获取原始数据及其类型
        sub_data = self.data
        for key in keys[:-1]:
            sub_data = sub_data[key]
        
        original_value = sub_data[keys[-1]]
        new_value = line_edit.text()
        
        # 根据原始值的类型进行转换
        try:
            if isinstance(original_value, bool):
                # 处理布尔值
                new_value = new_value.lower() in ('true', '1', 'yes', 'on')
            elif isinstance(original_value, int):
                # 处理整数
                new_value = int(new_value)
            elif isinstance(original_value, float):
                # 处理浮点数
                new_value = float(new_value)
            elif isinstance(original_value, list):
                new_value = json.loads(new_value)
            # 如果是字符串类型，则不需要转换
            
            # 更新数据
            sub_data[keys[-1]] = new_value
            
        except ValueError as e:
            # 如果转换失败，恢复原值并显示错误消息
            line_edit.setText(str(original_value))
            QtWidgets.QMessageBox.warning(
                self,
                "类型错误",
                f"输入值必须与原始类型({type(original_value).__name__})匹配"
            )

    def save_data(self):
        # print(json.dumps(self.data, indent=4))
        json.dump(self.data, open(self.path, 'w',encoding='utf-8'), indent=4, ensure_ascii=False)
    def get_model_path(self):
        return self.data['model']['path']


if __name__ == "__main__":
    import sys

    # Example dictionary data
    json_path = "./input.json"
    data = json.load(open(json_path,'r',encoding='utf-8'))

    app = QtWidgets.QApplication(sys.argv)
    window = EditableTreeWidget(json_path)
    window.show()
    sys.exit(app.exec_())
