from maya import OpenMayaUI as omui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance


def get_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)

# When created, this class opens a popup window which displays text
class TyrantVCTextViewerPanel(QMainWindow):
   
    def __init__(self, window_title, text_to_display, callback, parent=None):
        super(TyrantVCTextViewerPanel, self).__init__(parent)

        self.callback = callback
        self.setWindowTitle(window_title)
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Text Viewer
        self.text_viewer = QPlainTextEdit()
        self.text_viewer.setPlainText(text_to_display)
        self.text_viewer.setReadOnly(True)
        main_layout.addWidget(self.text_viewer)

        # Apply the layout to the central widget
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    # Sets up the panel and displays it. Should be called after creation
    def run(self):
        self.show()
        self.raise_()

    # Deletes instances of this
    def delete_instances(self):
        self.close()


def main(window_title, text_to_display, callback):
    # Create text viewer
    global text_viewer
    text_viewer = TyrantVCTextViewerPanel(window_title = window_title,
                                   text_to_display=text_to_display,
                                   callback=callback,
                                   parent=get_main_window())
    text_viewer.run()
    return text_viewer

# This is called if text_viewer_UI is run on its own 
if __name__ == '__main__':
    main("")