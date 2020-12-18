import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from node_editor_wnd import NodeEditorWnd

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

if __name__ == '__main__':
    print("Running Node Editor...")
    app = QApplication(sys.argv)

    wnd = NodeEditorWnd()

    sys.exit(app.exec_())