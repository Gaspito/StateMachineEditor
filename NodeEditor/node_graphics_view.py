from PyQt5.QtCore import Qt, QEvent, QPointF
from PyQt5.QtGui import QPainter, QMouseEvent
from PyQt5.QtWidgets import QGraphicsView
from PyQt5.uic.properties import QtGui

import node_link
import node_socket
from node_add_item_window import AddItemWindow
from node_graphics_link import QDMGraphicsLink
from node_graphics_node import QDMGraphicsNode
from node_graphics_socket import QDMGraphicsSocket
from node_link import Link
from node_node import Node

DEBUG = False


STATE_NORMAL = 1
STATE_DRAG_LINK = 2


class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.grScene = grScene
        self.grScene.view = self

        self.zoomInFactor = 1.25
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [5, 20]
        self.zoomClamp = True

        self.mousePosition = QPointF()

        self.dragLink = None

        self.state = STATE_NORMAL

        self.initUI()

        self.setScene(self.grScene)

    def initUI(self):
        self.setRenderHint(QPainter.Antialiasing)
        self.setRenderHint(QPainter.HighQualityAntialiasing)
        self.setRenderHint(QPainter.TextAntialiasing)
        self.setRenderHint(QPainter.SmoothPixmapTransform)

        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        self.on_add_item_drag_enter(event)
        cursor_pos = self.mapToScene(event.pos())
        self.mousePosition = cursor_pos
        if self.state == STATE_DRAG_LINK:
            self.dragLink.update_positions()
        super().mouseMoveEvent(event)

    def leftMouseButtonPress(self, event):
        # print("Left mouse button pressed")
        # print("Mouse position: {0}".format( self.mapToScene( event.pos())))
        if event.modifiers() & Qt.CTRL:
            releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(), Qt.MiddleButton,
                                       Qt.NoButton, event.modifiers())
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(), Qt.LeftButton,
                                    event.buttons(), event.modifiers())
            super().mousePressEvent(fakeEvent)
            return

        self.last_lmb_position = self.mapToScene(event.pos())

        target = self.get_item_at_cursor(event)
        if type(target) is QDMGraphicsSocket:
            if self.state == STATE_NORMAL:
                self.begin_drag_link(target.socket)
                return

        if self.state == STATE_DRAG_LINK:
            if type(target) is QDMGraphicsSocket:
                self.end_drag_link(target.socket)
            else:
                self.end_drag_link()
                return

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        self.accept_add_item_drop(event)

        if event.modifiers() & Qt.CTRL:
            self.setDragMode(QGraphicsView.NoDrag)
            super().mouseReleaseEvent(event)
            return

        if self.state == STATE_DRAG_LINK:
            if self._mouse_released_on_socket(event): return

        super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        return super().mousePressEvent(event)

    def middleMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        if DEBUG:
            item = self.get_item_at_cursor(event)
            if item is None:
                print("RMB DEBUG SCENE:")
                print("\tNodes:")
                for node in self.grScene.scene.nodes: print("\t\t{0}".format(node))
                print("\tLinks:")
                for link in self.grScene.scene.links: print("\t\t{0}".format(link))
            elif type(item) is QDMGraphicsSocket:
                print("RMB DEBUG Socket: {0}".format(item.socket))
            elif type(item) is QDMGraphicsNode:
                print("RMB DEBUG Node: {0}".format(item.node))
            elif isinstance(item, QDMGraphicsLink):
                print("RMB DEBUG Link: {0}".format(item.link))
            else:
                print("RMB DEBUG item: {0}".format(item))
        return super().mousePressEvent(event)

    def rightMouseButtonRelease(self, event):
        return super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_out_factor = 1 / self.zoomInFactor

        # compute zoom factor
        if event.angleDelta().y() > 0:
            zoom_factor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoomStep

        if self.zoomClamp:
            if self.zoom < self.zoomRange[0]:
                self.zoom = self.zoomRange[0]
                zoom_factor = 0
            elif self.zoom > self.zoomRange[1]:
                self.zoom = self.zoomRange[1]
                zoom_factor = 0

        # set scene scale
        if zoom_factor != 0:
            self.scale(zoom_factor, zoom_factor)
            # print("Zoom: {0}".format(self.zoom))

    def get_item_at_cursor(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        print("Object at cursor: {0}".format(obj))
        return obj

    def begin_drag_link(self, socket):
        self.state = STATE_DRAG_LINK
        if DEBUG: print("Begin drag link")
        if socket is not None:
            if DEBUG: print("\t assigned socket: {0}".format(socket))
            socket_in = socket if socket.position is node_socket.INPUT else None
            socket_out = socket if socket.position is node_socket.OUTPUT else None
            if DEBUG: print(socket_in, socket_out)
            self.dragLink = Link(self.grScene.scene, socket_in, socket_out)
            if DEBUG: print(self.dragLink)
            if DEBUG: print("drag link begun")

    def end_drag_link(self, socket=None):
        self.state = STATE_NORMAL
        if DEBUG: print("End drag link")
        if socket is not None:
            if DEBUG: print("\t assigned socket: {0}".format(socket))
            dragged_socket = self.dragLink.socketOut if self.dragLink.socketOut is not None else self.dragLink.socketIn
            other_socket = socket
            dragged_socket.connect(other_socket)
            other_socket.connect(dragged_socket)
        self.dragLink.remove()
        self.dragLink = None

    def _mouse_released_on_socket(self, event):
        new_lmb_position = self.mapToScene(event.pos())
        lmp_delta = (new_lmb_position - self.last_lmb_position)
        lmp_sqr_dist = lmp_delta.x() * lmp_delta.x() + lmp_delta.y() * lmp_delta.y()
        mouse_threshold = 1.0
        if lmp_sqr_dist >= mouse_threshold * mouse_threshold:
            target = self.get_item_at_cursor(event)
            if type(target) is QDMGraphicsSocket:
                self.end_drag_link(target.socket)
                return True
            self.end_drag_link()
        return False

    def on_add_item_drag_enter(self, event):
        pass
        #if AddItemWindow.DRAG_ITEM is not None:
        #    print("Dragged item enter")

    def accept_add_item_drop(self, event):
        drop = AddItemWindow.DRAG_ITEM
        if drop is not None:
            print("Accepted drop item {0}".format(AddItemWindow.DRAG_ITEM))
            if drop is Node or issubclass(drop, Node):
                newNode = drop(self.grScene.scene)
                cursorPos = self.mapToScene(event.pos())
                newNode.setPosition(cursorPos.x(), cursorPos.y())
                AddItemWindow.DRAG_ITEM = None
