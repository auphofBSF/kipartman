from dialogs.panel_parts import PanelParts
from frames.edit_category_frame import EditCategoryFrame
from frames.edit_part_frame import EditPartFrame, EVT_EDIT_PART_APPLY_EVENT, EVT_EDIT_PART_CANCEL_EVENT
import helper.tree
from helper.filter import Filter
import rest
import wx

# help pages:
# https://wxpython.org/docs/api/wx.gizmos.TreeListCtrl-class.html

# class PartCategoryDataObject(wx.TextDataObject):
#     def __init__(self, category): 
#         super(PartCategoryDataObject, self).__init__()
#         self.category = category
#         self.SetText(json.dumps({'model': 'PartCategory', 'url': category.path, 'id': category.id}))
#         
# class PartCategoryDropTarget(wx.TextDropTarget):
#     def __init__(self, frame):
#         self.frame = frame
#         super(PartCategoryDropTarget, self).__init__()
#     
#     #TODO: set drag cursor depending on accept/reject drop
#     def OnDropText(self, x, y, text):
#         data = json.loads(text)
#         print "PartCategoryDropTarget.OnDropText", data, x, y
#         item, _ = self.frame.tree_categories.HitTest((x, y))
#         if item.IsOk():
#             target_category = self.frame.tree_categories.GetItemData(item)
#         else:
#             target_category = None
#         if data['model']=='PartCategory':
#             source_category = PartCategoriesQuery().get(data['id'])[0]
#             if source_category:
#                 source_category.parent = target_category
#             PartCategoriesQuery().update(source_category)
#         elif data['model']=='Part':
#             source_part = PartsQuery().get(data['id'])[0]
#             if source_part:
#                 source_part.category = target_category
#                 PartsQuery().update(source_part)
#         self.frame.load()
#         return wx.DragMove
# 
# 
# class PartDataObject(wx.TextDataObject):
#     def __init__(self, category): 
#         super(PartDataObject, self).__init__()
#         self.category = category
#         self.SetText(json.dumps({'model': 'Part', 'url': category.path, 'id': category.id}))
# 
# class PartDropTarget(wx.TextDropTarget):
#     def __init__(self, frame):
#         self.frame = frame
#         super(PartDropTarget, self).__init__()
#     
#     #TODO: set drag cursor depending on accept/reject drop
#     def OnDropText(self, x, y, text):
#         data = json.loads(text)
#         print "PartDropTarget.OnDropText", data, x, y
#         item, _ = self.frame.tree_parts.HitTest((x, y))
#         if item.IsOk():
#             # do a copy to avoid nasty things
#             target_part = copy.deepcopy(self.frame.parts_model.ItemToObject(item))
#         else:
#             target_part = None
#         if data['model']=='Part':
#             source_part = PartsQuery().get(data['id'])[0]
#             if source_part and target_part:
#                 target_part.parts.append(source_part.id)
#                 PartsQuery().update(target_part)
#         self.frame._loadParts()
#         return wx.DragMove

class DataModelCategory(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategory, self).__init__()
        self.category = category
        
    def GetValue(self, col):
        vMap = { 
            0 : self.category.name,
            1 : self.category.description,
        }
        return vMap[col]

    def GetAttr(self, col, attr):
        attr.Bold = True
        return True

    def GetDragData(self):
        return {'id': self.category.id}
    
class DataModelCategoryPath(helper.tree.TreeContainerItem):
    def __init__(self, category):
        super(DataModelCategoryPath, self).__init__()
        self.category = category
    
    def GetValue(self, col):
        if self.category:
            path = self.category.path
        else:
            path = "/"
        if col==1:
            return path
        return ''

    def HasContainerColumns(self):
        return True

    def GetAttr(self, col, attr):
        if col==1:
            attr.Bold = True
            return True
        return False
    
class DataModelPart(helper.tree.TreeContainerLazyItem):
    def __init__(self, part):
        super(DataModelPart, self).__init__()
        self.part = part
        if part.has_childs:
            # add a fake item
            self.childs.append(None)
            
    def GetValue(self, col):
        vMap = { 
            0 : str(self.part.id),
            1 : self.part.name,
            2 : self.part.description,
            3 : self.part.comment
        }
        return vMap[col]

    def Load(self, manager):
        if self.part.has_childs==False:
            return
        part = rest.api.find_part(self.part.id, with_childs=True)
        
        for child in part.childs:
            manager.AppendItem(self, DataModelPart(child))

    def GetDragData(self):
        if isinstance(self.parent, DataModelCategoryPath):
            return {'id': self.part.id}
        return None


