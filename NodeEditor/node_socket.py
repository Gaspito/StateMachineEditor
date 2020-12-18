import node_link
from node_graphics_socket import QDMGraphicsSocket

DEBUG = False
INPUT = 1
OUTPUT = 2


class Socket:
    def __init__(self, node, identifier, position=INPUT):
        self.node = node
        self.scene = node.scene
        self.identifier = identifier
        self.position = position

        self.links = []

        self.grSocket = None
        if DEBUG: print("socket created : {0}".format(self))

    def get_color_hash(self):
        return "#27d87d"

    def on_paint(self, painter, rect):
        x, y, w, h = rect
        painter.drawEllipse(x, y, w, h)

    def get_socket_type(self):
        return "hidden.core"

    def can_connect_to(self, other_socket):
        if other_socket.get_socket_type() == self.get_socket_type()\
                and other_socket.position != self.position:
            return True
        else:
            return False

    def connect(self, other_socket):
        print("connecting {0} with {1} ".format(self, other_socket))
        if self.can_connect_to(other_socket) and self.position is INPUT:
            self.disconnect()
            return node_link.Link(self.scene.grScene.scene, self, other_socket, node_link.BEZIER_LINK)
        return None

    def set_link(self, link=None):
        self.links.append(link)

    def remove_link(self, link):
        if link in self.links:
            self.links.remove(link)
            #link.remove()

    def disconnect(self):
        if len(self.links) == 0:
            return
        print("disconnecting socket ", self)
        for link in self.links:
            self.remove_link(link)
        self.links.clear()

    def get_index(self):
        return self.node.sockets.index(self)

    def get_position(self):
        if DEBUG: print("Getting position of socket {0} of node {1} at index {3}, graphics item: {2}".format(
            self, self.node, self.grSocket, self.get_index()))

        return self.grSocket.get_position()

    def is_linked(self):
        return len(self.links) > 0

    def on_graphics_init(self):
        pass

    def __str__(self):
        return "Node[{0}].{1}({2})".format(self.node.get_index(), self.identifier, self.get_socket_type())