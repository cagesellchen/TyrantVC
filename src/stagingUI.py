from maya import OpenMayaUI as omui
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
#import git_access

def get_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)
    
class TyrantVCStagingUI(QMainWindow):    
    # The name of the object for this panel, used to identify it by Maya

    
    def __init__(self, project_name, file_list, parent=None):
       super(TyrantVCStagingUI, self).__init__(parent)
  
       self.setWindowTitle(project_name + ' Commit')
       central_widget = QWidget()
       main_layout = QVBoxLayout()
       
       #File List
       self.file_list = QListWidget()
       self.file_list.label = QLabel("Select Files to Commit:")
       main_layout.addWidget(self.file_list.label)
       main_layout.addWidget(self.file_list)
       for f in file_list:
           qlw.setCheckState(Qt.Checked)
           self.file_list.addItem(qlw)
           
       
       #Commit Message
       self.commit_msg = QPlainTextEdit()
       self.commit_msg.label = QLabel("Enter Commit Message:")
       main_layout.addWidget(self.commit_msg.label)
       main_layout.addWidget(self.commit_msg)
       
       #Commit Button
       self.commit_btn = QPushButton()
       self.commit_btn.setText('Commit')
       self.commit_btn.clicked.connect(self.on_commit_btn_click)
       main_layout.addWidget(self.commit_btn)
       
       
       central_widget.setLayout(main_layout)
       self.setCentralWidget(central_widget)
       
    def on_commit_btn_click(self):
        if (self.commit_msg.toPlainText() == ""):
            print ("NO MESSAGE")
        else:
            print ("PRETEND THIS COMMITTED SOMETHING!")
            git_access.commit(".", self.commit_msg.toPlainText())
            self.close()
            
    # Sets up the panel and displays it. Should be called after creation
    def run(self):
        self.show()
        self.raise_()
        
    def delete_instances(self):     
        self.deleteLater()

def main(project_path):
    global main_panel
    main_panel = TyrantVCStagingUI(project_name = project_path,
        file_list = git_access.get_files_changed(),
        parent=get_main_window())
    main_panel.run()
    return main_panel

#if __name__ == '__main__':
#    main("n/a")