class TreeManagerParts(helper.tree.TreeManager):
    def __init__(self, tree_view):
        super(TreeManagerParts, self).__init__(tree_view)

    def FindPart(self, part_id):
        for data in self.data:
            if isinstance(data, DataModelPart) and isinstance(data.parent, DataModelCategoryPath) and data.part.id==part_id:
                return data
        return None
    
    def FindCategoryPath(self, category):
        if category:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category.id==category.id:
                    return data
        else:
            for data in self.data:
                if isinstance(data, DataModelCategoryPath) and data.category is None:
                    return data
        return None
    
    def DeletePart(self, part):
        partobj = self.FindPart(part.id)
        if partobj is None:
            return
        categoryobj = partobj.parent
        self.DeleteItem(partobj.parent, partobj)
        if categoryobj and len(categoryobj.childs)==0:
            self.DeleteItem(categoryobj.parent, categoryobj)

    def UpdatePart(self, part):
        partobj = self.FindPart(part.id)
        if partobj is None:
            return
        self.UpdateItem(partobj)

    def AppendCategoryPath(self, category):
        categoryobj = self.FindCategoryPath(category)
        if categoryobj:
            return categoryobj
        categoryobj = DataModelCategoryPath(category)
        self.AppendItem(None, categoryobj)
        return categoryobj
    
    def AppendPart(self, part):
        categoryobj = self.AppendCategoryPath(part.category)
        partobj = DataModelPart(part)
        self.AppendItem(categoryobj, partobj)
        self.Expand(categoryobj)
        return partobj
    
        
class PartsFrame(PanelParts): 
    def __init__(self, parent): 
        super(PartsFrame, self).__init__(parent)
        
        # create categories list
        self.tree_categories_manager = helper.tree.TreeManager(self.tree_categories)
        self.tree_categories_manager.AddTextColumn("name")
        self.tree_categories_manager.AddTextColumn("description")
        self.tree_categories_manager.DropAccept(DataModelCategory, self.onTreeCategoriesDropCategory)
        self.tree_categories_manager.DropAccept(DataModelPart, self.onTreeCategoriesDropPart)
        self.tree_categories_manager.OnSelectionChanged = self.onTreeCategoriesSelChanged
        # parts filters
        self.parts_filter = Filter(self.filters_panel, self.onButtonRemoveFilterClick)
        
        # create parts list
        self.tree_parts_manager = TreeManagerParts(self.tree_parts)
        self.tree_parts_manager.AddIntegerColumn("id")
        self.tree_parts_manager.AddTextColumn("name")
        self.tree_parts_manager.AddTextColumn("description")
        self.tree_parts_manager.AddIntegerColumn("comment")
        self.tree_parts_manager.OnSelectionChanged = self.onTreePartsSelChanged
        # 
        # create edit part panel
        self.panel_edit_part = EditPartFrame(self.part_splitter)
        self.part_splitter.SplitHorizontally(self.part_splitter.Window1, self.panel_edit_part, 400)
        self.panel_edit_part.Bind( EVT_EDIT_PART_APPLY_EVENT, self.onEditPartApply )
        self.panel_edit_part.Bind( EVT_EDIT_PART_CANCEL_EVENT, self.onEditPartCancel )

        # initial edit state
        self.show_part(None)
        self.edit_state = None
        
        self.load()
        
    def loadCategories(self):
        # clear all
        self.tree_categories_manager.ClearItems()
        
        # load categories
        categories = rest.api.find_parts_categories()

        # load tree
        to_add = []
        id_category_map = {}
        for category in categories:
            to_add.append(category)
        while len(to_add)>0:
            category = to_add[0]
            id_category_map[category.id] = DataModelCategory(category)
            to_add.pop(0)
            
            # add to model
            if category.parent:
                self.tree_categories_manager.AppendItem(id_category_map[category.parent.id], id_category_map[category.id])
            else:
                self.tree_categories_manager.AppendItem(None, id_category_map[category.id])
            
            # load childs
            if category.childs:
                for child in category.childs:
                    to_add.append(child)
        
    def loadParts(self):
        # clear all
        self.tree_parts_manager.ClearItems()
        
        # load parts
        parts = rest.api.find_parts(**self.parts_filter.query_filter())

        # load categories
        categories = {}
        for part in parts:
            if part.category:
                category_name = part.category.path
            else:
                category_name = "/"

            if categories.has_key(category_name)==False:
                categories[category_name] = DataModelCategoryPath(part.category)
                self.tree_parts_manager.AppendItem(None, categories[category_name])
            self.tree_parts_manager.AppendItem(categories[category_name], DataModelPart(part))
        
        for category in categories:
            self.tree_parts_manager.Expand(categories[category])
                
    def load(self):
        try:
            self.loadCategories()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        try:
            self.loadParts()
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def load_full_part(self, partobj):
        if partobj:
            # read whole part from server
            partobj.part = rest.api.find_part(partobj.part.id, with_offers=True, with_parameters=True, with_childs=True, with_distributors=True, with_manufacturers=True)
        
    def show_part(self, part):
        # disable editing
        self.panel_edit_part.enable(False)
        # enable evrything else
        self.panel_category.Enabled = True
        self.panel_parts.Enabled = True
        # set part
        self.panel_edit_part.SetPart(part)
        
    def edit_part(self, part):
        self.show_part(part)
        # enable editing
        self.panel_edit_part.enable(True)
        # disable evrything else
        self.panel_category.Enabled = False
        self.panel_parts.Enabled = False
        
    def new_part(self):
        part = rest.model.PartNew()
        
        # set category
        item = self.tree_categories.GetSelection()
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
            if category.category:
                part.category = category.category
        
