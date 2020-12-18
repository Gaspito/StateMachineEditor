from PyQt5.QtCore import Qt, QFile
from PyQt5.QtGui import QBrush, QPen, QColor, QFont
from PyQt5.QtWidgets import *

import node_link
from node_add_item_window import AddItemWindow
from node_graphics_scene import QDMGraphicsScene
from node_graphics_view import QDMGraphicsView
from node_link import Link
from node_menu import MainMenu
from node_node import Node
from node_scene import Scene
from node_socket import Socket


class NodeEditorWnd(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stylesheet_filename = 'qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)

        self.initUI()

    def initUI(self):
        self.setGeometry(200,300, 800, 600)

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        # create graphics scene
        self.scene = Scene()
        self.grScene = self.scene.grScene

        # create graphics view
        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)

        self.setWindowTitle("Node Editor")
        self.show()

        self.addNodes()

        self.addItemWindow = AddItemWindow(self)
        self.addItemWindow.show()

        self.menu_bar = MainMenu(self, self)

        #self.addDebugContent()

    def set_scene(self, scene):
        self.scene = scene
        self.grScene = self.scene.grScene
        self.layout.removeWidget(self.view)
        self.addItemWindow.close()
        self.menu_bar.close()
        self.view = QDMGraphicsView(self.grScene, self)
        self.layout.addWidget(self.view)
        for i in self.scene.links:
            i.update_positions()
        self.addItemWindow = AddItemWindow(self)
        self.addItemWindow.show()
        self.menu_bar = MainMenu(self, self)

    def addDebugContent(self):
        green_brush = QBrush(Qt.green)
        line_pen = QPen(Qt.black)
        line_pen.setWidth(2)
        rectangle = self.grScene.addRect(-100, -100, 80, 100, line_pen, green_brush)
        rectangle.setFlag(QGraphicsItem.ItemIsMovable)

        text = self.grScene.addText("H E L L O   M E T E O R", QFont("Arial"))
        text.setDefaultTextColor(QColor("#e3b0ac"))
        text.setFlag(QGraphicsItem.ItemIsMovable)
        text.setFlag(QGraphicsItem.ItemIsSelectable)

        widget1 = QPushButton("Push Me")
        proxy1 = self.grScene.addWidget(widget1)
        proxy1.setPos(0, -50)

        widget2 = QTextEdit("Edit me")
        proxy2 = self.grScene.addWidget(widget2)
        proxy2.setPos(0, 100)

        line = self.grScene.addLine(-100, -100, 400, 400, line_pen)
        line.setFlag(QGraphicsItem.ItemIsMovable)

    def loadStylesheet(self, filename):
        print("Loading STYLE: {0}".format(filename))
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))

    def addNodes(self):
        pass
