import math

from PyQt5.QtCore import QLine
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import *


class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
        super().__init__(parent)

        self.scene = scene

        # settings
        self._grid_size = 20
        self._grid_squares = self._grid_size * 5
        self._background_color = QColor("#383838")
        self._grid_color = QColor("#303030")
        self._grid_color_dark = QColor("#1b1b1b")
        self._grid_pen = QPen(self._grid_color)
        self._grid_pen_dark = QPen(self._grid_color_dark)

        self.view = None

        self.setBackgroundBrush(self._background_color)

    def setGrScene(self, width, height):
        self.setSceneRect(-width//2, -height//2, width, height)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # draw grid

        # > compute all lines to be drawn
        lines_light, lines_dark = [], []
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - left % self._grid_size
        first_top = top - top % self._grid_size

        for x in range(first_left, right, self._grid_size):
            if x % self._grid_squares == 0:
                lines_dark.append(QLine(x, top, x, bottom))
            else:
                lines_light.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self._grid_size):
            if y % self._grid_squares == 0:
                lines_dark.append(QLine(left, y, right, y))
            else:
                lines_light.append(QLine(left, y, right, y))

        # > use pen to draw lines
        painter.setPen(self._grid_pen)
        painter.drawLines(*lines_light)
        painter.setPen(self._grid_pen_dark)
        painter.drawLines(*lines_dark)