#         part.name = ''
#         part.description = ''
#         part.comment = ''
#         part.octopart = None
#         part.updated = None
#         part.category = None
#         part.childs = []
#         part.footprint = None
#         part.parameters = []
#         part.distributors = []
#         part.manufacturers = []

        self.edit_part(part)


    def onButtonRefreshCategoriesClick( self, event ):
        self.loadCategories()

    def onButtonAddCategoryClick( self, event ):
        category = EditCategoryFrame(self).addCategory(rest.model.PartCategoryNew)
        if category:
            try:
                # retrieve parent item from selection
                parentitem = self.tree_categories.GetSelection()
                parentobj = None
                category.parent = None
                if parentitem:
                    parentobj = self.tree_categories_manager.ItemToObject(parentitem)
                    category.parent = parentobj.category
                    
                # create category on server
                category = rest.api.add_parts_category(category)
                # create category on treeview
                newitem = self.tree_categories_manager.AppendItem(parentobj, DataModelCategory(category)) 
                # add category to item element
                self.tree_categories_manager.SelectItem(newitem)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonEditCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        category = EditCategoryFrame(self).editCategory(categoryobj.category)
        if not category is None:
            try:
                categoryobj.category = rest.api.update_parts_category(categoryobj.category.id, category)
                self.tree_categories_manager.UpdateItem(categoryobj)
                self.onTreeCategoriesSelChanged(None)
            except Exception as e:
                wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

    def onButtonRemoveCategoryClick( self, event ):
        sel = self.tree_categories.GetSelection()
        categoryobj = self.tree_categories_manager.ItemToObject(sel)
        if categoryobj is None:
            return
        try:
            res = wx.MessageDialog(self, "Remove category '"+categoryobj.category.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
            if res==wx.ID_OK:
                rest.api.delete_parts_category(categoryobj.category.id)
                self.tree_categories_manager.DeleteItem(categoryobj.parent, categoryobj)
            else:
                return
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)



    def onButtonRemoveFilterClick( self, event ):
        button = event.GetEventObject()
        self.parts_filter.remove(button.GetName())
        self.tree_categories.UnselectAll()
        self.loadParts()


    def onTreeCategoriesSelChanged( self, event ):
        item = self.tree_categories.GetSelection()
        category = None
        if item.IsOk():
            category = self.tree_categories_manager.ItemToObject(item)
        # set category filter
        self.parts_filter.remove('category')
        if category:
            self.parts_filter.add('category', category.category.id, category.category.name)
        # apply new filter and reload
        self.loadParts()

    def onTreeCategoriesDropCategory(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))
        try:
            source_category_id = data['id']
            source_category = rest.api.find_parts_category(source_category_id)
            source_categoryitem = helper.tree.TreeManager.drag_item
            source_categoryobj = self.tree_categories_manager.ItemToObject(source_categoryitem)
    
            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                if source_category_id==dest_category.id:
                    return wx.DragError
                source_category.parent = rest.model.PartCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_category.parent = None
            
            # update on server
            category = rest.api.update_parts_category(source_category.id, source_category)

            # update tree model
            if source_categoryobj:
                self.tree_categories_manager.MoveItem(source_categoryobj.parent, dest_categoryobj, source_categoryobj)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)

        return wx.DragMove

    def onTreeCategoriesDropPart(self, x, y, data):
        dest_categoryitem, _ = self.tree_categories.HitTest((x, y))

        try:
            source_part_id = data['id']
            source_part = rest.api.find_part(source_part_id)

            dest_category = None
            dest_categoryobj = None
            if dest_categoryitem.IsOk():
                dest_categoryobj = self.tree_categories_manager.ItemToObject(dest_categoryitem)
                dest_category = dest_categoryobj.category
                source_part.category = rest.model.PartCategoryRef(id=dest_category.id)
            else:
                # set if as root category
                source_part.category = None
            
            # update on server
            part = rest.api.update_part(source_part.id, source_part)
            
            # update tree model
            self.tree_parts_manager.DeletePart(source_part)
            self.tree_parts_manager.AppendPart(part)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        return wx.DragMove


    def onTreePartsSelChanged( self, event ):
        item = self.tree_parts.GetSelection()
        part = None
        if item.IsOk():
            obj = self.tree_parts_manager.ItemToObject(item)
        if isinstance(obj, DataModelPart):
            part = obj.part
            self.load_full_part(obj)
        self.show_part(part)

            
    def onEditPartApply( self, event ):
        part = event.data
        print type(part), part.to_str()
        try:
            if self.edit_state=='edit':
                # update part on server
                part = rest.api.update_part(part.id, part)
                self.tree_parts_manager.Update(part)
            elif self.edit_state=='add':
                part = rest.api.add_part(part)
                self.tree_parts_manager.AppendPart(part)
        except Exception as e:
            wx.MessageBox(format(e), 'Error', wx.OK | wx.ICON_ERROR)
        self.edit_state = None
        self.show_part(part)
     
    def onEditPartCancel( self, event ):
        part = None
        if self.tree_parts.GetSelection():
            part = self.parts_model.ItemToObject(self.tree_parts.GetSelection())
        self.edit_state = None
        self.show_part(part)


    def onButtonAddPartClick( self, event ):
        self.edit_state = 'add'
        self.new_part()













