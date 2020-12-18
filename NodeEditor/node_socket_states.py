from PyQt5 import QtCore
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPolygon

import node_link
from node_socket import Socket, INPUT, OUTPUT


class StateFlowSocket(Socket):
    def __init__(self, node, identifier, coords, position=INPUT):
        super().__init__(node, identifier, position)

        self.coords = coords

    def get_color_hash(self): return "#ced1d1"

    def get_socket_type(self): return "state.flow"

    def on_graphics_init(self):
        # print("Init Graphics, Socket {0}".format(self.grSocket.pos))
        node_position = self.node.grNode.pos()
        node_width = self.node.grNode.width
        node_height = self.node.grNode.height

        x = node_position.x() + self.coords[0] * node_width
        y = node_position.y() + self.coords[1] * node_height

        self.grSocket.pos = [x, y]

    def on_paint(self, painter, rect):
        if self.is_linked():
            return
        from node_graphics_view import STATE_DRAG_LINK
        if self.node.grNode.isSelected() or \
                self.node.scene.grScene.view.state == STATE_DRAG_LINK:
            super().on_paint(painter, rect)

    def can_connect_to(self, other_socket):
        if other_socket.get_socket_type() == self.get_socket_type():
            return True
        else:
            return False

    def connect(self, other_socket):
        if other_socket.get_socket_type() == self.get_socket_type():
            if other_socket.is_linked():
                for link in self.links:
                    if link.socketIn == other_socket or link.socketOut == other_socket:
                        return
            self.disconnect()
            other_socket.disconnect()
            other_socket.position = INPUT
            self.position = OUTPUT
            return node_link.Link(self.scene.grScene.scene, other_socket, self, node_link.DIRECT_LINK)
        return None
