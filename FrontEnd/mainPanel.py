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
        
        
        self.button1 = QPushButton()
        self.button1.setText('PushMe')
        
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        self.setLayout(layout)
        self.setWindowTitle('TyrantVC')
        
        self.setAttribute(Qt.WA_DeleteOnClose)
    
    # Should be triggered automatically when the panel is closed
    #def dockCloseEventTriggered(self):
    #    self.delete_instances()
    
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
        cmds.workspaceControl(self.WORKSPACE_NAME, e=True, ttc=["AttributeEditor", -1], wp='preferred', mw=300)
        self.raise_()
        
        self.setDockableParameters(width=300)
        
            
def main():
    global mainPanel
    mainPanel = TyrantVCMainPanel(parent=get_main_window())
    mainPanel.run()
    return mainPanel
    

if __name__ == '__main__':
    main()
