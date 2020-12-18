from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout

import node_socket
from node_graphics_socket import QDMGraphicsSocket
from node_socket import Socket
from node_socket_widget import QDMSocketWidget


DEBUG = False


class QDMContentWidget(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.node = node
        self.socket_wdgs = []

        self.init_layout()
        self.init_content()

    def init_layout(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)

    def init_content(self):
        self.addSocket(self.node.find_socket("states_up"), "")
        self.addSocket(self.node.find_socket("states_down"), "")
        self.addSocket(self.node.find_socket("flow_in"), "Flow")
        self.addSocket(self.node.find_socket("flow_out"), "")
        self.add_space()
        self.wdg_label = QLabel("Text")
        self.layout.addWidget(self.wdg_label)
        self.addSocket(self.node.find_socket("text_in"), "")
        self.layout.addWidget(QTextEdit("Entry field"))
        self.addSocket(self.node.find_socket("text_out"), "")
        self.layout.addWidget(QLabel("Other Label field"))
        self.layout.addStretch()

    def add_space(self):
        self.layout.addSpacing(4)

    def addSocket(self, socket, label=""):
        wdg = QDMSocketWidget(socket)
        if len(label) > 0:
            label = QLabel(label)
            if socket.position == node_socket.OUTPUT:
                label.setAlignment(Qt.AlignRight)
            self.layout.addWidget(label)
        self.layout.addWidget(wdg)
        self.socket_wdgs.append(wdg)

    def drawSocketItems(self):
        if DEBUG: print("Node {0} drawing sockets...".format(self.node))
        for wdg in self.socket_wdgs:
            pos = wdg.getPosition()
            wdg.grSocket = QDMGraphicsSocket(wdg.socket, pos, self.node.grNode)
            if DEBUG: print("Socket {0} pos: {1}".format(wdg, pos))
        if DEBUG: print("done")
