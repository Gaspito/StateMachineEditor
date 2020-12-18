import math

from PyQt5.QtCore import Qt, QPointF, QRect, QRectF
from PyQt5.QtGui import QPen, QColor, QPainterPath, QPolygon, QPolygonF, QBrush
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem


class QDMGraphicsLink(QGraphicsPathItem):
    def __init__(self, link, parent=None):
        super().__init__(parent)

        self.link = link

        self._color = QColor(self.get_color())
        self._shadow_color = QColor("#2a2a2a")
        self._selected_color = QColor("#f0a91b")
        self._width = 2.0
        self._shadow_width = 1.0
        self._pen = QPen(self._color)
        self._pen.setWidth(self._width)
        self._shadow_pen = QPen(self._shadow_color)
        self._shadow_pen.setWidth(self._width + self._shadow_width*2)
        self._selected_pen = QPen(self._selected_color)
        self._selected_pen.setWidth(self._width)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setZValue(-1)

        self._startPosition = [-100, 0]
        self._endPosition = [100, 400]

    def get_color(self):
        if self.link.socketOut is None: return "#f0a91b"
        return self.link.socketOut.get_color_hash()

    def set_start(self, x, y):
        self._startPosition = [x, y]

    def set_end(self, x, y):
        self._endPosition = [x, y]

    def get_start(self): return self._startPosition

    def get_end(self): return self._endPosition

    def boundingRect(self):
        x = min(self._startPosition[0], self._endPosition[0])
        y = min(self._startPosition[1], self._endPosition[1])
        w = max(self._startPosition[0], self._endPosition[0]) - x
        h = max(self._startPosition[1], self._endPosition[1]) - y
        return QRectF(x, y, w, h)

    def paint(self, painter, option, widget):
        # print("Begin Link Painting")
        self.updatePath()
        # print("\tpath updated")
        # draw shadow
        painter.setPen(self._shadow_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
        # draw color
        painter.setPen(self._pen if not self.isSelected() else self._selected_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
        # print("End Link Painting")

    def updatePath(self):
        raise NotImplemented("This method has to be overridden in a child class.")

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key_Backspace or event.key() == Qt.Key_Delete:
            self.link.scene.removeLink(self.link)

    def get_save_text(self):
        return ""

    def load_save_text(self, properties: dict):
        pass

    @classmethod
    def get_type_name(cls):
        return "Link"


class QDMGraphicsLinkDirect(QDMGraphicsLink):

    def updatePath(self):
        # print("\tbegin path creation at {0}".format(self._startPosition))
        path = QPainterPath(
            QPointF(self._startPosition[0], self._startPosition[1])
        )
        # print("\tpath created")
        path.lineTo(QPointF(self._endPosition[0], self._endPosition[1]))
        self.setPath(path)

    def paint(self, painter, option, widget):
        self.updatePath()
        _start = self.get_start()
        _end = self.get_end()
        _center = [(_start[0] + _end[0]) * 0.5, (_start[1] + _end[1]) * 0.5]
        _start_to_end = [_end[0] - _start[0], _end[1] - _start[1]]
        _dist = math.sqrt(_start_to_end[0] * _start_to_end[0] + _start_to_end[1] * _start_to_end[1])
        _dir = [_start_to_end[0] / _dist, _start_to_end[1] / _dist]
        _tan = [_dir[1], 0 - _dir[0]]
        _arrow_half_w = 5
        _arrow_h = 8
        _arrow = QPolygonF()
        _arrow.append(QPointF(_center[0] + _dir[0] * _arrow_h, _center[1] + _dir[1] * _arrow_h))
        _arrow.append(QPointF(_center[0] - _tan[0] * _arrow_half_w, _center[1] - _tan[1] * _arrow_half_w))
        _arrow.append(QPointF(_center[0] + _tan[0] * _arrow_half_w, _center[1] + _tan[1] * _arrow_half_w))
        _arrow.append(QPointF(_center[0] + _dir[0] * _arrow_h, _center[1] + _dir[1] * _arrow_h))
        # draw shadow
        painter.setPen(self._shadow_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
        painter.setBrush(QBrush(self._shadow_color))
        painter.drawPolygon(_arrow)
        # draw color
        painter.setPen(self._pen if not self.isSelected() else self._selected_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self._color if not self.isSelected() else self._selected_color))
        painter.drawPolygon(_arrow)

    @classmethod
    def get_type_name(cls):
        return "Direct"


class QDMGraphicsLinkBezier(QDMGraphicsLink):

    TANGENT = 100

    def updatePath(self):
        # print("\tbegin path creation")
        path = QPainterPath(
            QPointF(self._startPosition[0], self._startPosition[1])
        )
        # print("\tpath created")
        startTangent = [self._startPosition[0] + QDMGraphicsLinkBezier.TANGENT,
                        self._startPosition[1]]
        endTangent = [self._endPosition[0] - QDMGraphicsLinkBezier.TANGENT,
                        self._endPosition[1]]
        # print("\tpath tangents set")
        path.cubicTo(
            QPointF(startTangent[0], startTangent[1]),
            QPointF(endTangent[0], endTangent[1]),
            QPointF(self._endPosition[0], self._endPosition[1])
        )
        self.setPath(path)

    @classmethod
    def get_type_name(cls):
        return "Bezier"
