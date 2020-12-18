from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPainterPath, QPixmap, QPainter, QPen, QBrush

from node_content_widget import QDMContentWidget
from node_graphics_node import QDMGraphicsNode
from node_node import Node
from node_socket_states import StateFlowSocket
from nodes.QLabelEdit import QLabelEdit


class NodeEvent(Node):
    def __init__(self, scene):
        super().__init__(scene)
        self.name = "New Event"

    def initTitle(self):
        self.title = "Event"

    def initSockets(self):
        self.sockets.append(StateFlowSocket(self, "flow_up", [0.5, 0]))
        self.sockets.append(StateFlowSocket(self, "flow_up_2", [0.4, 0]))
        self.sockets.append(StateFlowSocket(self, "flow_up_3", [0.6, 0]))
        self.sockets.append(StateFlowSocket(self, "flow_down", [0.5, 1]))
        self.sockets.append(StateFlowSocket(self, "flow_down_2", [0.4, 1]))
        self.sockets.append(StateFlowSocket(self, "flow_down_3", [0.6, 1]))
        self.sockets.append(StateFlowSocket(self, "flow_left", [0, 0.5]))
        self.sockets.append(StateFlowSocket(self, "flow_left_2", [0, 0.3]))
        self.sockets.append(StateFlowSocket(self, "flow_left_3", [0, 0.7]))
        self.sockets.append(StateFlowSocket(self, "flow_right", [1, 0.5]))
        self.sockets.append(StateFlowSocket(self, "flow_right_2", [1, 0.3]))
        self.sockets.append(StateFlowSocket(self, "flow_right_3", [1, 0.7]))

    def create_content(self):
        self.content = _NodeEventContent(self)

    def create_graphics(self):
        self.grNode = _NodeEventGraphics(self)

    def set_name(self, text):
        self.name = text

    @classmethod
    def get_preview(cls, w, h):
        pixmap = QPixmap(w, h)
        pixmap.fill(QColor(0, 0, 0, 0))
        painter = QPainter()
        pen = QPen(QColor(0, 0, 0, 255))
        pen.setWidth(2)
        brush = QBrush()
        brush.setColor(QColor("#c0753f"))
        brush.setStyle(Qt.SolidPattern)
        painter.begin(pixmap)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(2, 10, w-4, h-20)
        painter.end()
        return pixmap

    @classmethod
    def get_type_name(cls):
        return "Event"

    def get_save_text(self):
        return super().get_save_text() + "name:{0}".format(self.name.replace(" ", "_"))

    def load_save_text(self, properties: dict):
        super().load_save_text(properties)
        if "name" in properties.keys():
            self.name = properties["name"]
            self.content.refresh()


class _NodeEventContent(QDMContentWidget):
    def __init__(self, parent):
        self.name_edit = None
        super().__init__(parent)
        self.setFixedWidth(200 - 20)
        self.setFixedHeight(50 - 20)

    def init_content(self):
        for socket in self.node.sockets:
            self.addSocket(socket)
        self.name_edit = QLabelEdit()
        if type(self.node) is NodeEvent:
            self.name_edit.setCallback(self.node.set_name)
        self.name_edit.setText("Name")
        self.name_edit.setFixedWidth(200 - 20)
        self.name_edit.setAlignment(Qt.AlignCenter)
        self.name_edit.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.name_edit)

    def refresh(self):
        self.name_edit.setText(self.node.name)


class _NodeEventGraphics(QDMGraphicsNode):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)
        self.width = 200
        self.height = 75
        self.title_item.setDefaultTextColor(QColor(255, 255, 255, 100))
        self.title_item.setFont(QFont("Arial", 8, QFont.StyleItalic))
        self.title_item.setX(80)
        self._disconnected_brush = QBrush(QColor("#71a0e2"))

    def get_background_color(self):
        return "#c0753f"

    def has_input(self):
        for socket in self.node.sockets:
            for link in socket.links:
                if link.socketIn == socket:
                    return True
        return False

    def paint(self, painter, option, widget=None):
        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addEllipse(0, 0, self.width, self.height)
        painter.setPen(Qt.NoPen)
        brush = self._background_brush if self.has_input() or not self.node.is_linked() else self._disconnected_brush
        painter.setBrush(brush)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addEllipse(0, 0, self.width, self.height)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

