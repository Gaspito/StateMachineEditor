from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsItem


DEBUG = False


class QDMGraphicsSocket(QGraphicsItem):
    def __init__(self, socket, pos, parent=None):
        super().__init__(parent)
        self.socket = socket
        self.socket.grSocket = self
        if DEBUG: print("Socket Graphics Item Created for {0}".format(self.socket))

        self.radius = 6.0
        self._outline_width = 2.5
        self._background_color = QColor(socket.get_color_hash())
        self._outline_color = QColor("#2a2a2a")

        self._pen = QPen(self._outline_color)
        self._pen.setWidth(self._outline_width)
        self._brush = QBrush(self._background_color)

        self.pos = pos

        self.socket.on_graphics_init()

    def paint(self, painter, option, widget):
        painter.setPen(self._pen)
        painter.setBrush(self._brush)

        # paint circle
        #painter.drawEllipse(self.pos[0] - self.radius, self.pos[1] - self.radius/2,
        #                    self.radius * 2, self.radius * 2)

        rect = [self.pos[0] - self.radius, self.pos[1] - self.radius/2, self.radius * 2, self.radius * 2]
        self.socket.on_paint(painter, rect)

    def boundingRect(self):
        return QRectF(
            self.pos[0] - self.radius, self.pos[1] - self.radius/2,
            self.radius * 2, self.radius * 2
        )

    def get_position(self):
        return [self.pos[0]+self.socket.node.grNode.pos().x(),
                self.pos[1]+self.socket.node.grNode.pos().y()+self.radius/2]

    def on_clicked(self, event):
        if DEBUG: print("Socket {1} of type: {0} was clicked".format(self.socket.get_socket_type(),
                                                                     self.socket.identifier))