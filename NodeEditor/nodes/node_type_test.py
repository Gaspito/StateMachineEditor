from PyQt5.QtCore import Qt, QPoint, QPointF
from PyQt5.QtGui import QPainterPath, QColor, QFont, QPixmap, QPainter, QPen, QBrush, QPolygonF
from PyQt5.QtWidgets import QLabel, QLineEdit, QGraphicsProxyWidget, QStyle, QWidget

import node_socket
from node_content_widget import QDMContentWidget
from node_graphics_link import QDMGraphicsLink, QDMGraphicsLinkDirect
from node_graphics_node import QDMGraphicsNode
from node_link import Link
from node_node import Node
from node_socket_states import StateFlowSocket
from nodes.QLabelEdit import QLabelEdit


class NodeTest(Node):
    def __init__(self, scene):
        self.name = "New_Test"
        super().__init__(scene)

    def initTitle(self):
        self.title = "Test"

    def initSockets(self):
        self.sockets.append(TestFlowSocket(self, "flow_up", [0.5, 0]))
        self.sockets.append(TestFlowSocket(self, "flow_up_2", [0.35, 0.15]))
        self.sockets.append(TestFlowSocket(self, "flow_up_3", [0.65, 0.15]))
        self.sockets.append(TestFlowSocket(self, "flow_down", [0.5, 1]))
        self.sockets.append(TestFlowSocket(self, "flow_down_2", [0.35, 0.85]))
        self.sockets.append(TestFlowSocket(self, "flow_down_3", [0.65, 0.85]))
        self.sockets.append(TestFlowSocket(self, "flow_left", [0, 0.5]))
        self.sockets.append(TestFlowSocket(self, "flow_left_2", [0.15, 0.35]))
        self.sockets.append(TestFlowSocket(self, "flow_left_3", [0.15, 0.65]))
        self.sockets.append(TestFlowSocket(self, "flow_right", [1, 0.5]))
        self.sockets.append(TestFlowSocket(self, "flow_right_2", [0.85, 0.35]))
        self.sockets.append(TestFlowSocket(self, "flow_right_3", [0.85, 0.65]))

    def create_content(self):
        self.content = _NodeTestContent(self)

    def create_graphics(self):
        self.grNode = _NodeTestGraphics(self)

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
        brush.setColor(QColor("#c84737"))
        brush.setStyle(Qt.SolidPattern)
        painter.begin(pixmap)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawConvexPolygon(QPoint(w * 0.5, 2), QPoint(w - 2, h * 0.5),
                                  QPoint(w * 0.5, h - 2), QPoint(2, h * 0.5))
        painter.end()
        return pixmap

    @classmethod
    def get_type_name(cls):
        return "Test"

    def get_save_text(self):
        return super().get_save_text() + "name:{0}".format(self.name.replace(" ", "_"))

    def load_save_text(self, properties: dict):
        super().load_save_text(properties)
        if "name" in properties.keys():
            self.name = properties["name"]
            self.content.refresh()


class _NodeTestContent(QDMContentWidget):
    def __init__(self, parent):
        self.name_edit = None
        super().__init__(parent)
        self.layout.setContentsMargins(0, 30, 0, 10)
        self.setFixedWidth(150 - 20)
        self.setFixedHeight(150 - 20 - 30)

    def init_content(self):
        for socket in self.node.sockets:
            self.addSocket(socket)
        self.name_edit = QLabelEdit()
        if type(self.node) is NodeTest:
            self.name_edit.setCallback(self.node.set_name)
        self.name_edit.setText("Name")
        self.name_edit.setFixedWidth(150 - 20)
        self.name_edit.setAlignment(Qt.AlignCenter)
        self.name_edit.setFont(QFont("Arial", 10))
        self.layout.addWidget(self.name_edit)

    def refresh(self):
        self.name_edit.setText(self.node.name)


class _NodeTestGraphics(QDMGraphicsNode):
    def __init__(self, node, parent=None):
        super().__init__(node, parent)
        self.width = 150
        self.height = 150
        self.title_item.setDefaultTextColor(QColor(255, 255, 255, 100))
        self.title_item.setFont(QFont("Arial", 8, QFont.StyleItalic))
        self.title_item.setX(60)
        self.title_item.setY(30)

    def get_title_color(self):
        return "#0e6ab8"

    def get_background_color(self):
        return "#c84737"

    def paint(self, painter, option, widget=None):
        # content
        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        polygon = QPolygonF()
        polygon.append(QPoint(self.width * 0.5, 2))
        polygon.append(QPoint(self.width - 2, self.height * 0.5))
        polygon.append(QPoint(self.width * 0.5, self.height - 2))
        polygon.append(QPoint(2, self.height * 0.5))
        polygon.append(QPoint(self.width * 0.5, 2))
        path_content.addPolygon(polygon)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._background_brush)
        painter.drawPath(path_content.simplified())

        # outline
        path_outline = QPainterPath()
        path_outline.addPolygon(polygon)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())


