import wx
from ObjectListView2 import ObjectListView, ColumnDefn

from Data import DataHandler


class OLVPanel(wx.Panel):
    """
    Panel that contains the list view of a library

    Attributes:
        self.olv: ObjectListView: wx.ListCtrl

    """

    def __init__(self, parent, data: DataHandler):
        wx.Panel.__init__(self, parent)
        self.data = data

        sources = data.database.select_all_source_folders()
        choices = ['All Assets']
        for source in sources: choices.append(source[3])

        self.source_choice = wx.Choice(self, choices=choices)
        self.source_choice.SetSelection(0)

        idn_column = ColumnDefn("ID", "right", 60, "idn")
        sku_column = ColumnDefn("SKU", "right", 80, "sku")
        product_name_column = ColumnDefn("Product Name", "left", 160, "product_name", isSpaceFilling=True)
        zip_size_column = ColumnDefn("Zip Size", "right", 90, "get_size")
        installed_column = ColumnDefn("Installed", "right", 90, "get_installed")

        self.columns = [idn_column, sku_column, product_name_column, zip_size_column, installed_column]
        assets = data.database.select_all_assets()

        self.olv = ObjectListView(parent=self, style=wx.LC_REPORT | wx.SUNKEN_BORDER,
                                  useAlternateBackColors=True)

        self.olv.SetColumns(self.columns)
        self.olv.SetObjects(assets)

        self.olv.oddRowsBackColor = wx.Colour(255, 255, 255)
        self.olv.evenRowsBackColor = wx.Colour(240, 240, 240)
        self.olv._FormatAllRows()

        main_box = wx.BoxSizer(wx.VERTICAL)
        main_box.Add(self.source_choice, 0, wx.EXPAND | wx.ALL, 5)
        main_box.Add(self.olv, 1, wx.EXPAND | wx.ALL, 5)
        self.SetSizer(main_box)

        self.source_choice.Bind(wx.EVT_CHOICE, self.on_source_change)

    def on_source_change(self, event=None):
        selection = self.source_choice.GetSelection()

        if selection == 0:
            assets = self.data.database.select_all_assets()
        else:
            assets = self.data.database.select_all_assets_by_parent(selection - 1)

        self.olv.DeleteAllItems()
        self.olv.SetObjects(assets)
