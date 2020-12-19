import sys
import PyQt5
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from node_editor_wnd import NodeEditorWnd

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    PyQt5.QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

IS_THIRD_PARTY = False

if __name__ == '__main__':
    print("Running Node Editor...")

    args = sys.argv
    if len(args) > 0:
        print("\trunning with arguments: {0}".format(args))
        if "thirdpartycontrol" in args:
            IS_THIRD_PARTY = True
            print("Control lend to third party application")
            print("Use command lines to use the editor")

    app = QApplication(sys.argv)

    NodeEditorWnd.IS_THIRD_PARTY = IS_THIRD_PARTY
    wnd = NodeEditorWnd()

    sys.exit(app.exec_())