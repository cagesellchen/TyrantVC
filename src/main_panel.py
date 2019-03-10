from maya.app    .general.mayaMixin import MayaQWidgetDockableMixin
from maya import OpenMayaUI as omui
from maya import cmds as cmds
from maya import mel as mel
from PySide2.QtCore import * 
from PySide2.QtGui import * 
from PySide2.QtWidgets import *
from shiboken2 import wrapInstance
import re
import git_access
import config_access
import stagingUI

# Returns the main maya window
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
        # we need a central widget because this panel is a DockableMixin, so it needs
        # a widget for us to attach a layout to
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # set up the project button, the dropdown button at the top that contains
        # the list of projects
        self.project_button = QPushButton()
        self.project_menu = QMenu()
        self.project_list = None
        self.project_path = None
        self.project_name = None
        self.populate_project_menu()
     
        main_layout.addWidget(self.project_button)
        
        ## Tabs: set up the tabs that take up most of the main panel
        tab_widget = QTabWidget()
        files_tab_widget = QWidget()
        commits_tab_widget = QWidget()

        # set up the files and commits tab
        self.make_files_tab(files_tab_widget)
        self.make_commits_tab(commits_tab_widget)

        # add both the tabs to the layout
        tab_widget.addTab(files_tab_widget, 'Files')
        tab_widget.addTab(commits_tab_widget, 'Commits')
        main_layout.addWidget(tab_widget)
        
        # commit button at the bottom of the panel
        self.commit_btn = QPushButton()
        self.commit_btn.setText('Commit')
        self.commit_btn.clicked.connect(self.on_commit_btn_click)
        main_layout.addWidget(self.commit_btn)
        
        # now that everything is added to the layout, we can set it to be the
        # layout of the central_widget, and then attach central_widget to self.
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('TyrantVC')
        self.setAttribute(Qt.WA_DeleteOnClose)   


    ####################
    ####################
        #COMMITS TAB#     
    ####################
    ####################

    # Sets up the commits tab, should only be called once when setting up the UI
    def make_commits_tab(self, commits_tab_widget):
        commits_layout = QVBoxLayout()
        commits_list = QWidget()
        self.commits_list_layout = QVBoxLayout()
        
        self.populate_commits_tab()
            
        commits_list.setLayout(self.commits_list_layout)
        self.commits_scroll_area = QScrollArea()
        self.commits_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.commits_scroll_area.setWidgetResizable(True)
        self.commits_scroll_area.setWidget(commits_list)
        
        commits_layout.addWidget(self.commits_scroll_area)
        commits_tab_widget.setLayout(commits_layout)
    
    # Gets the commit information for the current repo and fills the commits tab
    # with the appropriate info for each commit. Should be called whenever the repo
    # changes, or when going back from the files list
    def populate_commits_tab(self):
        # if the layout already exists, clean up the old one so we can replace it
        if self.commits_list_layout is not None:
            self.clear_commits_list_layout()
                  
        # if we have a project selected, then we should fill commits tab with its commits
        if self.project_name is not None:
            commit_data = git_access.get_all_commits()
            # commit_data in the form of (commit_id, date, message, files)
            for i, commit in enumerate(commit_data):
                self.make_commit_box(str(len(commit_data) - i), commit)
            # addStretch() makes sure the frames sit at the top instead of stretching down
            self.commits_list_layout.addStretch()
            # layout().update() makes sure the UI updates -- Maya has a bug with dockable panels not updating
            self.layout().update()

    # Removes everything currently in the commits list. Should be called
    # before populating the commits list (either with files or with a new commit list)           
    def clear_commits_list_layout(self):
        # takeAt(0) will remove the first from the layout, pushing the rest up.
        # we can continue doing that until there are none left
        while self.commits_list_layout.count():
            child = self.commits_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    # Puts a commit box for the provided number and commit in the
    # commits_list_layout. Should be called whenever populating the
    # commits list    
    def make_commit_box(self, number, commit):
        # assign commit fields to variables for readability
        date = commit[1]
        message = commit[2]
        num_files = str(len(commit[3]))
        
        ## set up the box that contains the commit info
        box = QFrame()
        box.setFrameStyle(QFrame.StyledPanel)
        box.setLineWidth(2)
        box.setMaximumHeight(80)
        box.setMaximumWidth(230)
        
        ## layout setup, doing stacked HBoxes so that
        ## we aren't restricted by a grid
        box_layout = QVBoxLayout()
        
        first_row_layout = QHBoxLayout()
        second_row_layout = QHBoxLayout()

        ## label containing the commit number
        first_row_layout.addWidget(self.get_commit_id_label(number))

        ## label containing the commit message
        first_row_layout.addWidget(self.get_commit_message_label(message))
        
        ## label containing the date
        second_row_layout.addWidget(self.get_commit_date_label(date))
        
        ## button containing the number of files
        files_btn = QPushButton()
        files_btn.setText(num_files + (' file' if num_files is '1' else ' files'))
        files_btn.clicked.connect(lambda c=commit, n=number: self.on_commit_file_btn_click(number, c))
        second_row_layout.addWidget(files_btn)
        
        ## add everything to the box
        box_layout.addLayout(first_row_layout)
        box_layout.addLayout(second_row_layout)
        box.setLayout(box_layout)
        self.commits_list_layout.addWidget(box)
        self.commits_list_layout.setAlignment(box, Qt.AlignTop)

    # Called when user clicks the button associated with a certain commit in the commits tab
    # commit is in the form (commit_id, date, message, files)
    def on_commit_file_btn_click(self, number, commit):
        commit_id = commit[0]
        date = commit[1]
        message = commit[2]
        files = commit[3]
        
        self.clear_commits_list_layout()
        
        ## set up the frame
        box = QFrame()
        box.setFrameStyle(QFrame.StyledPanel)
        box.setLineWidth(2)
        box.setMaximumHeight(80)
        box.setMaximumWidth(230)
        
        box_layout = QVBoxLayout()
        first_row_layout = QHBoxLayout()
        
        ## back button, to return to the commits list
        back_button = QPushButton()
        back_button.setText('Back')
        back_button.clicked.connect(self.populate_commits_tab)
        first_row_layout.addWidget(back_button)
        
        ## calls helper functions to add the ID and the commit message
        first_row_layout.addWidget(self.get_commit_id_label(number))
        first_row_layout.addWidget(self.get_commit_message_label(message))
        
        box_layout.addLayout(first_row_layout)
        
        ## the date
        box_layout.addWidget(self.get_commit_date_label(date))
        
        box.setLayout(box_layout)
        
        self.commits_list_layout.addWidget(box)
        
        ## for every file in this commit, add a commit_file_box to the layout
        for filename in files:
            self.make_commit_file_box(filename, commit_id)
        
        # addStretch() makes sure the frames sit at the top instead of stretching down
        self.commits_list_layout.addStretch()
        # layout().update() makes sure the UI updates -- Maya has a bug with dockable panels not updating
        self.layout().update()
    
    # Creates a single box that provides a filename and buttons to open the
    # file and the diff, and adds it to commits_list_layout
    def make_commit_file_box(self, filename, commit_id):
        ## set up the frame
        box = QFrame()
        box.setFrameStyle(QFrame.StyledPanel)
        box.setLineWidth(2)
        box.setMaximumHeight(80)
        box.setMaximumWidth(230)
        
        box_layout = QVBoxLayout()
        
        ## the filename label
        filename_label = QLabel()
        filename_label.setText(filename)
        box_layout.addWidget(filename_label)
        
        ## the two buttons, one that lets you view the file and one that views changes
        button_layout = QHBoxLayout()
        
        view_file_button = QPushButton()
        view_file_button.setText('View File')
        view_file_button.clicked.connect(lambda f=filename,c=commit_id: self.show_file(f, c))
        button_layout.addWidget(view_file_button)
        
        view_changes_button = QPushButton()
        view_changes_button.setText('View Changes')
        view_changes_button.clicked.connect(lambda f=filename,c=commit_id: self.show_diff(f, c))
        button_layout.addWidget(view_changes_button)
        
        ## add everything to the layout
        box_layout.addLayout(button_layout)
        box.setLayout(box_layout)
        self.commits_list_layout.addWidget(box)
    
    # Called when the suer clicks the "View File" button for a file in commit history,
    # and will open a new window with the post-commit version for that file from that commit 
    def show_file(self, filename, commit_id):
        file = git_access.get_file_version(commit_id, filename)
        # TODO: pop up with a new window that has the file info in it
        print(file)
    
    # Called when the user clicks the "View Changes" button for a file in commit history,
    # and will open a new window with the diff for that file from that commit  
    def show_diff(self, filename, commit_id):
        # TODO: add a git_access method that returns the diff 
        # TODO: pop up with a new window that has the diff in it
        print(filename)
    
    # Helper method that returns a label with the given commit id in the proper format    
    def get_commit_id_label(self, number):
        id_label = QLabel()
        id_label.setText(number + ':')
        tf = id_label.font()
        tf.setBold(True)
        tf.setPixelSize(int(tf.pixelSize() * 1.5))
        id_label.setFont(tf)
        id_label.adjustSize()
        return id_label
        
    # Helper method that returns a label with the given commit message in the proper format        
    def get_commit_message_label(self, message):
        message_label = QLabel()
        message_label.setText(message)
        message_label.setWordWrap(True)
        tf = message_label.font()
        tf.setBold(True)
        message_label.setFont(tf)
        message_label.adjustSize()
        return message_label
    
    # Helper method that returns a label with the given commit date in the proper format 
    def get_commit_date_label(self, date):    
        date_label = QLabel()
        # put date in, cutting off the time zone
        date_label.setText(' '.join(date.split(' ')[:-1]))
        return date_label

    ####################
    ####################
        #FILES TAB#     
    ####################
    ####################

    # Creates the files tab in the given file_tab_widget
    def make_files_tab(self, files_tab_widget):
        file_layout = QVBoxLayout()
        # the file tab contains a TreeView, which is displaying a FileSystemModel.
        # this FileSystemModel will display the files from a given root directory.
        # to set the root directory of self.file_model, call self.file_model.setRootPath
        # as well as self.file_tree.setRootIndex.
        self.file_model = QFileSystemModel()
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        # attach a function to the file_tree so that if it is double clicked, we 
        # can open the file that is selected.
        self.file_tree.doubleClicked.connect(self.on_file_double_click)
        file_layout.addWidget(self.file_tree)
        files_tab_widget.setLayout(file_layout)

    # Should be called whenever the file model view needs to change the folder it is looking at.
    # name should be the name of the current project, and path should be the path to the directory.
    # this function also updates the project_button.
    def set_file_model_path(self, name, path):
        self.project_name = name
        self.project_path = path
        self.file_model.setRootPath(path)
        self.file_tree.setRootIndex(self.file_model.index(path))
        self.project_button.setText(name)

    # Called when the file system model widget is double-clicked
    # and opens the appropriate file in script editor using mel commands.
    # If the file is already open in the script editor, it just selects that tab.
    def on_file_double_click(self):
        index = self.file_tree.currentIndex()
        # the full file path of the file selected
        file_path = self.file_model.filePath(index)
        # just the file name and extension
        file_name = self.file_model.fileName(index)
        ext = None
        if len(file_name.split('.')) > 1:
            ext = file_name.split('.')[1]
          
        # opens the script editor
        mel.eval('ScriptEditor')
        # tries to select the tab with the given file name, if it finds it,
        # then it selects it and returns 1.
        res = mel.eval('selectExecuterTabByName(\"' + file_path + '\");')
        if res == 1:
            return  
        # couldn't find the tab, so we need to make it
        tab_selected = False

        if ext == 'py':
            mel.eval('buildNewExecuterTab(-1, "Python", "python", 0);')
        elif ext == 'mel':
            mel.eval('buildNewExecuterTab(-1, "MEL", "mel", 0);')
        else:
            tab_selected = True
            mel.eval('addNewExecuterTab("", 0);')

        
        # if it was not a python or mel file, we didn't build it, and addExecutorTab
        # already selected it. 
        if not tab_selected:    
            # these commands will select the tab that we just created
            mel.eval('tabLayout -e -selectTabIndex `tabLayout -q -numberOfChildren $gCommandExecuterTabs` $gCommandExecuterTabs;')
            mel.eval('selectCurrentExecuterControl();')

        # this command will fill the newly created tab with the contents of the given file    
        mel.eval('delegateCommandToFocusedExecuterWindow("-e -loadFile \\"' + file_path + '\\"", 0);')
        # these commands will rename the tab to the file name, with the path as the tooltip hover
        mel.eval('renameCurrentExecuterTab(\"' + file_path + '\", 0);')
        mel.eval('delegateCommandToFocusedExecuterWindow "-e -modificationChangedCommand executerTabModificationChanged" 0;');
        mel.eval('delegateCommandToFocusedExecuterWindow "-e -fileChangedCommand executerTabFileChanged" 0;')
    


    ####################
    ####################
        #MAIN TAB#     
    ####################
    ####################

    # This should be called when the project list changes, and it fills the project button 
    # with the list of projects from the project_list, or if project_list has not been
    # filled, it fills it from the config file
    def populate_project_menu(self):
        self.project_menu.clear() 
        
        # call config_access to get a list if we don't have one yet. after that we
        # should maintain our own project_list.
        if self.project_list is None:
            self.project_list = config_access.parse_config()
        
        # add a function to each item in the drop down that will call a function, passing it 
        # that item, the tuple of (name, file_path)    
        for item in self.project_list:
            self.project_menu.addAction(item[0], lambda t=item: self.project_menu_item_clicked(t))
            
        self.project_menu.addAction("Create new project...", self.create_new_project)
        self.project_button.setMenu(self.project_menu)
        
        # by default, we don't select any project    
        self.project_button.setText("No Project Selected")
    


    # Called upon clicking a project in the project_list. Sets the button text       
    def project_menu_item_clicked(self, item):           
        self.set_file_model_path(item[0], item[1])    
        git_access.create_repo(item[1])
        self.populate_commits_tab() 

    
    # Called upon clicking the create new project button. Opens a file dialog, adds the project
    # selected to the list, and opens that project.
    def create_new_project(self):
        # opens a file dialog which allows only selection of directories
        res = cmds.fileDialog2(fileMode=3, dialogStyle=2, okCaption='Select', caption='Select Folder for Project')
        if res is None:
            # they cancelled the file picker
            return
        
        # get the last thing after a / or a \, which is the name of the directory
        project_name = re.split(r'[/\\]', res[0])[-1]
        # check to make sure a project with the same name doesn't already exist (this is not allowed)
        for item in self.project_list:
            if (item[0] == project_name):
               cmds.warning("A project with name '" + item[0] + "' already exisits")
               return
            #    PySide.QtGui.QMessageBox QStatusBar.showMessage("Error: a project of this name already exists")
            #    return
        
        # add the new project to the list and re-populate    
        self.project_list.append((project_name, res[0]))
        config_access.add_config(project_name, res[0])
        self.populate_project_menu()
        
        self.set_file_model_path(project_name, res[0])

        git_access.create_repo(self.project_path)
        self.populate_commits_tab()


    # Called upon clicking the commit button, should open up the staging area window
    def on_commit_btn_click(self):
        if (self.project_path == None):
            cmds.warning("No project currently open")
        elif (git_access.get_files_changed() == []):
            cmds.warning("No files in '" + self.project_name + "' have been modified")
        else:
            if (self.staging_ui != None):
                # if a staging ui already exits, close it, then make a new one.
                self.staging_ui.delete_instances()
                self.staging_ui = None
            self.staging_ui = stagingUI.main(self.project_path, self.populate_commits_tab)



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

# main should be called in order to run mainPanel            
def main():
    global mainPanel
    main_window = get_main_window()  
    mainPanel = TyrantVCMainPanel(parent=main_window)
    mainPanel.run()
    return mainPanel
    
if __name__ == '__main__':
    main()