class TestFlowSocket(StateFlowSocket):
    def __init__(self, node, identifier, coords):
        super().__init__(node, identifier, coords, node_socket.OUTPUT)

    def get_color_hash(self): return "#d52a56"

    def get_socket_type(self): return "state.flow"

    def connect(self, other_socket: node_socket.Socket):
        # if the two sockets are not linked yet,
        # then a test flow link is needed, since the output node's "connect" method is called first.
        # otherwise, a regular test flow link will suffice

        if not other_socket.get_socket_type() == super().get_socket_type():
            return None
        print("print sockets have valid types")
        sockets_are_linked = False
        for link in other_socket.links:
            if link.socketIn == self or link.socketOut == self:
                sockets_are_linked = True
                break
        print("Are sockets linked: {0}".format(sockets_are_linked))
        if sockets_are_linked:
            return None

        if self.is_linked():
            self.disconnect()
        if other_socket.is_linked():
            other_socket.disconnect()
        print("Sockets have been disconnected from obsolete links")
        self.position = node_socket.OUTPUT
        other_socket.position = node_socket.INPUT
        print("Sockets have their positions valid")
        return Link(self.scene.grScene.scene, other_socket, self, TestLinkGraphics)

    def disconnect(self):
        super().disconnect()
        self.position = node_socket.OUTPUT


class QTestLinkProxy(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)


class TestLinkGraphics(QDMGraphicsLinkDirect):
    def __init__(self, link: Link, parent=None):
        super().__init__(link, parent)
        print("creating test link")
        self.name = "Outcome"
        self._widget_proxy = QGraphicsProxyWidget(self)
        self._widget = QTestLinkProxy()
        print("proxy widget created")
        self.name_edit = QLabelEdit(self._widget)
        self.name_edit.setCallback(self.set_name)
        self.name_edit.setText(self.name)
        self.name_edit.setFixedWidth(80)
        self.name_edit.setAlignment(Qt.AlignCenter)
        self.name_edit.setFont(QFont("Arial", 10))
        print("name edit initialized")
        _start = self.get_start()
        _end = self.get_end()
        _center = [(_start[0] + _end[0]) * 0.5, (_start[1] + _end[1]) * 0.5]
        _size = [80, 25]
        print("center position found")
        self._widget.setGeometry(_center[0] - _size[0] * 0.5, _center[1] - _size[1] * 0.5,
                                   _size[0], _size[1])
        print("name edit geometry set")
        self._widget_proxy.setWidget(self._widget)
        print("widget set to proxy")

    def updatePath(self):
        _start = self.get_start()
        _end = self.get_end()
        _center = [(_start[0] + _end[0]) * 0.5, (_start[1] + _end[1]) * 0.5]
        _size = [80, 20]
        self._widget.setGeometry(_center[0] - _size[0] * 0.5, _center[1] - _size[1] * 0.5,
                                   _size[0], _size[1])
        path = QPainterPath(
            QPointF(_start[0], _start[1])
        )
        _out_id = self.link.socketOut.identifier
        if "up" in _out_id or "down" in _out_id :
            path.lineTo(QPointF(_start[0], _center[1]))
        else:
            path.lineTo(QPointF(_center[0], _start[1]))
        path.lineTo(QPointF(_center[0], _center[1]))
        _in_id = self.link.socketIn.identifier
        if "up" in _in_id or "down" in _in_id:
            path.lineTo(QPointF(_end[0], _center[1]))
        else:
            path.lineTo(QPointF(_center[0], _end[1]))
        path.lineTo(QPointF(_end[0], _end[1]))
        self.setPath(path)

    @classmethod
    def get_type_name(cls):
        return "Test"

    def get_color(self):
        return "#d52a56"

    def set_name(self, text):
        self.name = text

    def get_save_text(self):
        data = super().get_save_text()
        data += "name:{0} ".format(self.name)
        return data

    def load_save_text(self, properties: dict):
        super().load_save_text(properties)
        if "name" in properties.keys():
            self.name = properties["name"]
            self.name_edit.setText(self.name)