#     def onButtonAddPartClick( self, event ):
#         self.edit_state = 'add'
#         self.new_part()
# 
#     def onButtonEditPartClick( self, event ):
#         if not self.tree_parts.GetSelection():
#             return
#         part = self.parts_model.ItemToObject(self.tree_parts.GetSelection())
#         self.edit_state = 'edit'
#         self.edit_part(part)
# 
#     def onButtonRemovePartClick( self, event ):
#         item = self.tree_parts.GetSelection()
#         if not item:
#             return 
#         part = self.parts_model.ItemToObject(item)
#         if part.parent:
#             res = wx.MessageDialog(self, "Remove part '"+part.name+"' from '"+part.parent.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
#             if res==wx.ID_OK:
#                 # remove selected part from subparts
#                 part.parent.parts.remove(part.id)
#                 PartsQuery().update(part.parent)
#             else:
#                 return 
#         else:
#             res = wx.MessageDialog(self, "Remove part '"+part.name+"'", "Remove?", wx.OK|wx.CANCEL).ShowModal()
#             if res==wx.ID_OK:
#                 # remove part
#                 PartsQuery().delete(part)
#             else:
#                 return
#         self._loadParts()
#         event.Skip()
# 
#     def onSearchPartsTextEnter( self, event ):
#         # set search filter
#         self.parts_filter.remove('search')
#         if self.search_parts.Value!='':
#             self.parts_filter.add('search', self.search_parts.Value)
#         # apply new filter and reload
#         self._loadParts()
# 
#     def onButtonRefreshPartsClick( self, event ):
#         self.loadParts()
# 
#     def onTreePartsItemBeginDrag( self, event ):
#         part = self.parts_model.ItemToObject(event.GetItem())
#         data =  PartDataObject(part)
#         event.SetDataObject(data)
# 
#         
#     def onTreePartsItemDrop( self, event ):
#         event.Allow()
# 
#     def onTreePartsItemCollapsed( self, event ):
#         event.Skip()
#     
#     def onTreePartsItemExpanded( self, event ):
#         event.Skip()
# 
#     def onTreePartsItemExpanding( self, event ):
#         item = event.GetItem()
#         print type(item)
#         if item:
#             obj = self.parts_model.ItemToObject(item)
#         if isinstance(obj, DataModelPart) and obj.part.has_childs and obj.childs_loaded==False:
#             print "Loading childs", obj.part.id
#             part = rest.api.find_part(obj.part.id, with_childs=True)
#             obj.part.childs = part.childs
#             
#             for child in obj.part.childs:
#                 for part in obj.part.childs:
#                     item. children.append(self.ObjectToItem(DataModelPart(part, obj)))
#             self.parts_model.ItemsChanged(item)
#             
#     
#     def onTreePartsSelectionChanged( self, event ):
#         part = None
#         if event.GetItem():
#             part = self.parts_model.ItemToObject(event.GetItem())
#         self.show_part(part)
# 
