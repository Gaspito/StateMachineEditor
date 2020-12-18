from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QFont, QPainterPath, QPen, QColor, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem, QGraphicsProxyWidget
from PyQt5.uic.properties import QtGui


class QDMGraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.node = node
        self.content = self.node.content

        self._title_color = Qt.white
        self._title_font = QFont("Arial", 12)

        self.width = 180
        self.height = 240
        self.edge_size = 10
        self.title_height = 24
        self._padding = 4

        self._pen_default = QPen(QColor(self.get_outline_color()))
        self._pen_selected = QPen(QColor("#e18b32"))
        self._title_brush = QBrush(QColor(self.get_title_color()))
        self._background_brush = QBrush(QColor(self.get_background_color()))

        self.initTitle()
        self.title = self.node.title

        # init content
        self.initContent()

        # init sockets
        #self.initSockets()

        self.setFlag(QGraphicsItem.ItemIsFocusable, True)

        self.initUI()

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height
        ).normalized()

    def initUI(self):
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setTextWidth(self.width - 2 * self._padding)
        self.title_item.setX(self._padding)

    def get_title_color(self):
        return "#954a4a"

    def get_background_color(self):
        return "#2b2b2b"

    def get_outline_color(self):
        return "#181818"

    def initSockets(self):
        self.content.drawSocketItems()

    def initContent(self):
        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2 * self.edge_size, self.height - 2 * self.edge_size - self.title_height)
        self.grContent.setWidget(self.content)

    @property
    def title(self): return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.title_item.setPlainText(self._title)

    def paint(self, painter, option, widget=None):
        # title
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size,
                           self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._title_brush)
        painter.drawPath(path_title.simplified())

        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height, self.width, self.height - self.title_height,
                                    self.edge_size, self.edge_size)
        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_brush)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.node.update_linked_sockets()

    def keyReleaseEvent(self, event):
        super().keyReleaseEvent(event)
        if not self.hasFocus():
            return
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.node.scene.removeNode(self.node)