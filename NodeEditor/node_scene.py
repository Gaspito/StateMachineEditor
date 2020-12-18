import node_link
import node_node
from node_graphics_scene import QDMGraphicsScene


class Scene:
    def __init__(self):
        self.nodes = []
        self.links = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)
        self.grScene.addItem(node.grNode)

    def addLink(self, link):
        self.links.append(link)

    def removeNode(self, node: node_node.Node):
        for i in node.sockets:
            for link in i.links:
                self.removeLink(link)
            i.disconnect()
        self.nodes.remove(node)
        self.grScene.removeItem(node.grNode)
        del node

    def removeLink(self, link: node_link.Link):
        if link.socketIn is not None:
            link.socketIn.remove_link(link)
        if link.socketOut is not None:
            link.socketOut.remove_link(link)
        self.links.remove(link)
        self.grScene.removeItem(link.grLink)
        del link