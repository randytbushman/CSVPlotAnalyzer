import wx
from customWX import Panels


class AnalysisPanel(Panels.OptionsPanel):
    def __init__(self, parent, frame):
        super().__init__(parent=parent, style=wx.SUNKEN_BORDER)
        self.frame = frame
        gp = self.frame.graphPanel

        # Data Interpolation Section
        # Declare Widgets
        self.addSectionTitle('Data Interpolation')
        self.interpStaticBox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY), wx.VERTICAL)
        self.interpolationTypeChoiceBox = wx.Choice(self, choices=['Linear', 'Quadratic', 'Cubic'])
        self.interpolationTypeChoiceBox.SetSelection(1)
        self.numInterpPointsCtrl = wx.SpinCtrl(self, initial=1000, min=250, max=50000)
        self.currentNumPoints = wx.TextCtrl(self, style=wx.TE_READONLY)
        self.interpolateDataButton = wx.Button(self, -1, 'Interpolate Data')
        self.interpolateDataButton.Bind(wx.EVT_BUTTON, gp.interpolateData)

        # Bind Widgets
        self.interpolateDataButton.Bind(wx.EVT_BUTTON, gp.interpolateData)

        # Position Widgets
        self.addWidgetLeftLabel(self.interpolationTypeChoiceBox, 'Type', vBox=self.interpStaticBox)
        self.addWidgetLeftLabel(self.currentNumPoints, 'Current Number of Points', vBox=self.interpStaticBox)
        self.addWidgetLeftLabel(self.numInterpPointsCtrl, 'Interpolate to', vBox=self.interpStaticBox)
        self.addExistingButton(self.interpolateDataButton, vBox=self.interpStaticBox)
        self.appendMainVBox(self.interpStaticBox)
        self.addStaticLine()

        # Data Smoothing Section
        # Declare Widgets
        self.addSectionTitle('Smooth Data')
        self.smoothStaticBox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY), wx.VERTICAL)
        self.smoothPoly = wx.SpinCtrl(self, initial=3, min=1, max=15)
        self.smoothWinLength = wx.SpinCtrl(self, initial=11, min=3, max=101)
        self.smoothDataButton = wx.Button(self, -1, 'Smooth Data')

        # Bind Widgets
        self.smoothDataButton.Bind(wx.EVT_BUTTON, gp.smoothData)

        # Position Widgets
        self.addWidgetLeftLabel(self.smoothPoly, 'Polynomial Order', vBox=self.smoothStaticBox)
        self.addWidgetLeftLabel(self.smoothWinLength, 'Window Length', vBox=self.smoothStaticBox)
        self.addExistingButton(self.smoothDataButton, vBox=self.smoothStaticBox)
        self.appendMainVBox(self.smoothStaticBox)
        self.addStaticLine()

        # Data Fitting Section
        self.addSectionTitle('Data Fitting')
        self.addStaticLine()

        self.SetSizer(self.mainVBox)

    def getCurrentNumPoints(self):
        return self.currentNumPoints.GetValue()

    def getInterpolationMethod(self):
        return self.interpolationTypeChoiceBox.GetStringSelection()

    def getNumberToInterpolateTo(self):
        return self.numInterpPointsCtrl.GetValue()

    def getSmoothingPoly(self):
        return self.smoothPoly.GetValue()

    def getSmoothingWindow(self):
        return self.smoothWinLength.GetValue()
