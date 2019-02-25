# TyrantVC User Manual [![Build Status](https://travis-ci.org/cagesellchen/TyrantVC.svg?branch=master)](https://travis-ci.org/cagesellchen/TyrantVC)

## What is TyrantVC?
Version control systems are tools that allow you to manage changes to source code over time. Version control software keeps track of every modification to a set of files, and you can save a version of a file at any time by “committing” the modified files you wish to save. You can then view past versions of a file, or revert to a previous version. This affords confidence when changing code, because committed code is never lost.

TyrantVC is a version control plugin for Maya which provides users with access to standard version control functionality for their scripting projects, including committing files and viewing previous versions of your project. The plugin includes the addition of a special UI panel to the Maya Environment which allows you to access all of this functionality in an intuitive way.

## Prerequisites
* Maya 2017 or newer
* Git

## Installing TyrantVC
**MacOSX:**
1. Open the terminal
2. Navigate to downloads:
> cd Downloads
3. Download install_plugin.py:
> wget https://raw.githubusercontent.com/cagesellchen/TyrantVC/master/install_plugin.py
4. Run install_plugin.py
> python install-plugin.py

**Windows:**
1. Open the Command Prompt as an Administrator (right click the Command Prompt shortcut and select "Run as Administrator")
2. Navigate to downloads:
> cd "Downloads"
3. Download install_plugin.py:
> curl https://raw.githubusercontent.com/cagesellchen/TyrantVC/master/install_plugin.py
4. Run install_plugin.py
> py install-plugin.py

Doing this should download all of the plugin files to the correct location on your disk. You should check this by doing the following:

1. In Maya, open the Plugin Manager. You can do this by selecting the Windows tab, going to Settings/Preferences, and clicking on Plug-in Manager.
2. In the Plug-in Manager, scroll through the plugins until you see TyrantVC. 
Make sure Loaded and Auto load are both checked.

If this does not work you can perform the installation manually by downloading all of the script files and moving them to the correct location on your disk:

**Windows:**
1. Open the Command Prompt
2. Navigate to the Maya plugin folder: 
> cd "C:\Program Files\Autodesk\Maya2019\bin\plug-ins"
3. Clone our repo: 
> git clone https://github.com/cagesellchen/TyrantVC
4. Move tyrantvc.py to its parent folder (plug-ins): 
> move TyrantVC/tyrantvc.py

**MacOSX:**
1. Open the terminal
2. Navigate to the Maya plugin folder: 
> cd /Users/Shared/Autodesk/maya/plug-ins
3. Clone our repo: 
> git clone https://github.com/cagesellchen/TyrantVC
4. Move tyrantvc.py to its parent folder (plug-ins): 
> mv TyrantVC/tyrantvc.py .

Note that you need the period at the end of the above command

You should restart Maya if it was open. Check that TyrantVC shows up in the Plug-in Manager, and that Loaded and Auto load are both checked (see above for instructions on how to do this). 

There should be a new tab in the shelves panel called TyrantVC. In that tab, click the first icon to open up the plugin. Instructions on what each element of that panel does and how to operate the plugin are listed below.

  
## Using TyrantVC
### Creating A Project
A new version control project can be created for any folder of script files. If you want to create a new empty project, create an empty folder in your Maya scripts folder.

To create a project:
1. Click on the arrow next to the “\<Current Project>” text within the TyrantVC panel. Note: if this is the first time using the plugin, “No Current Project” will be displayed.
2. From the dropdown, scroll to the bottom and select “Create a New Project”. 
3. Select the folder location of your project. 
4. Once the location is specified, a git repo will be created, and your project will be shown in the file browsing area of the UI panel.
  
### Changing Projects
1. Click on the arrow next to the “\<Current Project>” text within the TyrantVC panel. 
2. From the dropdown, select the project you wish to work on.

### View Files in Current Project
The Files tab allows you to view the files in your current project. 
* To view files in your project, click the “Files” tab at the top of the main panel.
* Files highlighted as green are up to date with the latest commit.
* Files that are highlighted with red have been modified since the last commit. 
* You can click on a file to explore the previous versions of that file. 

### View a List of Previous Commits
The Commit tab allows you to view a history of commits for the current project. 
* To view previous commits, click the “Commits” tab at the top of the main panel. 
* Each commit entry shows the date, the commit message, and the number of files in the commit. 
* To view more information about any individual commit, you can click on the commit. This will create a popup with more information.

### Committing a File
The staging area allows you to commit (save) files. To navigate to the staging area:
1. Click the “Commit” button at the bottom of the window. This will open a pop-up window which displays a list of the files which have been modified since your last commit.
2. By default every file is checked (which means they will all be committed).  If you don’t want to commit certain files, you can uncheck them.
3. Enter a mandatory commit message, which should describe the changes you’ve made since your last commit.
4. To finalize your commit, click “Commit”.  Otherwise, click “Cancel” or close the popup window.

### View a Past Commit
To view a past commit: 
1. Select the “Commits” tab
2. Click on the commit for which you would like to see more information.

The Past Commit View will show you each file that was a part of this commit, as well as the number of lines added and removed. 

To view the version of the file that was added at this commit, click on the file in the list and you will be taken to the Previous File Version view.

To return to the Commit Tracking area, click the “Back” button in the upper lefthand corner.

### View A File's Previous Commits
To view a file's previous commits:
1. Select the “Files” tab
2. Double click the desired file  This will display a list of previous commits. 

To return to File View, click the “Back” button in the upper lefthand corner.

### View a Previous Version of a File
To view a previous version of a file:
1. Select the Files tab
2. Double click the desired file
3. Select the desired commit from the list of previous commits. This will open a pop-up window, displaying the state of the file at that previous commit.  

Because this is a past version of the file, it cannot be edited.  However, you can copy and paste any or all of the file into your current file editor window.






 

