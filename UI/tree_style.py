from PySide6 import QtWidgets

class TreeStyle:
    @staticmethod
    def get_style():
        return {
            "tree_widget": """
                QTreeWidget {
                    font-family: "Microsoft YaHei", Arial;
                    font-size: 12px;
                    border: 1px solid #d0d0d0;
                    background-color: white;
                    padding: 5px;
                }
                QTreeWidget::item {
                    height: 30px;
                    color: #333333;
                    padding: 2px;
                }
                QTreeWidget::item:hover {
                    background-color: #e6f3ff;
                }
                QTreeWidget::item:selected {
                    background-color: #0078d7;
                    color: white;
                }
                QHeaderView::section {
                    background-color: #f0f0f0;
                    padding: 5px;
                    border: 1px solid #d0d0d0;
                    font-weight: bold;
                }
                QLineEdit {
                    padding: 3px;
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    background-color: #ffffff;
                }
                QLineEdit:focus {
                    border: 1px solid #0078d7;
                    background-color: #f8f8f8;
                }
            """,
            
            "save_button": """
                QPushButton {
                    padding: 8px 16px;
                    background-color: #0078d7;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1084e3;
                }
                QPushButton:pressed {
                    background-color: #006abc;
                }
            """,
            
            "line_edit": """
                QLineEdit {
                    margin: 2px;
                    padding: 3px;
                }
            """
        }

    @staticmethod
    def apply_tree_style(tree_widget):
        """应用树形控件的基本设置"""
        # 设置样式
        tree_widget.setStyleSheet(TreeStyle.get_style()["tree_widget"])
        
        # 隐藏表头
        tree_widget.setHeaderHidden(True)
        
        # 设置列宽自动调整
        tree_widget.header().setStretchLastSection(True)  # 最后一列自动填充
        tree_widget.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # 第一列自适应内容
        
        # 启用工具提示
        tree_widget.setToolTipDuration(5000)
        tree_widget.setMouseTracking(True)
        
        # 设置交替行颜色
        tree_widget.setAlternatingRowColors(True)