import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx

from TyrantVC.src import main_panel

# method for loading the main panel from the script editor
class open_tyrant_vc(OpenMayaMPx.MPxCommand):
    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
 
    def doIt(self, argList):
        main_panel.main()
 
def creator():
    return OpenMayaMPx.asMPxPtr( open_tyrant_vc() )
 
def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Team TyrantVC', '1.0', 'Any')
    try:
        # open the main ui on load
        main_panel.main()
        
        plugin.registerCommand('open_tyrant_vc', creator)
    except:
        raise RuntimeError('Failed to register command')
 
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterCommand('open_tyrant_vc')
    except:
        raise RuntimeError ('Failed to unregister command')