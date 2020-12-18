from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QFont, QDrag, QCursor, QPixmap, QGuiApplication
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout

from node_node import Node


class QNodeItemFrame(QFrame):
    def __init__(self, node_type):
        super().__init__()
        self.node_type = node_type
        self.preview = None


class AddItemWindow(QWidget):

    DRAG_ITEM = None
    DEFAULT_PIXMAP = None

    def __init__(self, main_window):
        super().__init__()
        self.setParent(main_window)
        self.main_window = main_window
        self.setGeometry(0, 30, 200, 400)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        AddItemWindow.DEFAULT_PIXMAP = QPixmap("images/default_node.png")
        # title
        layout = QVBoxLayout()
        self.titleLabel = QLabel("Items")
        self.titleLabel.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.titleLabel)
        # items
        self.items = []
        self.init_items()
        for i in self.items:
            layout.addWidget(i)
        # final
        self.setLayout(layout)

    def add_item(self, item, item_name):
        frame = QNodeItemFrame(item)
        frame.setFrameStyle(QFrame.NoFrame)
        layout = QHBoxLayout()
        image = QLabel()
        image.setFixedWidth(50)
        image.setFixedHeight(50)
        frame.preview = item.get_preview(50, 50)
        image.setPixmap(frame.preview)
        image.setStyleSheet("{ }")
        layout.addWidget(image)
        label = QLabel(item_name)
        layout.addWidget(label)
        frame.setLayout(layout)
        self.items.append(frame)

    def init_items(self):
        from nodes.node_type_state import NodeState
        self.add_item(NodeState, "State")
        from nodes.node_type_event import NodeEvent
        self.add_item(NodeEvent, "Event")
        from nodes.node_type_test import NodeTest
        self.add_item(NodeTest, "Test")
        self.add_item(Node, "Action")
        self.add_item(Node, "Sub level")

    def drag_item(self, item_index):
        print("Begin Drag itemID: {0}".format(item_index))
        item = self.items[item_index].node_type
        print("item is {0}".format(item))
        AddItemWindow.DRAG_ITEM = item
        cursor = QCursor(self.items[item_index].preview)
        QGuiApplication.setOverrideCursor(cursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            for i in self.items:
                if i.underMouse():
                    self.drag_item(self.items.index(i))
                    break
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if AddItemWindow.DRAG_ITEM is not None:
            self.main_window.view.on_add_item_drag_enter(event)

    def mouseReleaseEvent(self, event):
        if AddItemWindow.DRAG_ITEM is not None:
            self.main_window.view.accept_add_item_drop(event)
            QGuiApplication.restoreOverrideCursor()
