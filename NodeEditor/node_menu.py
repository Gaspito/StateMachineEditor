import os

import node_serialization
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar, QFrame, QWidget, QHBoxLayout, QPushButton, QMenu, \
    QFileDialog, QDialog, QVBoxLayout, QLabel

from node_scene import Scene


class MainMenu(QWidget):
    def __init__(self, app, parent=None):
        super().__init__(parent)
        self.app = app
        self.layout = QHBoxLayout()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setFixedHeight(30)
        self.file_menu = QPushButton("File")
        self.file_menu.setFixedHeight(30)
        self.file_menu.clicked.connect(self.on_file_menu)
        self.layout.addWidget(self.file_menu)
        self.setLayout(self.layout)
        self.show()

    def on_file_menu(self):
        print("On File Menu")
        menu = QMenu(self)
        new_act = menu.addAction("New")
        new_act.triggered.connect(self.on_file_new)
        open_act = menu.addAction("Open")
        open_act.triggered.connect(self.on_file_open)
        save_act = menu.addAction("Save")
        save_act.triggered.connect(self.on_file_save)
        menu.exec_(self.mapToGlobal(self.file_menu.pos() + QPoint(0, 30)))

    def on_file_new(self):
        self.save_before_clear_dialog()
        scene = Scene()
        self.app.set_scene(scene)

    def on_file_save(self):
        scene = self.app.scene
        file = self.save_file_dialog()
        if file is None:
            return
        print("Saving to file: {0}".format(file))
        node_serialization.serialize_scene(scene, file)

    def on_file_open(self):
        self.save_before_clear_dialog()
        file = self.open_file_dialog()
        if file is None:
            return
        print("Opening file: {0}".format(file))
        scene = node_serialization.deserialize_scene(file)
        self.app.set_scene(scene)

    def save_before_clear_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("Save before clear")
        layout = QVBoxLayout()
        layout.addWidget(QLabel(text="Do you wish to save this scene before opening a new one?"))
        line = QHBoxLayout()
        accept = QPushButton(text="Yes, save")
        accept.clicked.connect(dialog.accept)
        accept.clicked.connect(self.on_file_save)
        line.addWidget(accept)
        cancel = QPushButton(text="No")
        cancel.clicked.connect(dialog.reject)
        line.addWidget(cancel)
        layout.addLayout(line)
        dialog.setLayout(layout)
        dialog.exec()

    def save_file_dialog(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Scene", os.path.dirname(__file__), "Scene File (*.nodes)")
        if filename:
            return filename
        return None

    def open_file_dialog(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self, "Open Scene", os.path.dirname(__file__), "Scene File (*.nodes)")
        if filename:
            return filename
        return None
