from maya import OpenMayaUI as omui
from maya import cmds as cmds
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import git_access

def get_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)
    
# TyrantVCStagingUI creates a popup which displays a list of files to commit, a window to enter a
# commit message, and a commit button.  Users can select or deselect files.
class TyrantVCStagingUI(QMainWindow):    
    
    def __init__(self, project_name, file_list, callback, parent=None):
       super(TyrantVCStagingUI, self).__init__(parent)
       
       self.callback = callback
       self.setWindowTitle(project_name + ' Commit')
       central_widget = QWidget()
       main_layout = QVBoxLayout()
       
       #Create File List
       self.file_list = QListWidget()
       self.file_list.label = QLabel("Select Files to Commit:")
       main_layout.addWidget(self.file_list.label)
       main_layout.addWidget(self.file_list)
       for f in file_list:
           qlw = QListWidgetItem(f)
           qlw.setCheckState(Qt.Checked)
           self.file_list.addItem(qlw)

       # Create Commit Message panel
       self.commit_msg = QPlainTextEdit()
       self.commit_msg.label = QLabel("Enter Commit Message:")
       main_layout.addWidget(self.commit_msg.label)
       main_layout.addWidget(self.commit_msg)
       
       #Create Commit Button
       self.commit_btn = QPushButton('Commit')
       self.commit_btn.clicked.connect(self.on_commit_btn_click)
       main_layout.addWidget(self.commit_btn)
       
       # Apply the main_layout
       central_widget.setLayout(main_layout)
       self.setCentralWidget(central_widget)


    # Called when the user clicks the commit button
    # Commits all the checked files, and closes the window
    def on_commit_btn_click(self):
        # No commit message
        if (self.commit_msg.toPlainText() == ""):
                  cmds.warning("Commit message is required")
        else:
            #Determine the selected files
            commit_list = []
            for i in range (0, self.file_list.count()):
                item = self.file_list.item(i)
                if (item.checkState() == Qt.Checked):
                    commit_list.append(item.text())

            # No files selected
            if commit_list == []:
                cmds.warning("Select at least one file to commit")
            else:
                # Commit the selected files
                git_access.commit(commit_list, self.commit_msg.toPlainText())
                self.callback()
                self.delete_instances()

    # Sets up the panel and displays it. Should be called after creation
    def run(self):
        self.show()
        self.raise_()

    # Deletes this staging_ui
    def delete_instances(self):
        self.close()


# Creates a stagin_UI from the given project_path and callback and returns it
def main(project_path, callback):
    # Create staging UI
    global staging_ui
    staging_ui = TyrantVCStagingUI(project_name = project_path,
        file_list = git_access.get_files_changed(),
        callback = callback,
        parent=get_main_window())
    staging_ui.run()
    return staging_ui


# Called if staging_ui is run independently
if __name__ == '__main__':
    main("")