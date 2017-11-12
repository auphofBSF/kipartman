# Chapter 5: Data Displays and Grids
# Recipe 6: Modelling your data
#
from dialogs.panel_select_octopart import PanelSelectOctopart
from octopart.queries import PartsQuery
import wx.dataview as dv
import wx.lib.newevent
from frames.dropdown_frame import DropdownFrame
from frames.dropdown_dialog import DropdownDialog
from frames.select_octopart_frame import SelectOctopartFrame, EVT_SELECT_OCTOPART_OK_EVENT
import datetime
import inspect


SelectOctopartOkEvent, EVT_SELECT_OCTOPART_OK_EVENT = wx.lib.newevent.NewEvent()
SelectOctopartCancelEvent, EVT_SELECT_OCTOPART_APPLY_EVENT = wx.lib.newevent.NewEvent()

class OctopartDataModel(wx.dataview.PyDataViewModel):
    def __init__(self, searchpart):
        super(OctopartDataModel, self).__init__()
        if searchpart!='':
            q = PartsQuery()
            q.get(searchpart)
            self.data = q.results()
        else:
            self.data = []
            
    def GetColumnCount(self):
        return 7

    def GetColumnType(self, col):
        mapper = { 
            0 : 'string',
            1 : 'string',
            2 : 'string',
            3 : 'long',
            4 : 'long',
            5 : 'long',
            6 : 'string',
        }
        return mapper[col]

    def GetChildren(self, parent, children):
        # check root node
        if not parent:
            for octopart in self.data:
                children.append(self.ObjectToItem(octopart))
            return len(self.data)
        return 0
    
    def IsContainer(self, item):
        return False

    def HasContainerColumns(self, item):
        return True

    def GetParent(self, item):
        return wx.dataview.NullDataViewItem
    
    def GetValue(self, item, col):
        obj = self.ItemToObject(item)
        vMap = { 
            0 : obj.item().manufacturer().name(),
            1 : obj.snippet(),
            2 : obj.item().mpn(),
            3 : str(len(obj.item().offers())),
            4 : str(len(obj.item().datasheets())),
            5 : str(len(obj.item().specs())),
            6 : obj.item().octopart_url(), #TODO
        }
        if vMap[col] is None:
            return ""
        return vMap[col]

    def SetValue(self, value, item, col):
        pass
    
    def GetAttr(self, item, col, attr):
        return False

#     def HasDefaultCompare(self):
#         return False
#     
#     def Compare(self, item1, item2, column, ascending):
        #TODO allow sort integer columns properly
            
class SelectOctopartFrame(PanelSelectOctopart):
    def __init__(self, parent, initial_search=None): 
        """
        Create a popup window from frame
        :param parent: owner
        :param initial: item to select by default
        """
        super(SelectOctopartFrame, self).__init__(parent)

        self.search_octopart.Value = initial_search
    
        # create octoparts list
        self.octoparts_model = OctopartDataModel(initial_search)
        print self.octoparts_model.data
        #pdb.set_trace()
        self.tree_octoparts.AssociateModel(self.octoparts_model)
        # add default columns
        self.tree_octoparts.AppendTextColumn("Manufacturer", 0, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Description", 1, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Name", 2, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Offers", 3, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Datasheets", 4, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Parameters", 5, width=wx.COL_WIDTH_AUTOSIZE)
        self.tree_octoparts.AppendTextColumn("Details", 6, width=wx.COL_WIDTH_AUTOSIZE)
        for c in self.tree_octoparts.Columns:
            c.Sortable = True

        # set result functions
        self.cancel = None
        self.result = None
    
    def SetResult(self, result, cancel=None):
        self.result = result
        self.cancel = cancel
    
    def _search(self):
        # apply new filter and reload
        self.octoparts_model.Cleared()
        self.octoparts_model = OctopartDataModel(self.search_octopart.Value)
        #pdb.set_trace()
        self.tree_octoparts.AssociateModel(self.octoparts_model)


    # Virtual event handlers, overide them in your derived class
    def onSearchOctopartButton( self, event ):
        self._search()
    
    def onSearchOctopartEnter( self, event ):
        self._search()
    
    def onButtonCancelClick( self, event ):
        event = SelectOctopartCancelEvent()
        wx.PostEvent(self, event)
        if self.cancel:
            self.cancel()
    
    def onButtonOkClick( self, event ):
        sel = self.tree_octoparts.GetSelection()
        if not sel:
            return
        octopart = self.octoparts_model.ItemToObject(self.tree_octoparts.GetSelection())
        
        # trigger result event
        event = SelectOctopartOkEvent(data=octopart)
        wx.PostEvent(self, event)
        if self.result:
            self.result(octopart)

class ClassViewer(wx.Frame):
    def __init__(self, parent, title):
        super(ClassViewer, self).__init__(parent, title=title)

        # Look at all classes in wx namespace
        data = list()
        for x in dir(wx):
            item = getattr(wx, x)
            if inspect.isclass(item):
               # data.append(HierarchyInfo(item, None))
               pass

        dvc = dv.DataViewCtrl(self, style=dv.DV_VERT_RULES)
        #dvc.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU, self.onItemSelected)
        #self.model = ClassDataModel(data)
        #dvc.AssociateModel(self.model)
        
        autosize = wx.COL_WIDTH_AUTOSIZE
        dvc.AppendTextColumn("Class", 0, width=autosize)
        dvc.AppendTextColumn("Subclasses", 1, width=autosize, 
                             align=wx.ALIGN_CENTER)
        dvc.AppendTextColumn("Docstring", 2, width=autosize)

        sizer = wx.BoxSizer()
        sizer.Add(dvc, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize((400, 200))


class MyApp(wx.App):
    def OnInit(self):
        self.frame = ClassViewer(None, title="DataView Model")
        self.frame.Show();
        # dropdown = DropdownDialog(self.button_octopart, SelectOctopartFrame, '2N2222')
        # dropdown.panel.Bind( EVT_SELECT_OCTOPART_OK_EVENT, self.onSelectOctopartFrameOk )
        # dropdown.Dropdown()
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
