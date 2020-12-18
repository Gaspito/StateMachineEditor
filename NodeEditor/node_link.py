from PyQt5.QtGui import QCursor

from node_graphics_link import QDMGraphicsLinkDirect, QDMGraphicsLinkBezier
from node_socket import Socket

DIRECT_LINK = QDMGraphicsLinkDirect
BEZIER_LINK = QDMGraphicsLinkBezier


class Link:
    def __init__(self, scene, socketIn: Socket, socketOut: Socket, link_type=DIRECT_LINK):
        self.scene = scene
        self.socketIn = socketIn
        self.socketOut = socketOut

        if self.socketIn is not None: self.socketIn.set_link(self)
        if self.socketOut is not None: self.socketOut.set_link(self)

        self.grLink = link_type(self)

        self.update_positions()
        self.scene.addLink(self)
        self.scene.grScene.addItem(self.grLink)

    def remove_from_sockets(self):
        if self.socketIn is not None:
            self.socketIn.remove_link(self)

        if self.socketOut is not None:
            self.socketOut.remove_link(self)

    def remove(self):
        # print("Removing link {0} from it's sockets".format(self))
        self.remove_from_sockets()
        # print("Removed link {0} from it's sockets".format(self))
        self.scene.grScene.removeItem(self.grLink)
        self.grLink = None
        if self in self.scene.links: self.scene.removeLink(self)

    def update_positions(self):
        if self.scene.grScene.view is None:
            return
        cursor_position = self.grLink.mapFromScene(self.scene.grScene.view.mousePosition)
        # print("Cursor Position Found at {0}".format(cursor_position))
        if self.socketIn is not None:
            self.grLink.set_end(*self.socketIn.get_position())
        else:
            self.grLink.set_end(cursor_position.x(), cursor_position.y())
        if self.socketOut is not None:
            self.grLink.set_start(*self.socketOut.get_position())
        else:
            self.grLink.set_start(cursor_position.x(), cursor_position.y())
        self.grLink.update()

    def get_index(self):
        if self in self.scene.links:
            return self.scene.links.index(self)
        else:
            return -1

    def get_save_text(self):
        input_node = self.scene.nodes.index(self.socketIn.node)
        input_socket = self.socketIn.identifier
        output_node = self.scene.nodes.index(self.socketOut.node)
        output_socket = self.socketOut.identifier
        data = "type:{0} input:{1}.{2} output:{3}.{4} ".format(self.grLink.__class__.get_type_name(),
                                                               input_node, input_socket,
                                                               output_node, output_socket)
        data += self.grLink.get_save_text()
        return data

    def load_save_text(self, properties: dict):
        self.grLink.load_save_text(properties)

    def __str__(self):
        return "Link[{0}] : {1} -> {2}".format(self.get_index(), self.socketOut, self.socketIn)
