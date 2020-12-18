import sys

from node_add_item_window import AddItemWindow
from node_link import Link
from node_node import Node
from node_scene import Scene
import os
from os import path


def serialize_scene(scene: Scene, filename: str):
    # verify if the file already exists
    if path.exists(filename):
        # file exists, so the old copy is destroyed
        os.remove(filename)
    # start writing to file
    file = open(filename, "wt")
    print("file created, saving nodes")
    # serialize nodes
    for node in scene.nodes:
        file.write("ADD_NODE " + node.get_save_text() + os.linesep)
    print("saving links")
    # serialize links
    for link in scene.links:
        file.write("ADD_LINK " + link.get_save_text() + os.linesep)
    print("saved data, closing file")
    file.close()


def deserialize_node(scene: Scene, data: str):
    args = data.split(" ")
    node_type = ""
    for arg in args:
        if arg.startswith("type:"):
            node_type = arg.split(":")[1]
    if node_type == "":
        return
    node = None
    for cls in Node.__subclasses__():
        if cls.get_type_name() == node_type:
            node = cls(scene)
            break
    print(node)
    if node is not None:
        properties = {}
        for arg in args:
            if ":" in arg:
                key = arg.split(":")[0]
                value = arg.split(":")[1]
                properties[key] = value
        node.load_save_text(properties)
    print("deserialized node")


def deserialize_link(scene: Scene, data: str):
    args = data.split(" ")
    properties = {}
    for arg in args:
        if ":" in arg:
            key = arg.split(":")[0]
            value = arg.split(":")[1]
            properties[key] = value
    input_node = None
    input_socket = None
    output_node = None
    output_socket = None
    input_node = scene.nodes[int(properties["input"].split(".")[0])]
    input_socket = input_node.find_socket(properties["input"].split(".")[1])
    output_node = scene.nodes[int(properties["output"].split(".")[0])]
    output_socket = output_node.find_socket(properties["output"].split(".")[1])
    print(input_socket, output_socket)
    link = output_socket.connect(input_socket)
    if link is not None:
        link.load_save_text(properties)
    link = input_socket.connect(output_socket)
    if link is not None:
        link.load_save_text(properties)


def deserialize_scene(filename: str):
    scene = Scene()
    file = open(filename, "rt")
    lines = file.readlines()
    file.close()
    print("file opened")
    for line in lines:
        print(line)
        if line.startswith("ADD_NODE"):
            deserialize_node(scene, line)
        elif line.startswith("ADD_LINK"):
            deserialize_link(scene, line)
    return scene
