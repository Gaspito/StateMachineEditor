from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon

import node_link
from node_socket import Socket, INPUT, OUTPUT


class FlowSocket(Socket):
    def get_color_hash(self): return "#dedede"

    def get_socket_type(self): return "common.flow"

    def on_paint(self, painter, rect):
        x, y, w, h = rect
        polygon = QPolygon([
            QPoint(x+w*0.25, y+h+0.2),
            QPoint(x+w, y+h/2),
            QPoint(x+w*0.25, y-0.2)
        ])

        painter.drawPolygon(polygon)

    def connect(self, other_socket):
        print("connecting {0} with {1} ".format(self, other_socket))
        if self.can_connect_to(other_socket) and self.position is OUTPUT:
            self.disconnect()
            return node_link.Link(self.scene.grScene.scene, other_socket, self, node_link.BEZIER_LINK)
        return None


class StringSocket(Socket):
    def get_color_hash(self): return "#b85ed7"
    def get_socket_type(self): return "common.string"
    def can_connect_to(self, other_socket): return other_socket.position != self.position


class FloatSocket(Socket):
    def get_color_hash(self): return "#408eea"
    def get_socket_type(self): return "common.float"


class IntSocket(Socket):
    def get_color_hash(self): return "#4c2ed1"

    def get_socket_type(self): return "common.int"

    def can_connect_to(self, other_socket):
        return (other_socket.get_socket_type() == self.get_socket_type() \
               or other_socket.get_socket_type() == "common.float") \
               and other_socket.position != self.position