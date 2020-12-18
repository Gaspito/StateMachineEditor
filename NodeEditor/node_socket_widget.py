from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

import node_socket


class QDMSocketWidget(QWidget):
    def __init__(self, socket, otherSocket=None, parent=None):
        super().__init__(parent)

        self.socket = socket

        self.setFixedHeight(0)

    def initUI(self):
        pass

    def getPosition(self):
        if self.socket.position == node_socket.INPUT:
            return [self.pos().x(),
                    self.pos().y() + self.socket.node.grNode.title_height]
        else:
            return [self.pos().x() + self.socket.node.grNode.width,
                    self.pos().y() + self.socket.node.grNode.title_height]
