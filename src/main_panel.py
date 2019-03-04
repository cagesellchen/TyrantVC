from maya.app    .general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from maya import cmds as cmds
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import re
import git_access
import stagingUI


def get_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QWidget)
    
#TODO: Split into FileBrowserUI and CommitBrowserUI
class TyrantVCMainPanel(MayaQWidgetDockableMixin, QMainWindow):
    # The name of the object for this panel, used to identify it by Maya
    OBJECT_NAME = 'TyrantVCMainPanel'
    # The name of the workspace control associated with this panel
    WORKSPACE_NAME = OBJECT_NAME + 'WorkspaceControl'
    
    def __init__(self, parent=None):
        print "__init__"
        self.delete_instances()
        
        super(TyrantVCMainPanel, self).__init__(parent)
        
        ### Panels
        self.staging_ui = None
        
        ### UI section
        
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        self.project_button = QPushButton()
        self.project_menu = QMenu()
        self.project_list = None
        self.project_path = None
        self.project_name = None
        self.populate_project_menu()
     
     
     
        main_layout.addWidget(self.project_button)
        
        tab_widget = QTabWidget()
        files_tab_widget = QWidget()
        commits_tab_widget = QWidget()
        
        # TODO: Insert things into the files and commits widgets here
        file_layout = QVBoxLayout()
        self.file_model = QFileSystemModel()
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        file_layout.addWidget(self.file_tree)
        files_tab_widget.setLayout(file_layout)
        
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

    def populate_project_menu(self):
        print "populate_project_menu"
        self.project_menu.clear() 
        # TODO: here is where we call our config file wrapper and get the info...
        # it should return a list of tuples
        if self.project_list is None:
            self.project_list = []
            
        for item in self.project_list:
            self.project_menu.addAction(item[0], lambda t=item: self.project_menu_item_clicked(t))
            
        self.project_menu.addAction("Create new project...", self.create_new_project)
        self.project_button.setMenu(self.project_menu)
            
        self.project_button.setText("No Project Selected")
    
    # Called upon clicking a project in the project_list. Sets the button text       
    def project_menu_item_clicked(self, item):
        print "project_menu_item_clicked"
        
        self.project_button.setText(item[0])
        #TODO: refactor with create_new_project into set path method?
        self.project_name = item[0]
        self.project_path = item[1]
        
        self.file_model.setRootPath(item[1])
        self.file_tree.setRootIndex(self.file_model.index(self.project_path))
      
        git_access.load_repo(item[1])
    
    # Called upon clicking the create new project button
    def create_new_project(self):
        print "create_new_project"
        res = cmds.fileDialog2(fileMode=3, dialogStyle=2, okCaption='Accept', caption='Select Folder for Project')
        if res is None:
            # they cancelled the file picker
            return
        
        project_name = re.split(r'[/\\]', res[0])[-1]
        for item in self.project_list:
            print item[0]
            if (item[0] == project_name):
               cmds.warning("A project with name '" + item[0] + "' already exisits")
               return
            #    PySide.QtGui.QMessageBox QStatusBar.showMessage("Error: a project of this name already exists")
            #    return
        self.project_name = project_name
        self.project_path = res[0]
        self.project_list.append((project_name, self.project_path))
        # TODO: write to config file
        self.populate_project_menu()
        
        #DEBUG
        print ("project_path = " + str(self.project_path))
        
        git_access.create_repo(self.project_path)
        
        self.project_button.setText(project_name)
        self.file_model.setRootPath(self.project_path)
        self.file_tree.setRootIndex(self.file_model.index(self.project_path))
   
        
    # Called upon clicking the commit button, should open up the staging area window
    def on_commit_btn_click(self):
        print "on_commit_btn_click"
        if (self.project_path == None):
            cmds.warning("No project currently open")
       
        elif (git_access.get_files_changed() == []):
            cmds.warning("No files in '" + self.project_name + "' have been modified")
        else:
            if (self.staging_ui != None):
                self.staging_ui.delete_instances()
                self.staging_ui = None
            self.staging_ui = stagingUI.main(self.project_path)


    # Calls MEL workspaceControl command to check if the given
    # control exists, and if it does, closes and deletes it
    def delete_control(self, name):
        print "delete_control"
        if cmds.workspaceControl(name, q=True, exists=True):
            cmds.workspaceControl(name, e=True, close=True)
            cmds.deleteUI(name, control=True)
    
    # Deletes lingering instances of the panel and its workspace
    # control -- Maya can't have multiple panels with the same name up.
    def delete_instances(self):
        print "delete_instances"
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
        print "run"
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
