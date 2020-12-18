from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QBoxLayout, QVBoxLayout, QHBoxLayout


class QLabelEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # print("Init Label Edit")
        self.text = "Enter Text"
        self.label = QLabel("Hello World", parent=self)
        self.label.setStyleSheet("{  }")
        self.line_edit = QLineEdit(parent=self)
        # print("Widgets added")
        self.label.show()
        self.line_edit.hide()
        # print("layout added")
        self.in_edit_mode = False
        self.on_edit_line = None
        # print("Label Edit Initiated")

    def setCallback(self, callback):
        self.on_edit_line = callback

    def setFixedWidth(self, w: int):
        super().setFixedWidth(w)
        self.label.setFixedWidth(w)
        self.line_edit.setFixedWidth(w)

    def setText(self, text):
        self.text = text
        self.label.setText(text)
        self.line_edit.setText(text)
        if self.on_edit_line is not None:
            self.on_edit_line(text)

    def beginEdit(self):
        if not self.in_edit_mode:
            self.setText(self.label.text())
            self.line_edit.show()
            self.label.hide()
            self.line_edit.setFocus()
            self.in_edit_mode = True

    def endEdit(self):
        if self.in_edit_mode:
            self.setText(self.line_edit.text())
            self.label.show()
            self.line_edit.hide()
            self.label.setFocus()
            self.in_edit_mode = False

    def setAlignment(self, alginment):
        self.label.setAlignment(alginment)
        self.line_edit.setAlignment(alginment)

    def setFont(self, font: QFont):
        self.label.setFont(font)
        self.line_edit.setFont(font)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.beginEdit()
        super().mousePressEvent(event)

    def leaveEvent(self, event):
        self.endEdit()
        super().leaveEvent(event)

    def set_label_style(self, style: str):
        self.label.setStyleSheet(style)

    def set_edit_stlye(self, style: str):
        self.line_edit.setStyleSheet(style)