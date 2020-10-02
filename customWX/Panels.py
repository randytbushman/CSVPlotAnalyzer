import wx
import wx.lib.scrolledpanel as sp


class OptionsPanel(sp.ScrolledPanel):
    def __init__(self, parent, style):
        super().__init__(parent=parent, style=style)
        self.mainVBox = wx.BoxSizer(wx.VERTICAL)
        self.SetupScrolling()

    def addExistingButton(self, button=None, vBox=None):
        if vBox is None:
            vBox = self.mainVBox
        self.addWidgetLeftLabel(button, flag=wx.BOTTOM | wx.TOP | wx.ALIGN_CENTER_HORIZONTAL, vBox=vBox)
        return button

    def addWidgetLeftLabel(self, widget, label='', flag=wx.BOTTOM | wx.TOP, vBox=None):
        if vBox is None:
            vBox = self.mainVBox
        hBox = wx.BoxSizer(wx.HORIZONTAL)
        if not label == '':
            text = wx.StaticText(self, label=label)
            hBox.Add(text, 0, wx.LEFT | wx.RIGHT, 5)
        hBox.Add(widget, 0, wx.LEFT | wx.RIGHT, 5)
        vBox.Add(hBox, 0, flag, 10)

    def addSectionTitle(self, title, border=10, flag=wx.TOP | wx.BOTTOM | wx.ALIGN_CENTER_HORIZONTAL, vBox=None):
        if vBox is None:
            vBox = self.mainVBox
        text = wx.StaticText(self, label=title, style=wx.ALIGN_CENTER)
        text.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD))
        vBox.Add(text, 0, flag, border)

    def appendMainVBox(self, vBoxToAdd, border=10):
        self.mainVBox.Add(vBoxToAdd, 0, wx.EXPAND | wx.BOTTOM | wx.TOP | wx.LEFT | wx.RIGHT, border)

    def addStaticLine(self, border=10, flag=wx.EXPAND | wx.BOTTOM | wx.TOP, vBox=None):
        if vBox is None:
            vBox = self.mainVBox
        line = wx.StaticLine(self)
        vBox.Add(line, 0, flag, border)
