from dialogs.panel_footprints_proto import PanelFootprintsProto
from frames.edit_footprint_frame_proto import EditFootprintFrameProto, EVT_EDIT_FOOTPRINT_APPLY_EVENT, EVT_EDIT_FOOTPRINT_CANCEL_EVENT
from kicad.kicad_resource_manager import KicadResourceManager, KicadResourcePretty
from helper.filter import Filter
import rest
import helper.tree
import os

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

class DataModelLibraryPath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(DataModelLibraryPath, self).__init__()
        self.path = path
        
    def GetValue(self, col):
        vMap = { 
            0 : os.path.basename(self.path),
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def GetDragData(self):
        return {'id': self.path}

class DataModelLibrary(helper.tree.TreeContainerItem):
    def __init__(self, path, name):
        super(DataModelLibrary, self).__init__()
        self.path = os.path.join(path, name)
        self.name = name
        
    def GetValue(self, col):
        vMap = { 
            0 : self.name,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = False
        return True

    def GetDragData(self):
        return {'id': self.path}

class TreeManagerLibraries(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerLibraries, self).__init__(tree_view)

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelLibraryPath) and data.path==os.path.normpath(path):
                return data
        return None

    def FindLibrary(self, path, name):
        pathobj = self.FindPath(path)
        for data in self.data:
            if isinstance(data, DataModelLibrary) and data.name==name and data.parent==pathobj:
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelLibraryPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def AppendLibrary(self, path, name):
        libraryobj = self.FindLibrary(path, name)
        if libraryobj:
            return libraryobj
        pathobj = self.FindPath(path)
        print "++", path
        libraryobj = DataModelLibrary(path, name)
        self.AppendItem(pathobj, libraryobj)


class DataModelFootprintPath(helper.tree.TreeContainerItem):
    def __init__(self, path):
        super(DataModelFootprintPath, self).__init__()
        self.path = path
    
    def GetValue(self, col):
        if col==1:
            return self.path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False

class DataModelFootprint(helper.tree.TreeItem):
    def __init__(self, path, footprint):
        super(DataModelFootprint, self).__init__()
        self.path = path
        self.footprint = footprint

    def GetValue(self, col):
        if self.footprint.id==-1:
            id = ''
        else:
            id = self.footprint.id
        vMap = { 
            0 : str(id),
            1 : self.footprint.name,
            2 : self.footprint.description,
            3 : self.footprint.comment
        }
        return vMap[col]

#    def GetDragData(self):
#        if isinstance(self.parent, DataModelCategoryPath):
#            return {'id': self.footprint.id}
#        return None

class TreeManagerFootprints(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerFootprints, self).__init__(tree_view)

    def FindPath(self, path):
        for data in self.data:
            if isinstance(data, DataModelFootprintPath) and data.path==os.path.normpath(path):
                return data
        return None

    def AppendPath(self, path):
        pathobj = self.FindPath(path)
        if pathobj:
            return pathobj
        pathobj = DataModelFootprintPath(path)
        parentpath = self.FindPath(os.path.dirname(path))
        self.AppendItem(parentpath, pathobj)
        return pathobj

    def AppendFootprint(self, path, footprint):
        pathobj = self.FindPath(path)
        footprintobj = DataModelFootprint(path, footprint)
        self.AppendItem(pathobj, footprintobj)
        return footprintobj


class FootprintsFrameProto(PanelFootprintsProto): 
    def __init__(self, parent):
        super(FootprintsFrameProto, self).__init__(parent)
        
        self.resource_pretty = KicadResourcePretty()
        self.manager_pretty = KicadResourceManager(self.resource_pretty)

        # create libraries data
        self.tree_libraries_manager = TreeManagerLibraries(self.tree_libraries)
        self.tree_libraries_manager.AddTextColumn("name")
        self.tree_libraries_manager.OnSelectionChanged = self.onTreeLibrariesSelChanged

        # footprints filters
        self.footprints_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)

        # create footprint list
        self.tree_footprints_manager = TreeManagerFootprints(self.tree_footprints)
        self.tree_footprints_manager.AddIntegerColumn("id")
        self.tree_footprints_manager.AddTextColumn("name")
        self.tree_footprints_manager.AddTextColumn("description")
        self.tree_footprints_manager.AddIntegerColumn("comment")
        self.tree_footprints_manager.OnSelectionChanged = self.onTreeFootprintsSelChanged

        # create edit footprint panel
        self.panel_edit_footprint = EditFootprintFrameProto(self.footprint_splitter)
        self.footprint_splitter.SplitHorizontally(self.footprint_splitter.Window1, self.panel_edit_footprint, 400)
        self.panel_edit_footprint.Bind( EVT_EDIT_FOOTPRINT_APPLY_EVENT, self.onEditFootprintApply )
        self.panel_edit_footprint.Bind( EVT_EDIT_FOOTPRINT_CANCEL_EVENT, self.onEditFootprintCancel )

        self.toolbar_footprint.ToggleTool(self.toggle_footprint_path.GetId(), True)
        
        self.load() 
        
    def load(self):
        self.loadLibraries()
        self.loadFootprints()
        
    def loadLibraries(self):
        # clear all
        self.tree_libraries_manager.ClearItems()
        
        # load libraries
        libraries = self.resource_pretty.GetLibraries()

        # load tree
        for library in libraries:
            # decompose path
            folders = []
            path = os.path.dirname(library)
            name = os.path.basename(library)
            while path!='':
                folders.insert(0, path)
                path = os.path.dirname(path)
            
            for folder in folders:
                self.tree_libraries_manager.AppendPath(folder)

            self.tree_libraries_manager.AppendLibrary(os.path.dirname(library), name)

    def loadFootprints(self):
        # clear all
        self.tree_footprints_manager.ClearItems()

        # load libraries from kicad files
        libraries = self.resource_pretty.GetLibraries()
        
        # load footprints from local folder
        for library in libraries:
            path = library
            self.tree_footprints_manager.AppendPath(path)

            # load footprints
            footprint_files = self.resource_pretty.GetFootprints(library)
            for footprint_file in footprint_files:
                footprint = rest.model.Footprint(id=-1)
                footprint.name = footprint_file.replace('.kicad_mod', '')
                footprint.local_footprint = os.path.join(path, footprint_file)
                self.tree_footprints_manager.AppendFootprint(path, footprint)
        
        # load footprints from kipartbase
        # TODO
    
    def setToolbarFootprintState(self):
        pass
    
    def onTreeLibrariesSelChanged( self, event ):
        item = self.tree_libraries.GetSelection()
        if item.IsOk()==False:
            return    
        pathobj = self.tree_libraries_manager.ItemToObject(item)
        # set category filter
        self.footprints_filter.remove('path')
        if pathobj:
            self.footprints_filter.add('path', pathobj.path, pathobj.path)
        # apply new filter and reload
        self.loadFootprints()

    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.footprints_filter.remove(button.GetName())
        self.tree_libraries.UnselectAll()
        self.loadFootprints()

    def onTreeFootprintsSelChanged( self, event ):
        item = self.tree_footprints.GetSelection()
        if item.IsOk()==False:
            return
        footprintobj = self.tree_footprints_manager.ItemToObject(item)
        if isinstance(footprintobj, DataModelFootprint)==False:
            return
        self.panel_edit_footprint.SetFootprint(footprintobj.footprint)
        
    def onEditFootprintApply( self, event ):
        pass
     
    def onEditFootprintCancel( self, event ):
        pass