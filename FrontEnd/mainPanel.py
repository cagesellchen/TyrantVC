from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from maya import cmds as cmds
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance



def get_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)
    
class TyrantVCMainPanel(MayaQWidgetDockableMixin, QMainWindow):
    # The name of the object for this panel, used to identify it by Maya
    OBJECT_NAME = 'TyrantVCMainPanel'
    # The name of the workspace control associated with this panel
    WORKSPACE_NAME = OBJECT_NAME + 'WorkspaceControl'
    
    def __init__(self, parent=None):
        self.delete_instances()
        
        super(TyrantVCMainPanel, self).__init__(parent)
        
        ### UI section
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        tab_widget = QTabWidget()
        files_tab_widget = QWidget()
        commits_tab_widget = QWidget()
        
        # TODO: Insert things into the files and commits widgets here
        
        tab_widget.addTab(files_tab_widget, 'Files')
        tab_widget.addTab(commits_tab_widget, 'Commits')
        main_layout.addWidget(tab_widget)
        
        self.commit_btn = QPushButton()
        self.commit_btn.setText('Commit')
        self.commit_btn.clicked.connect(self.on_commit_btn_click)
        main_layout.addWidget(self.commit_btn)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        self.setWindowTitle('TyrantVC')
        
        self.setAttribute(Qt.WA_DeleteOnClose)   

    # Called upon clicking the commit button, should open up the staging area window
    def on_commit_btn_click(self):
        print 'commit!'
        
    
    # Calls MEL workspaceControl command to check if the given
    # control exists, and if it does, closes and deletes it
    def delete_control(self, name):
        if cmds.workspaceControl(name, q=True, exists=True):
            cmds.workspaceControl(name, e=True, close=True)
            cmds.deleteUI(name, control=True)
    
    # Deletes lingering instances of the panel and its workspace
    # control -- Maya can't have multiple panels with the same name up.
    def delete_instances(self):
        
        # For now since we're docking automatically, it looks like we don't
        # need this cleanup step, we just need to delete the control.
        # However, we should keep this code around in case we change things
        # and end up needing it.
        
        #for obj in get_main_window().children():
        #    if(obj.__class__.__name__ == self.OBJECT_NAME):
        #        obj.setParent(None)
        #        obj.deleteLater()
                
        self.delete_control(self.WORKSPACE_NAME)
    
    # Sets up the panel and displays it. Should be called after creation        
    def run(self):
        self.setObjectName(self.OBJECT_NAME)
        
        self.show(dockable=True, area='right', floating=False)
        # Attach this to the outliner (-1 means append to the bottom)
        cmds.workspaceControl(self.WORKSPACE_NAME, e=True, ttc=['Outliner', -1], wp='preferred', mw=300)
        self.raise_()
        
        self.setDockableParameters(width=300)
        
            
def main():
    global mainPanel
    mainPanel = TyrantVCMainPanel(parent=get_main_window())
    mainPanel.run()
    return mainPanel
    

if __name__ == '__main__':
    main()
