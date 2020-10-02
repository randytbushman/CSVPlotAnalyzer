import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar


class Graph:
    def __init__(self, wxPanel, wxMinSize):
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(wxPanel, -1, self.figure)
        self.canvas.SetMinSize(wxMinSize)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.set_message = wxPanel.GetTopLevelParent().updateStatus     # Overrides function as the default does not work
        self.nameTracker = NameTracker()

        # Real labels
        self.dataSetLabel = 'Data Set'
        self.bestFitLabel = 'Best Fit'
        self.residualsLabel = 'Residuals'

        # Arrays of all known plot data
        self.backupXData = None
        self.backupYData = None
        self.xData = None
        self.yData = None
        self.baseline = None
        self.initialFit = None
        self.bestFit = None
        self.residuals = None

        self.axes.grid(True)

    def __getLineIndexFromDisplayLabel(self, displayLabel):
        """
        Searches the lines array in the axes for a line with the given
        label and returns its index.
        :param displayLabel:
        :return:
        """
        lines = self.axes.get_lines()
        for i in range(len(lines)):
            if lines[i].get_label() == displayLabel:
                return i
        return -1

    def __getLineIndexFromRealLabel(self, realLabel):
        return self.__getLineIndexFromDisplayLabel(self.nameTracker.getDisplayNameFromRealName(realLabel))

    def getLegendList(self):
        """
        Returns a string list of all of the lines in the legend,
        even those that are invisible and not displayed.
        :return: a string list of all legend elements
        """
        return [line.get_label() for line in self.axes.get_lines()]

    def getLineAlpha(self, lineIndex):
        return self.axes.get_lines()[lineIndex].get_alpha()

    def getLineColor(self, lineIndex):
        return matplotlib.colors.to_hex(self.axes.get_lines()[lineIndex].get_color())

    def getLineInfo(self, lineIndex):
        """
        Returns the alpha, color, line style, visibility state, z order, and label
        of the line we are looking for, given the label of the line.
        :param lineIndex:
        :return: alpha, color, line style, visibility state, z order, and label of line
        """
        line = self.axes.get_lines()[lineIndex]
        return line.get_alpha(), matplotlib.colors.to_hex(line.get_color()), line.get_linestyle(), line.get_visible(), line.get_zorder(), line.get_label()

    def getLineStyle(self, lineIndex):
        """
        Returns the linestyle of the line at the given index in the axes array.
        :param lineIndex:
        :return:
        """
        return self.axes.get_lines()[lineIndex].get_linestyle()

    def getLineVisibilityState(self, lineIndex):
        """
        Returns the visibility state of the line at the given index in the axes array.
        :param lineIndex:
        :return:
        """
        return self.axes.get_lines()[lineIndex].get_visible()

    def getLineZOrder(self, lineIndex):
        """
        Returns the zOrder of the line at the given index in the axes array.
        :param lineIndex:
        :return:
        """
        return self.axes.get_lines()[lineIndex].get_zorder()

    def setColorMultipleLines(self, axesIndexes, color):
        lines = self.axes.get_lines()
        for index in axesIndexes:
            lines[index].set_color(color)

    def setPlotTitle(self, title):
        """
        Renames the title of the graph.
        :param title: The new title of the graph.
        """
        self.axes.set_title(title)

    def setXLabel(self, xLabel):
        """
        Renames the x axis label on the graph.
        :param xLabel: The new label of the x axis
        """
        self.axes.set_xlabel(xLabel)

    def setYLabel(self, yLabel):
        """
        Renames the y axis label on the graph.
        :param yLabel: The new label of the y axis
        """
        self.axes.set_ylabel(yLabel)

    def changeLineAttributesGivenIndex(self, index, alpha, color, lineStyle, visibility, zOrder, newLabel):
        """
        Changes the attributes of the line in the axes array with the given index.
        :param index:
        :param alpha:
        :param color:
        :param lineStyle:
        :param visibility:
        :param zOrder:
        :param newLabel:
        :return:
        """
        line = self.axes.get_lines()[index]
        if alpha is not None:
            line.set_alpha(alpha)
        if color is not None and color != '':
            line.set_color(color)
        if lineStyle is not None and lineStyle != '':
            line.set_linestyle(lineStyle)
        if visibility is not None:
            line.set_visible(visibility)
        if zOrder is not None:
            line.set_zorder(zOrder)
        if newLabel is not None and newLabel != '':
            if True:
                self.nameTracker.renameDisplayNameGivenOldDisplayName(line.get_label(), newLabel)
                line.set_label(newLabel)
            else:
                errorStr += 'Cannot rename ' + oldLabel + ' to ' + newLabel + ' because the name already exists.'

    def __plot(self, xData, yData, label, style=None, visible=True):
        """
        Plots the given x and y data to the given axes.
        :param xData:
        :param yData:
        :param label:
        :param style:
        :param visible:
        """
        if style is None:
            self.axes.plot(xData, yData, label=label, alpha=1, visible=visible)
        else:
            self.axes.plot(xData, yData, style, label=label, alpha=1, visible=visible)
        self.nameTracker.addEntry(label)

    def plotNewDataset(self, xData, yData):
        """
        Plots a new signal. Will overwrite signal data as well as backup.
        Do not mistake for updateSignalData() as that function is intended
        for existing signals to modify.
        data.
        :param xData:
        :param yData:
        :return:
        """
        self.xData = xData.copy()
        self.yData = yData.copy()
        self.backupXData = xData.copy()
        self.backupYData = yData.copy()
        self.__plot(xData, yData, self.dataSetLabel, 'b')

    def redrawCanvas(self):
        """
        This function redraws the canvas on screen. Is necessary to call anytime
        that the plot is updated in anyway.
        :return:
        """
        self.canvas.draw()

    def rescale(self):
        """
        This function will fix the scaling with when there are different sized
        plots on screen. Is necessary to call when the use adds or removes a new
        segment to the graph. Will only scale visible plots.
        :return:
        """
        self.axes.relim(True)
        self.axes.autoscale_view()
        self.toolbar.Update()

    def __removeLineGivenDisplayLabel(self, displayLabel):
        lines = self.axes.get_lines()
        for i in range(len(lines)):
            if displayLabel == lines[i].get_label():
                lines.pop(i).remove()
                self.nameTracker.removeEntryGivenRealName(displayLabel)
                break

    # May not work. get displayLabel from realLabel if this does not work
    def __removeLineGivenRealLabel(self, realLabel):
        lines = self.axes.get_lines()
        for i in range(len(lines)):
            if lines[i].get_label() == realLabel:
                lines.pop(i).remove()
                self.nameTracker.removeEntryGivenRealName(realLabel)
                break

    def __removeLinesGivenRealLabelPrefix(self, realLabelPrefix):
        lines = self.axes.get_lines()
        segLen = len(realLabelPrefix)
        for i in reversed(range(len(lines))):
            line = lines[i]
            if self.nameTracker.getRealNameFromDisplayName(line.get_label())[:segLen] == realLabelPrefix:
                lines.pop(i).remove()
        self.nameTracker.removeAllEntriesWithRealPrefix(realLabelPrefix)

    def removeAllLinesInAxes(self):
        lines = self.axes.get_lines()
        for i in reversed(range(len(lines))):
            lines.pop(i).remove()
        self.nameTracker.clear()
        self.backupXData = None
        self.backupYData = None
        self.xData = None
        self.yData = None
        self.baseline = None
        self.initialFit = None
        self.bestFit = None
        self.residuals = None

    def removeBaseLine(self):
        self.__removeLineGivenDisplayLabel(self.dataSetLabel)
        self.baseline = None

    def removeInputSpecta(self):
        self.__removeLinesGivenRealLabelPrefix(self.realInputSpectraLabelPrefix)
        self.inputPredictedPeaksXData = None
        self.inputPredictedPeaksYData = None

    # TODO Identify which lines are being deleted and update fields
    def removeLinesWithAxeIndexes(self, indexes):
        """
        Removes the lines at the given indexes.
        :param indexes: a sorted list of line indexes in axes lines array
        :return:
        """
        lines = self.axes.get_lines()
        for i in reversed(indexes):
            realLabel = self.nameTracker.getRealNameFromDisplayName(lines[i].get_label())
            if realLabel == self.dataSetLabel:
                self.baseline = None
            elif realLabel == self.bestFitLabel:
                self.bestFit = None
            elif realLabel == self.realInitialFitLabel:
                self.initialFit = None
            elif realLabel == self.realResidualLabel:
                self.residuals = None
            elif realLabel == self.realSignalLabel:
                self.xData = None
                self.yData = None
                self.backupXData = None
                self.backupYData = None
                # Remove mapping and decon data.
            elif realLabel[:len(self.realDeconPeakLabelPrefix)] == self.realDeconPeakLabelPrefix:
                print('Need to remove decon data')
            elif realLabel[:len(self.realGuessPeaksLabelPrefix)] == self.realGuessPeaksLabelPrefix:
                print('Need to remove guess peak')
            elif realLabel[:len(self.realInputSpectraLabelPrefix)] == self.realInputSpectraLabelPrefix:
                print('Need to remove input spectra')
            elif realLabel[:len(self.mappingPrefix)] == self.mappingPrefix:
                print('Need to remove mapping')
            lines.pop(i).remove()
            self.nameTracker.removeEntryGivenRealName(realLabel)

    def removeDataSet(self):
        self.__removeLineGivenRealLabel(self.dataSetLabel)
        self.xData = None
        self.yData = None
        self.backupXData = None
        self.backupYData = None

    def restoreOriginalPlot(self):
        """
        Will replace the altered signal with its backup data and re-plots it.
        :return:
        """
        self.xData = self.backupXData.copy()
        self.yData = self.backupYData.copy()
        self.updateSignalData(self.xData, self.yData)

    def updateLegend(self):
        """
        Updates the legend to the graph. Will only display visible plots.
        If there are no visible plots, the legend will disappear.
        :return:
        """
        lines = self.axes.get_lines()
        legendLines = [line for line in lines if line.get_visible()]
        if self.axes.get_legend() is not None and len(legendLines) == 0:
            self.axes.get_legend().remove()
        else:
            self.axes.legend(handles=legendLines)

    def updateGraph(self):
        """
        Updates the legend, scale and graph canvas. These functions can
        be found separately in this class, but for convenience, this function
        compresses them all into one. Only use this function if you are updating
        all three!
        """
        self.rescale()
        self.updateLegend()
        self.redrawCanvas()


