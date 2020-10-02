import wx
import Graph


class GraphPanel(wx.Panel):
    def __init__(self, parent, frame):
        super().__init__(parent=parent, style=wx.SUNKEN_BORDER)
        self.frame = frame
        self.graph = Graph.Graph(self, wx.Size(1, 1))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.graph.canvas, 1, wx.GROW)
        sizer.Add(self.graph.toolbar, 0, wx.EXPAND)
        self.SetSizer(sizer)
        self.Fit()

    def changeLineAttributes(self, event):
        """

        :param event: wx event triggered by widget
        :return:
        """
        graph = self.graph
        gt = self.frame.graphOptionsTab
        legendIndexes = gt.getLegendSelectionIndexes()
        if len(legendIndexes) > 0:
            alpha = gt.getAlpha()
            color = gt.getLineColor()
            style = gt.getLineStyle()
            visibility = gt.getLineVisibilityState()
            zOrder = gt.getZOrder()
            newLabel = gt.getLineLabel()
            if len(legendIndexes) == 1 or newLabel == '':    # get rid of newLabel == '' somehow
                for index in legendIndexes:
                    graph.changeLineAttributesGivenIndex(index, alpha, color, style, visibility, zOrder, newLabel)
            else:
                for i, index in enumerate(legendIndexes):
                    graph.changeLineAttributesGivenIndex(index, alpha, color, style, visibility, zOrder, f'{newLabel} {i}')
            graph.updateGraph()
            gt.setLegendList(graph.getLegendList())
            self.frame.analysisOptionsTab.setPreviewPeakList(graph.getGuessPeakDisplayLabels())
            self.updateGraphLineWidgetInfo(event)
        else:
            self.frame.updateStatus('No line selected')

    def clearOutputPanels(self, event):
        """

        :param event: wx event triggered by widget
        :return:
        """
        self.frame.consoleTabPanel.clear()
        self.frame.parameterTabPanel.clearList()

    def deleteSelectedLines(self, event):
        """
        Will remove all of the lines that are selected in the line manipulation table
        from the graph and from the table itself.
        :param event:
        :return:
        """
        self.graph.removeLinesWithAxeIndexes(self.frame.graphOptionsTab.getLegendSelectionIndexes())
        self.graph.updateGraph()
        self.frame.graphOptionsTab.setLegendList(self.graph.getLegendList())

    def getGraph(self):
        """
        Returns the graph.
        :return:
        """
        return self.graph

    def rescaleGraph(self, event):
        self.graph.rescale()
        self.graph.redrawCanvas()

    def interpolateData(self, event):
        pass

    def smoothData(self, event):
        pass

    def updateGraphLineWidgetInfo(self, event):
        """

        :param event: wx event triggered by widget
        :return:
        """
        selections = self.frame.graphOptionsTab.getLegendSelectionIndexes()
        got = self.frame.graphOptionsTab
        if len(selections) == 0:
            got.disableLineManipulationWidgets()
        elif len(selections) == 1:
            got.enableLineManipulationWidgets()
            got.updateGraphLineWidgetInfo(*self.graph.getLineInfo(selections[0]))
        elif len(selections) > 1:
            # got.enableLineManipulationWidgets()   If there are bugs with the widgets, uncomment this. Should not have to
            got.setLineManipulationWidgetsToDefaultState()
        else:
            self.frame.updateStatus('No line selected')

    def updatePlotName(self, event, title=None, redrawCanvas=True):
        """

        :param event: wx event triggered by widget
        :param title:
        :param redrawCanvas:
        :return:
        """
        graphOptionsTab = self.frame.graphOptionsTab
        if title is None:
            title = graphOptionsTab.getPlotName()
        graphOptionsTab.graphTitleBox.ChangeValue(title)
        graph = self.graph
        graph.setPlotTitle(title)
        if redrawCanvas:
            graph.redrawCanvas()

    def updatePlotXLabel(self, event, xLabel=None, redrawCanvas=True):
        """

        :param event: wx event triggered by widget
        :param xLabel:
        :param redrawCanvas:
        :return:
        """
        graphOptionsTab = self.frame.graphOptionsTab
        if xLabel is None:
            xLabel = graphOptionsTab.getPlotXLabel()
        graphOptionsTab.xLabelBox.ChangeValue(xLabel)
        graph = self.graph
        graph.setXLabel(xLabel)
        if redrawCanvas:
            graph.redrawCanvas()

    def updatePlotYLabel(self, event, yLabel=None, redrawCanvas=True):
        """

        :param event: wx event triggered by widget
        :param yLabel:
        :param redrawCanvas:
        :return:
        """
        graphOptionsTab = self.frame.graphOptionsTab
        if yLabel is None:
            yLabel = graphOptionsTab.getPlotYLabel()
        graphOptionsTab.yLabelBox.ChangeValue(yLabel)
        graph = self.graph
        graph.setYLabel(yLabel)
        if redrawCanvas:
            graph.redrawCanvas()

    def changeColorWithDialog(self, event):
        """

        :param event: wx event triggered by widget
        :return:
        """
        graph = self.graph
        data = wx.ColourData()
        data.SetChooseFull(True)
        selections = self.frame.graphOptionsTab.getLegendSelectionIndexes()
        color = wx.Colour(graph.getLineColor(selections[0]))
        data.SetColour(color)
        dlg = wx.ColourDialog(self, data)
        dlg.CentreOnParent()
        if dlg.ShowModal() == wx.ID_OK:
            color = dlg.GetColourData().GetColour().GetAsString(flags=wx.C2S_HTML_SYNTAX)
            graph.setColorMultipleLines(selections, color)
            graph.updateLegend()
            graph.redrawCanvas()
        dlg.Destroy()

    def newDataSet(self, xData, yData):
        """
        Will plot new data to the graph, delete all old data at the same time.
        :param event: wx event triggered by widget
        :param xData:
        :param yData:
        :param xLabel:
        :param yLabel:
        :param title:
        :return:
        """
        graph = self.graph

        # self.frame.analysisOptionsTab.updateCurrentNumPoints(len(xData))
        # self.clearOutputPanels(event)

        graph.removeDataSet()

        graph.plotNewDataset(xData, yData)
        # graph.plotNewSignal(xData, yData)
        graph.updateGraph()

        # self.frame.graphOptionsTab.setLegendList(graph.getLegendList())
        # self.frame.analysisOptionsTab.clearPreviewPeakList()
        self.frame.updateStatus('Created new plot!')
