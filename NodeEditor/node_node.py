from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor, QBrush

import node_socket
from node_content_widget import QDMContentWidget
from node_graphics_node import QDMGraphicsNode
from node_socket import Socket
import node_socket_common as socket_types
import node_socket_states as socket_states_types


class Node:
    def __init__(self, scene):
        self.scene = scene

        self.title = ""
        self.initTitle()

        self.sockets = []
        self.initSockets()

        self.content = None
        self.create_content()

        self.grNode = None
        self.create_graphics()

        self.scene.addNode(self)

        self.grNode.initSockets()

    def create_content(self):
        self.content = QDMContentWidget(self)

    def create_graphics(self):
        self.grNode = QDMGraphicsNode(self)

    def initTitle(self):
        self.title = "Untitled Node"

    def initSockets(self):
        self.sockets.append(socket_states_types.StateFlowSocket(self, "states_up", [0.5, 0], position=node_socket.INPUT))
        self.sockets.append(socket_states_types.StateFlowSocket(self, "states_down", [0.5, 1], position=node_socket.OUTPUT))
        self.sockets.append(socket_types.FlowSocket(self, "flow_in"))
        self.sockets.append(socket_types.FlowSocket(self, "flow_out", position=node_socket.OUTPUT))
        self.sockets.append(socket_types.StringSocket(self, "text_in", position=node_socket.INPUT))
        self.sockets.append(socket_types.StringSocket(self, "text_out", position=node_socket.OUTPUT))

    def find_socket(self, identifier):
        for socket in self.sockets:
            if socket.identifier == identifier:
                return socket
        print("socket not found: {0}".format(identifier))
        return None

    def is_linked(self):
        for socket in self.sockets:
            if socket.is_linked():
                return True
        return False

    @property
    def position(self):
        return self.grNode.pos()

    def setPosition(self, x, y):
        self.grNode.setPos(x, y)

    def update_linked_sockets(self):
        for socket in self.sockets:
            if socket.is_linked():
                for link in socket.links:
                    link.update_positions()

    def get_index(self):
        return self.scene.nodes.index(self)

    @classmethod
    def get_preview(cls, w, h):
        pixmap = QPixmap(w, h)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter()
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        brush = QBrush()
        brush.setColor(QColor(255, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        painter.begin(pixmap)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawRect(2, 2, w - 4, h - 4)
        painter.end()
        return pixmap

    @classmethod
    def get_type_name(cls):
        return "Node"

    def get_save_text(self):
        save = "type:{0} x:{1} y:{2} ".format(self.__class__.get_type_name(), self.position.x(), self.position.y())
        return save

    def load_save_text(self, properties: dict):
        print(properties)
        x = float(properties["x"])
        y = float(properties["y"])
        print("loading position x:{0} y:{1}".format(x, y))
        self.setPosition(x, y)

    def __str__(self):
        return "Node[{0}] : '{1}'".format(self.get_index(), self.title)