class NameTracker:
    """
    The NameTracker is a special kind of data structure that allows
    the user to efficiently store the display name and the real name
    of the lines on a graph. The display name is the name that is
    displayed on the graph, legend, and possibly a ui, while the real
    name is the name given to the line when it is first created.

    For example, say the user plots a line originally named 'signal'.
    The user wants to change the name of 'signal' to 'test'. If we
    overwrite the name 'signal' it would make some functions harder to
    operate as we would have to remember that 'test' is the new name.
    This data structure will efficiently (in terms of access time) keep
    track of all of the display names and real names.

    There are no duplicates of real names and no duplicates of display names
    in this data structure. By default, when a name is added its display name
    is the same as its real name.

    Implementation is not complete, but will work in most cases!
    """
    def __init__(self):
        self.__realNameKeys = {}
        self.__displayNameKeys = {}

    def __str__(self):
        return '{Real Name: Display Name} -> ' + str(self.__realNameKeys)

    def getDisplayNameFromRealName(self, realName):
        return self.__realNameKeys[realName]

    def getAllDisplayNames(self):
        return self.__realNameKeys.keys()

    def getRealNameFromDisplayName(self, displayName):
        return self.__displayNameKeys[displayName]

    def addEntry(self, realName, displayName=None):
        if displayName is None:
            displayName = realName
        self.__realNameKeys[realName] = displayName
        self.__displayNameKeys[displayName] = realName

    def clear(self):
        self.__realNameKeys = {}
        self.__displayNameKeys = {}

    def removeEntryGivenDisplayName(self, displayName):
        try:
            realName = self.getDisplayNameFromRealName(displayName)
            del self.__realNameKeys[displayName]
            del self.__displayNameKeys[realName]
        except KeyError:
            pass

    def removeEntryGivenRealName(self, realName):
        try:
            displayName = self.getDisplayNameFromRealName(realName)
            del self.__realNameKeys[realName]
            del self.__displayNameKeys[displayName]
        except KeyError:
            pass

    def removeAllEntriesWithRealPrefix(self, labelSegment):
        segLength = len(labelSegment)
        toRemove = []
        for label in self.__realNameKeys.keys():
            if label[:segLength] == labelSegment:
                toRemove.append(label)
        for label in toRemove:
            self.removeEntryGivenRealName(label)

    def renameDisplayNameGivenOldDisplayName(self, oldDisplayName, newDisplayName):
        realName = self.getRealNameFromDisplayName(oldDisplayName)
        self.__realNameKeys[realName] = newDisplayName
        del self.__displayNameKeys[oldDisplayName]
        self.__displayNameKeys[newDisplayName] = realName

    def renameDisplayNameGivenRealName(self, label, newAlias):
        oldAlias = self.getDisplayNameFromRealName(label)
        self.__realNameKeys[label] = newAlias
        del self.__displayNameKeys[oldAlias]
        self.__displayNameKeys[newAlias] = label

